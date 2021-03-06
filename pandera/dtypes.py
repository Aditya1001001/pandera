"""Schema datatypes."""

from enum import Enum
from typing import Union

import numpy as np
import pandas as pd


# pylint: disable=invalid-name
try:
    PandasExtensionType = pd.core.dtypes.base.ExtensionDtype
except AttributeError:
    PandasExtensionType = "pd.core.dtypes.base.ExtensionDtype"


NUMPY_NONNULLABLE_INT_DTYPES = [
    "int", "int_", "int8", "int16", "int32", "int64",
    "uint8", "uint16", "uint32", "uint64",
]

# for int and float dtype, delegate string representation to the
# default based on OS. In Windows, pandas defaults to int64 while numpy
# defaults to int32.
_DEFAULT_PANDAS_INT_TYPE = str(pd.Series([1]).dtype)
_DEFAULT_PANDAS_FLOAT_TYPE = str(pd.Series([1.]).dtype)
_DEFAULT_NUMPY_INT_TYPE = str(np.dtype(int))
_DEFAULT_NUMPY_FLOAT_TYPE = str(np.dtype(float))


class PandasDtype(Enum):
    # pylint: disable=line-too-long
    """Enumerate all valid pandas data types.

    ``pandera`` follows the
    `numpy data types <https://docs.scipy.org/doc/numpy/reference/arrays.dtypes.html#arrays-dtypes>`_
    subscribed to by ``pandas`` and by default supports using the numpy data
    type string aliases to validate DataFrame or Series dtypes.

    This class simply enumerates the valid numpy dtypes for pandas arrays.
    For convenience ``PandasDtype`` enums can all be accessed in the top-level
    ``pandera`` name space via the same enum name.

    :examples:

    >>> import pandas as pd
    >>> import pandera as pa
    >>>
    >>>
    >>> pa.SeriesSchema(pa.Int).validate(pd.Series([1, 2, 3]))
    0    1
    1    2
    2    3
    dtype: int64
    >>> pa.SeriesSchema(pa.Float).validate(pd.Series([1.1, 2.3, 3.4]))
    0    1.1
    1    2.3
    2    3.4
    dtype: float64
    >>> pa.SeriesSchema(pa.String).validate(pd.Series(["a", "b", "c"]))
        0    a
    1    b
    2    c
    dtype: object

    You can also directly use the string alias for each data-type in the
    schema definition:

    >>> pa.SeriesSchema("int").validate(pd.Series([1, 2, 3]))
    0    1
    1    2
    2    3
    dtype: int64

    .. note::
        ``pandera`` also offers limited support for
        `pandas extension types <https://pandas.pydata.org/pandas-docs/stable/getting_started/basics.html#dtypes>`_,
        however since the release of pandas 1.0.0 there are backwards
        incompatible extension types like the ``String`` array. The extension
        types, e.g. ``pd.StringDtype()`` and their string aliases should work
        when supplied to the ``pandas_dtype`` argument when initializing
        ``pa.SeriesSchemaBase`` objects, but this functionality is only
        tested for pandas >= 1.0.0. Extension types in earlier versions are
        not guaranteed to work as the ``pandas_dtype`` argument in schemas
        or schema components.

    """

    Bool = "bool"  #: ``"bool"`` numpy dtype
    DateTime = "datetime64[ns]"  #: ``"datetime64[ns]"`` numpy dtype
    Timedelta = "timedelta64[ns]"  #: ``"timedelta64[ns]"`` numpy dtype
    Category = "category"  #: pandas ``"categorical"`` datatype
    Float = "float"  #: ``"float"`` numpy dtype
    Float16 = "float16"  #: ``"float16"`` numpy dtype
    Float32 = "float32"  #: ``"float32"`` numpy dtype
    Float64 = "float64"  #: ``"float64"`` numpy dtype
    Int = "int"  #: ``"int"`` numpy dtype
    Int8 = "int8"  #: ``"int8"`` numpy dtype
    Int16 = "int16"  #: ``"int16"`` numpy dtype
    Int32 = "int32"  #: ``"int32"`` numpy dtype
    Int64 = "int64"  #: ``"int64"`` numpy dtype
    UInt8 = "uint8"  #: ``"uint8"`` numpy dtype
    UInt16 = "uint16"  #: ``"uint16"`` numpy dtype
    UInt32 = "uint32"  #: ``"uint32"`` numpy dtype
    UInt64 = "uint64"  #: ``"uint64"`` numpy dtype
    Object = "object"  #: ``"object"`` numpy dtype

    #: The string datatype doesn't map to a first-class pandas datatype and is
    #: representated as a numpy ``"object"`` array. This will change after
    #: pandera explicitly supports pandas 1.0+ and is currently handled
    #: internally by pandera as a special case.
    String = "string"

    @property
    def str_alias(self):
        """Get datatype string alias."""
        return {
            "int": _DEFAULT_PANDAS_INT_TYPE,
            "float": _DEFAULT_PANDAS_FLOAT_TYPE,
            "string": "object",
        }.get(self.value, self.value)

    @classmethod
    def from_str_alias(cls, str_alias: str) -> Union["PandasDtype", None]:
        """Get PandasDtype from string alias.

        :param: pandas dtype string alias from
            https://pandas.pydata.org/pandas-docs/stable/getting_started/basics.html#basics-dtypes
        :returns: pandas dtype
        """
        return {
            "bool": cls.Bool,
            "datetime64[ns]": cls.DateTime,
            "timedelta64[ns]": cls.Timedelta,
            "category": cls.Category,
            "float": cls.Float,
            "float16": cls.Float16,
            "float32": cls.Float32,
            "float64": cls.Float64,
            "int": cls.Int,
            "int8": cls.Int8,
            "int16": cls.Int16,
            "int32": cls.Int32,
            "int64": cls.Int64,
            "uint8": cls.UInt8,
            "uint16": cls.UInt16,
            "uint32": cls.UInt32,
            "uint64": cls.UInt64,
            "object": cls.Object,
            "string": cls.String,
        }.get(str_alias)

    @classmethod
    def from_pandas_api_type(
            cls, pandas_api_type: str) -> Union["PandasDtype", None]:
        """Get PandasDtype enum from pandas api type.

        :param pandas_api_type: string output from
            https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.api.types.infer_dtype.html
        :returns: pandas dtype
        """
        if pandas_api_type.startswith("mixed"):
            return cls.Object

        return {
            "string": cls.String,
            "floating": cls.Float,
            "integer": cls.Int,
            "categorical": cls.Category,
            "boolean": cls.Bool,
            "datetime64": cls.DateTime,
            "datetime": cls.DateTime,
            "timedelta64": cls.Timedelta,
            "timedelta": cls.Timedelta,
        }.get(pandas_api_type)

    def __eq__(self, other):
        # pylint: disable=comparison-with-callable,too-many-return-statements
        # see https://github.com/PyCQA/pylint/issues/2306
        if other is None:
            return False
        elif self.value == "string":
            return self.value == other.value
        return self.str_alias == other.str_alias

    def __hash__(self):
        if self is PandasDtype.Int:
            hash_obj = _DEFAULT_PANDAS_INT_TYPE
        elif self is PandasDtype.Float:
            hash_obj = _DEFAULT_PANDAS_FLOAT_TYPE
        else:
            hash_obj = self.str_alias
        return id(hash_obj)
