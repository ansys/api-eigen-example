"""Python script for storing common constants for both gRPC server and client"""

import numpy as np

NP_DTYPE_TO_DATATYPE = {np.int32: "INTEGER", np.float64: "DOUBLE"}
"""Dictionary of constants showing the translation between the handled numpy dtypes and the gRPC DataType enum values."""
