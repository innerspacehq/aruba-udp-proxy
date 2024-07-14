import base64
import hmac
import json
import logging
import os
import socketserver
import sys
import time
import traceback
from hashlib import sha1

import requests

# Configure logging
logging.basicConfig(
    format="%(asctime)s [%(levelname)6s] %(message)s", level=logging.INFO
)

# Import custom modules
from models.aruba.datapacket import DataPacket
from models.aruba.messagetypes import MessageTypes

# Environment variables
PASSPHRASE = os.getenv("PASSPHRASE")
HMAC = os.getenv("HMAC")
INGEST_SERVER_URL = os.getenv("INGEST_SERVER_URL", "https://ingest.innrspc.com")
HOST = os.getenv("HOST", "0.0.0.0")
UDP_PORT = os.getenv("PORT", "8090")


class RssiUdpDataHandler(socketserver.BaseRequestHandler):
    """Handler class for processing incoming UDP data packets."""

    def handle(self):
        """Handle incoming UDP data packets."""
        data = self.request[0]
        socket = self.request[1]
        try:
            data_packet = DataPacket(data)
            logging.info(f"Message type: {data_packet.header.message_type}")

            if data_packet.header.message_type == MessageTypes.AR_AP_NOTIFICATION:
                self.handle_ap_notification(data_packet, socket)
            else:
                aruba_raw_rssi_data = {
                    "ap_mac": data_packet.header.ap_mac,
                    "ts": str(time.time()),
                    "message_code": str(
                        MessageTypes.convert_to_number(data_packet.header.message_type)
                    ),
                    "payload": base64.b64encode(data_packet.payload.payload).decode(
                        "utf-8"
                    ),
                }
                self.call_sensor_ingest(HMAC, aruba_raw_rssi_data)

        except Exception as e:
            logging.error(f"Exception error: {e}")
            logging.error(traceback.format_exc())

    def handle_ap_notification(self, data_packet: DataPacket, socket):
        """Handles AP notification messages."""
        try:
            ack_data_packet = data_packet
            logging.debug(ack_data_packet.to_binary())
            ack_data_packet.header.set_message_type(MessageTypes.AR_ACK)
            ack_header = bytes(ack_data_packet.to_binary())
            ack_checksum = hmac.new(bytes(PASSPHRASE, "utf-8"), ack_header, sha1)
            ack_response_packet = bytearray()
            ack_response_packet.extend(ack_header)
            ack_response_packet.extend(ack_checksum.digest())
            response_bytes = bytes(ack_response_packet)
            socket.sendto(response_bytes, self.client_address)
        except Exception as e:
            logging.error("Exception error in handling AP notification: " + str(e))
            logging.error(traceback.format_exc())

    @staticmethod
    def call_sensor_ingest(base64_hmac: str, aruba_raw_rssi_data: dict) -> bool:
        """Pushes the data to the sensor-ingest service."""
        params = {"is-token": base64_hmac}
        result = requests.post(
            INGEST_SERVER_URL + "/rssi/aruba",
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            data=json.dumps(aruba_raw_rssi_data),
            params=params,
            timeout=30,
        )
        if not result.ok:
            logging.error(
                f"Failed to call sensor-ingest to push payload: {aruba_raw_rssi_data.get('ap_mac')}"
            )
            return None
        return result.ok


if __name__ == "__main__":
    try:
        # Check that the required environment variables are set
        if not HMAC:
            logging.error("HMAC is not set.")
            sys.exit(1)

        if not PASSPHRASE:
            logging.error("PASSPHRASE is not set.")
            sys.exit(1)

        # Ensure that PORT is an integer
        try:
            UDP_PORT = int(UDP_PORT)
        except ValueError:
            logging.error("PORT must be an integer.")
            sys.exit(1)

        logging.info(f"Starting UDP server on {HOST}:{UDP_PORT}")
        with socketserver.UDPServer((HOST, UDP_PORT), RssiUdpDataHandler) as server:
            server.serve_forever()
    except Exception as e:
        logging.error(f"UDP Server has crashed. {e}")
        logging.error(traceback.format_exc())
