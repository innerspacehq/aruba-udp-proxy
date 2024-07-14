class DataPayload:
    """A class to represent and manage a data payload."""

    def __init__(self, data: bytes = None):
        """Initialize the DataPayload instance."""
        self.payload = ""
        if data:
            self.parse(data)

    def parse(self, payload_data: bytes):
        """Parse the given data and set it as the payload"""
        self.payload = payload_data
