from abc import ABC, abstractmethod
from typing import Tuple


class HomeAssistantAPI(ABC):
    """This is an abstract base class to be inherited by the different Flexit
    model classes. We define an API that will be used by the Home Assistant
    climate component. This ensures Home Assistant compatibility across
    different Flexit models."""

    @property
    @abstractmethod
    def current_temperature(self) -> float:
        """Return current measured temperature (for supply air)"""
        pass

    @abstractmethod
    def set_temperature(self, temperature: float) -> None:
        """Set target temperature (for supply air)"""
        pass

    @property
    @abstractmethod
    def fan_modes(self) -> Tuple[str, ...]:
        """Return a tuple of strings with names of supported fan modes"""
        pass

    @property
    @abstractmethod
    def fan_mode(self) -> str:
        """Return current fan mode as a string"""
        pass

    @abstractmethod
    def set_fan_mode(self, fan_mode: str) -> None:
        """Set new fan mode. Input must be one of self.fan_modes"""
        pass
