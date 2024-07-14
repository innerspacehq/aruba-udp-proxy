import binascii

from models.aruba.messagetypes import MessageTypes


class DataHeader:
    """A class to represent and manage a data header."""

    HEADER_LENGTH = 16

    def __init__(self, data: bytes = None):
        """Initialize the DataHeader instance."""
        self.header = ""
        self.message_type = "0000"
        self.message_id = "0000"
        self.major_version = "00"
        self.minor_version = "00"
        self.payload_length = "0000"
        self.ap_mac = "00:00:00:00:00:00"
        self.padding = "0000"

        if data:
            self.parse(data)

    def get_message_type(self) -> MessageTypes:
        """Get the message type."""
        return self.message_type

    def set_message_type(self, message_type: MessageTypes):
        """Set the message type."""
        self.message_type = message_type

    def parse(self, header_data: bytes):
        """Parse the given data and set it as the header"""

        if len(header_data) == self.HEADER_LENGTH:
            self.header = header_data
            self.message_type = MessageTypes(header_data[:2])
            self.message_id = int.from_bytes(header_data[2:4], byteorder="big")
            self.major_version = int.from_bytes(header_data[4:5], byteorder="big")
            self.minor_version = int.from_bytes(header_data[5:6], byteorder="big")
            self.payload_length = int.from_bytes(header_data[6:8], byteorder="big")
            self.ap_mac = ":".join("%02x" % b for b in header_data[8:14])
            self.padding = int.from_bytes(header_data[14:], byteorder="big")
        else:
            raise Exception("Invalid data header length.")

    def to_binary(self) -> bytes:
        """Convert the data header to its binary representation"""
        packet = bytearray()
        packet.extend(self.get_message_type().value)
        packet.extend(self.message_id.to_bytes(2, byteorder="big"))
        packet.append(self.major_version)
        packet.append(self.minor_version)
        packet.extend(self.payload_length.to_bytes(2, byteorder="big"))
        packet.extend(binascii.unhexlify(self.ap_mac.replace(":", "")))
        packet.extend(self.padding.to_bytes(2, byteorder="big"))

        if len(packet) == self.HEADER_LENGTH:
            return packet
        else:
            raise Exception("Invalid data header length.")
