class DataHash:
    """A class to represent and manage a data hash."""

    HASH_LENGTH = 20

    def __init__(self, data: bytes = None):
        """Initialize the DataHash instance."""
        self.hash = ""
        if data:
            self.parse(data)

    def parse(self, hash_data: bytes):
        """Parse the given data and set it as the data hash."""
        if hash_data:
            self.hash = hash_data
