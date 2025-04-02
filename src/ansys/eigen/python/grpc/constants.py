# Copyright (C) 2023 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Python script for storing common constants for both gRPC server and client."""

from math import floor
from sys import getsizeof

import numpy as np

MAX_CHUNKSIZE = 1024 * 1024 * 3
"""Maximum chunk size for transmitting in gRPC."""

NP_DTYPE_TO_DATATYPE = {np.int32: "INTEGER", np.float64: "DOUBLE"}
"""Dictionary of constants showing the translation between the handled numpy dtypes and the gRPC DataType enum values."""

HUMAN_SIZES = ["B", "KB", "MB", "GB", "TB"]
"""List of human-readable sizes handled."""


def human_size(content: object):
    """Method to show the size of the message in human-readable format.

    Parameters
    ----------
    content : object
        Content of the message.

    Returns
    -------
    str
        Size of the message received in human-readable format.
    """
    idx = 0
    content_length = getsizeof(content)

    while True:
        if content_length >= 1024:
            idx += 1
            content_length = floor(content_length / 1024)
        else:
            break

    if idx >= len(HUMAN_SIZES):
        raise RuntimeError("Message size above TB level... Not handled!")

    return str(content_length) + HUMAN_SIZES[idx]
