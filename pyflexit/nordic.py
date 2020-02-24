
class Nordic:
    """This class supports the Flexit Nordic models (S2, S3, S4, CL3)."""

    def __init__(self, client, unit: int):
        self._client = client
        self._unit = unit

    @staticmethod
    def update() -> bool:
        """Just for backwards compatibility with the CI66 implementation"""
        return True
