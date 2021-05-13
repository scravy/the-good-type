from __future__ import annotations

import datetime
import itertools
from typing import List, Tuple, Optional, Iterator, Union

from .util import range_incl

Date = Union[str, datetime.date]


def read_date(v: Union[datetime.date, str]) -> datetime.date:
    if isinstance(v, datetime.date):
        return v
    if isinstance(v, str):
        return datetime.date.fromisoformat(v)
    raise ValueError


def end_of_month(d: Date) -> datetime.date:
    d = read_date(d)
    next_month = d.month % 12 + 1
    next_year = d.year + (1 if next_month == 1 else 0)
    return datetime.date(next_year, next_month, 1) - datetime.timedelta(days=1)


class DateRange:

    @staticmethod
    def _date_or_begin_of_month(v: str) -> datetime.date:
        components = v.split('-')
        if len(components) == 2:
            year, month = components
            return datetime.date(int(year), int(month), 1)
        else:
            return datetime.date.fromisoformat(v)

    @staticmethod
    def _date_or_end_of_month(v: str) -> datetime.date:
        components = v.split('-')
        if len(components) == 2:
            year, month = components
            d: datetime.date = datetime.date(int(year), int(month), 1)
            return end_of_month(d)
        else:
            return datetime.date.fromisoformat(v)

    def __init__(self, date_range: str):
        self._subranges: List[Tuple[Optional[datetime.date], Optional[datetime.date]]] = []
        components = date_range.translate(str.maketrans('', '', ' ')).split(',')
        for component in components:
            range_components = component.split('..')
            if len(range_components) == 1:
                parts = component.split('-')
                if len(parts) == 2:
                    year, month = parts
                    year = int(year)
                    month = int(month)
                    lower: datetime.date = datetime.date(year, month, 1)
                    upper = end_of_month(lower)
                    self._subranges.append((lower, upper))
                else:
                    d = datetime.date.fromisoformat(component)
                    self._subranges.append((d, d))
            elif len(range_components) == 2:
                d1 = range_components[0] and self._date_or_begin_of_month(range_components[0]) or None
                d2 = range_components[1] and self._date_or_end_of_month(range_components[1]) or None
                self._subranges.append((d1, d2))

    def __contains__(self, item: Date) -> bool:
        d = read_date(item)
        for d1, d2 in self._subranges:
            if d1 and d2:
                if d1 <= d <= d2:
                    return True
            elif d1:
                if d1 <= d:
                    return True
            else:
                if d <= d2:
                    return True
        return False

    def __eq__(self, other):
        if isinstance(other, datetime.date):
            return self._cmp(other) == 0
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, datetime.date):
            return self._cmp(other) <= 0
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, datetime.date):
            return self._cmp(other) < 0
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, datetime.date):
            return self._cmp(other) >= 0
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, datetime.date):
            return self._cmp(other) > 0
        return NotImplemented

    def _cmp(self, other: datetime.date):
        max_ = self.max
        if max_ is not None and max_ < other:  # pylint: disable=E0601
            return -1
        min_ = self.min
        if min_ is not None and min_ > other:  # pylint: disable=E0601
            return 1
        return 0

    @property
    def min(self) -> Optional[datetime.date]:
        if any(lower is None for lower, _ in self._subranges):
            return None
        return min(lower for lower, _ in self._subranges)

    @property
    def max(self) -> Optional[datetime.date]:
        if any(upper is None for _, upper in self._subranges):
            return None
        return max(upper for _, upper in self._subranges)

    def iter(self, lower: Optional[Date] = None, upper: Optional[Date] = None) -> Iterator[datetime.date]:
        lower = lower and read_date(lower) or self.min or None
        upper = upper and read_date(upper) or self.max or None

        if not lower or not upper:
            raise ValueError('no lower or upper bound')

        for d in range_incl(lower, upper):
            if d in self:
                yield d

    def itermonths(self) -> Iterator[DateRange]:
        for _key, group in itertools.groupby(iter(self), lambda d: d.month):
            yield DateRange(','.join(sorted(str(d) for d in group)))

    def __iter__(self) -> Iterator[datetime.date]:
        min_ = self.min
        max_ = self.max
        if min_ is None or max_ is None:
            raise ValueError("open range")
        yield from self.iter(min_, max_)

    def _subranges_str(self) -> Iterator[str]:
        for lower, upper in self._subranges:
            if lower is None:
                yield f"..{upper}"
            elif upper is None:
                yield f"{lower}.."
            elif lower == upper:
                yield f"{lower}"
            else:
                yield f"{lower}..{upper}"

    def __str__(self) -> str:
        return ','.join(self._subranges_str())
