from pyflexit.common import HomeAssistantAPI
from typing import Tuple


class Nordic(HomeAssistantAPI):
    """This class supports the Flexit Nordic models (S2, S3, S4, CL3)."""

    def __init__(self, client, unit: int):
        self._client = client
        self._unit = unit

    @staticmethod
    def update() -> bool:
        """Just for backwards compatibility with the CI66 implementation"""
        return True

    @property
    def current_temperature(self) -> float:
        """HomeAssistantAPI: Get measured temperature for supply air.
        """
        raise NotImplementedError

    def set_temperature(self, temperature: float) -> None:
        """HomeAssistantAPI: Set target temperature for supply air

        The Nordic series have two separate target temperatures, one for
        "Home" and one for "Away". This method uses the current operating
        mode to select which target temperature to set. If the operating mode
        is neither "Home" nor "Away", setting the target temperature is thus
        not possible, and we raise an exception.
        """
        if self.fan_mode == "Home":
            self.set_home_temperature(temperature)
        elif self.fan_mode == "Away":
            self.set_away_temperature(temperature)
        else:
            raise RuntimeError(f"Cannot set target temperature in this "
                               f"operating mode: {self.fan_mode}")

    @property
    def fan_modes(self) -> Tuple[str, ...]:
        """Returns a tuple of strings with the valid fan modes"""
        return ("Off", "Away", "Home", "High", "Fume hood", "Fireplace",
                "Temporary high")

    @property
    def fan_mode(self) -> str:
        """Return a string with the current fan mode."""
        raise NotImplementedError

    def set_fan_mode(self, fan_mode: str) -> None:
        """Set new fan mode. The input string must be one of the first four
        values returned by self.fan_modes"""
        if fan_mode not in self.fan_modes[:4]:
            raise ValueError(f"Illegal fan mode: {fan_mode}. Supported "
                             f"values: {self.fan_modes[:4]}")
        raise NotImplementedError

    def set_home_temperature(self, value: float) -> None:
        """Set target temperature for supply air when in Home-mode"""
        raise NotImplementedError

    def set_away_temperature(self, value: float) -> None:
        """Set target temperature for supply air when in Away-mode"""
        raise NotImplementedError
