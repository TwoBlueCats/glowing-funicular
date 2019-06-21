import typing
from functools import total_ordering


@total_ordering
class MutableWrapper(list):
    def __init__(self, init=None, seq=()):
        super().__init__(seq)
        self.__value = init

    def Get(self):
        return self.__value

    def Set(self, val):
        if not (self.__value is None) and not isinstance(val, type(self.__value)):
            raise TypeError(
                f"Bad type assignment in MutableWrapper\nOrig type {type(self.__value)}, other type {type(val)}")
        self.__value = val
        return self

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, val):
        self.Set(val)

    def Clear(self):
        del self.__value
        self.__value = None

    def __delitem__(self, key):
        self.Clear()

    def __setitem__(self, key, value):
        return self.Set(value)

    def __getitem__(self, item):
        return self.Get()

    def __str__(self):
        return f"Wrapper about type {type(self.__value)} has value {self.__value}"

    def __eq__(self, other):
        return self.__value == other

    def __lt__(self, other):
        if isinstance(other, MutableWrapper):
            other = other.Get()
        return self.__value < other

    def __getattr__(self, item):
        return self.__value.__getattribute__(item)

    def __bool__(self):
        return bool(self.value)

    def __del__(self):
        self.Clear()
