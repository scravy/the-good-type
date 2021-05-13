import re
from enum import Enum

_PATTERN = re.compile("(?P<digits>[0-9]+)(?P<unit>[A-Za-z]+)")


class Unit(Enum):
    BYTES = ('', 1)
    KIBI_BYTES = ('Ki', 1024)
    MIBI_BYTES = ('Mi', 1024 * 1024)
    GIBI_BYTES = ('Gi', 1024 * 1024 * 1024)
    TEBI_BYTES = ('Ti', 1024 * 1024 * 1024 * 1024)
    KILO_BYTES = ('K', 1000)
    MEGA_BYTES = ('M', 1000 * 1000)
    GIGA_BYTES = ('G', 1000 * 1000 * 1000)
    TERRA_BYTES = ('T', 1000 * 1000 * 1000 * 1000)

    def __init__(self, unit, factor):
        self.unit = unit
        self.factor = factor


_UNITS = {unit.unit: unit.factor for unit in Unit}


class Bytes:
    def __init__(self, value):
        if isinstance(value, int):
            self._bytes = value
            return
        try:
            self._bytes = int(value)
            return
        except ValueError:
            pass
        r = _PATTERN.match(value)
        if not r:
            raise ValueError(f"Invalid format: {value}")
        unit = r.group('unit')
        if unit not in _UNITS:
            raise ValueError(f"Unknown unit: {unit} in {value}")
        digits = r.group('digits')
        self._bytes = int(digits) * _UNITS[unit]

    def convert(self, unit: Unit) -> int:
        return self._bytes // unit.factor

    def format(self, unit: Unit) -> str:
        return f"{self.convert(unit)}{unit.unit}"
