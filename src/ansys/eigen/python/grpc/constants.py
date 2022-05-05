"""Python script for storing common constants for both gRPC server and client"""

from math import floor
from sys import getsizeof

import numpy as np

NP_DTYPE_TO_DATATYPE = {np.int32: "INTEGER", np.float64: "DOUBLE"}
"""Dictionary of constants showing the translation between the handled numpy dtypes and the gRPC DataType enum values."""

HUMAN_SIZES = ["B", "KB", "MB", "GB", "TB"]
"""List of human-readable sizes handled."""


def human_size(request: object):
    """Method to show the size of the message in human-readable format.

    Parameters
    ----------
    content_length : object
        The request message.

    Returns
    -------
    str
        The size of the message received in human-readable format.
    """
    idx = 0
    content_length = getsizeof(request)

    while True:
        if content_length >= 1024:
            idx += 1
            content_length = floor(content_length / 1024)
        else:
            break

    if idx >= len(HUMAN_SIZES):
        raise RuntimeError("Message size above TB level... Not handled!")

    return str(content_length) + HUMAN_SIZES[idx]
