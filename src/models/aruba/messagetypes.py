import enum


class MessageTypes(enum.Enum):
    """
    Enum representing various message types used in the application.

    Each message type is associated with a specific byte value.
    """

    AR_AS_CONFIG_SET = b"\x00\x00"
    AR_STATION_REQUEST = b"\x00\x01"
    AR_ACK = b"\x00\x10"
    AR_NACK = b"\x00\x11"
    AR_TAG_REPORT = b"\x00\x12"
    AR_STATION_REPORT = b"\x00\x13"
    AR_COMPOUND_MESSAGE_REPORT = b"\x00\x14"
    AR_AP_NOTIFICATION = b"\x00\x15"
    AR_MMS_CONFIG_SET = b"\x00\x16"
    AR_STATION_EX_REPORT = b"\x00\x17"
    AR_AP_EX_REPORT = b"\x00\x18"

    @staticmethod
    def convert_to_number(message_type: "MessageTypes") -> int:
        """Convert a MessageType to its corresponding integer value"""
        return int.from_bytes(message_type.value, byteorder="big")
