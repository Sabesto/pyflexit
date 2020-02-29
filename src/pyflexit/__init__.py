from pyflexit.ci66 import CI66
from pyflexit.nordic import Nordic


def aggregate(client, unit: int, model: str = "CI66"):
    """Returns the appropriate class, depending on the model"""

    # Somehow automatically determine what aggregate we're talking to

    if model == "CI66":
        return CI66(client, unit)
    elif model == "Nordic":
        return Nordic(client, unit)
    else:
        raise ValueError(f"Unknown Flexit model: {model}")

#
# class pyflexit:
#     """This is just a dummy class to avoid making a breaking change"""
#
#     @staticmethod
#     def pyflexit(client, unit: int, model: str = "CI66"):
#         """Returns the appropriate class, depending on the model"""
#         if model == "CI66":
#             return CI66(client, unit)
#         elif model == "Nordic":
#             return Nordic(client, unit)
#         else:
#             raise ValueError(f"Unknown Flexit model: {model}")
