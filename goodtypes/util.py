import datetime
from numbers import Number

from typing import Callable, Iterator, TypeVar, Optional, Union, Type

E = TypeVar('E')


def _range(lower: E, step: Callable[[E], E], condition: Callable[[E], bool]) -> Iterator[E]:
    """
    Very generic range function. Yields a stream from lower, incremented by the given step-function,
    until the given condition is reached.

    spec: takeWhile predicate (iterate step seed)
    """
    current = lower
    while condition(current):
        yield current
        current = step(current)


def _get_incrementor(type_: Type[E], step: Number = 1) -> Callable[[E], E]:
    """
    Returns a function that increments values of the given type by the given step.

    ...basically `(+ 1)` (or `(+ step)` respectively), but can increment other types as well. Currently
    the only other type supported is datetime.date which is incremented in days.
    """
    if issubclass(type_, datetime.date):
        # noinspection PyTypeChecker
        return lambda value: value + datetime.timedelta(days=step)
    return lambda value: value + step


def range_excl(lower: E, upper: E, step: Optional[Union[Callable[[E], E], Number]] = None) -> Iterator[E]:
    if step is None:
        step = _get_incrementor(type(lower))
    elif isinstance(step, Number):
        step = _get_incrementor(type(lower), step)
    yield from _range(lower, step, lambda value: value < upper)


def range_incl(lower: E, upper: E, step: Optional[Union[Callable[[E], E], Number]] = None) -> Iterator[E]:
    if step is None:
        step = _get_incrementor(type(lower))
    elif isinstance(step, Number):
        step = _get_incrementor(type(lower), step)
    yield from _range(lower, step, lambda value: value <= upper)
