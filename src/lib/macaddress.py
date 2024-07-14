import re


class MacAddress:
    """Utility class for MAC address validation."""

    @staticmethod
    def is_valid(mac: str) -> bool:
        """Check if the given MAC address is valid."""
        return re.match(
            "[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac.lower()
        )
