"""Monitor and control a Flexit ventilation aggregate via Modbus."""

import struct
from typing import Optional

from pyflexit.ci66 import CI66
from pyflexit.nordic import Nordic


def autodetect_flexit_model(client, unit):
    """Automatically detect what Flexit model we're talking to.

    Args:
        client: A modbus client
        unit: The modbus slave id of the Flexit aggregate

    Returns:
        A model string, either "CI66", "Nordic" or "EcoNordic"
    """
    response = client.read_holding_registers(9070, 20, unit=unit)
    if response.isError():
        return "CI66"
    model_string = b"".join(struct.pack(">H", r) for r in response.registers).decode(
        "UTF-8"
    )
    # For (Eco)Nordic, the model string will look like:
    # MDL:ASN= POS3.6715/414;HW=48.46.50;
    # The digit after the / is 4 in Nordic series, 5 in EcoNordic series
    if model_string[19] == "4":
        return "Nordic"
    if model_string[19] == "5":
        return "EcoNordic"
    raise ValueError(f"Unknown model string: {model_string}")


def aggregate(client, unit: int, model: Optional[str] = None):
    """Returns the appropriate class, depending on the model.

    Args:
        client: A modbus client
        unit: The modbus slave id of the Flexit aggregate
        model: Optionally specify the Flexit model, otherwise we autodetect.

    Returns:
        An instance of the appropriate Flexit class
    """
    if model is None:
        model = autodetect_flexit_model(client, unit)

    if model == "CI66":
        return CI66(client, unit)
    elif model in ("Nordic", "EcoNordic"):
        return Nordic(client, unit)
    else:
        raise ValueError(f"Unknown Flexit model: {model}")
