import hmac
import logging
from hashlib import sha1

from lib.macaddress import MacAddress
from models.aruba.datahash import DataHash
from models.aruba.dataheader import DataHeader
from models.aruba.datapayload import DataPayload

# Configure logging
logging.basicConfig(
    format="%(asctime)s [%(levelname)6s] %(message)s", level=logging.INFO
)


class DataPacket:
    """A class to represent and manage a data packet."""

    def __init__(self, data: bytes = None):
        """Initialize the DataPacket instance."""
        if data and len(data) >= DataHeader.HEADER_LENGTH + DataHash.HASH_LENGTH:
            self.raw_data = data

            header_data = data[0 : DataHeader.HEADER_LENGTH]
            self.header = DataHeader(header_data)

            payload_data = data[
                DataHeader.HEADER_LENGTH : DataHeader.HEADER_LENGTH
                + self.header.payload_length
            ]
            self.payload = DataPayload(payload_data)

            hash_data = data[-DataHash.HASH_LENGTH :]
            self.hash = DataHash(hash_data)
        else:
            raise Exception("Invalid data received.")

    def to_binary(self) -> bytes:
        """Convert the data packet to its binary representation"""
        packet = bytearray()
        packet.extend(self.header.to_binary())
        return packet

    def validate(self, passphrase: str, client_address: str) -> bool:
        """Validate the data packet"""

        # check length
        expected_length = (
            DataHeader.HEADER_LENGTH + self.header.payload_length + DataHash.HASH_LENGTH
        )
        if len(self.raw_data) != expected_length:
            logging.error(
                f"Invalid message: Received data length does not match expected data length: "
                f"{len(self.raw_data)} vs {expected_length}"
            )
            return False

        # check checksum
        checksum_data = self.raw_data[
            0 : DataHeader.HEADER_LENGTH + self.header.payload_length
        ]
        target_checksum = hmac.new(
            bytes(passphrase, "utf-8"), bytes(checksum_data), sha1
        ).digest()
        if self.hash.hash != target_checksum:
            logging.error(
                f"Invalid message: Hash does not match message header and payload. : {self.header.ap_mac}"
            )
            return False

        # check MAC address
        mac_address = self.header.ap_mac
        if not MacAddress.is_valid(mac_address):
            logging.error(
                f"Invalid message: Unable to parse a valid MAC address from the data packet.: {mac_address}"
            )
            return False

        return True
