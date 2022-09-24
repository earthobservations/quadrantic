# """Quadrantic - Determination of quadrants based on angle, coordinates and others"""
# -*- coding: utf-8 -*-
# Copyright (C) 2022, Benjamin Gutzmann, earthobservations developers.
# Distributed under the MIT License. See LICENSE for more info.
from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Tuple, Union

from shapely.geometry import Point


class QList(list):
    """Slightly modified list to allow combination of list and Q objects
    like
        >>> [Q.FIRST, Q.SECOND] and Q.THIRD

    """

    def __and__(self, other):
        if type(other) != QList and type(other) != Q:
            raise TypeError("only Q objects and lists can be combined")

        try:
            return QList(sorted(set(self + other)))
        except TypeError:
            return QList(sorted({*self, other}))


class Q(Enum):
    """Quadrant enumeration, gets sorted after value 1 < ... < 4"""

    FIRST = 1
    SECOND = 2
    THIRD = 3
    FOURTH = 4

    def __lt__(self, other):
        return self.value < other

    def __le__(self, other):
        return self.value <= other

    def __gt__(self, other):
        return self.value > other

    def __ge__(self, other):
        return self.value >= other

    def __and__(self, other):
        return QList([self]) & other


class AngleUnit(Enum):
    """AngleUnit enumeration used for QuadrantFromAngle, especially defining full circle length"""

    DEGREE = 0
    GON = 1


class _QuadrantBase(ABC):
    @abstractmethod
    def get(self, *args, **kwargs) -> List[Q]:
        """
        Abstract method for determining the number of quadrants based on the implementation

        :param args: *args
        :param kwargs: **kwargs
        :return: list of Quadrants Q
        """
        pass


class QuadrantFromAngle(_QuadrantBase):
    """QuadrantFromAngle implementation based purely on a given angle, either in Degree or in Gon"""

    _angle_max = {AngleUnit.DEGREE: 360, AngleUnit.GON: 400}

    @staticmethod
    def _parse_unit(unit: Union[str, AngleUnit]) -> AngleUnit:
        """
        Parse AngleUnit from str or AngleUnit
        :param unit: unit given as str or AngleUnit
        :return: unit as AngleUnit
        """
        try:
            return AngleUnit(unit)
        except ValueError:
            try:
                return AngleUnit[unit.upper()]
            except KeyError as e:
                raise KeyError(f"{unit} is not a valid AngleUnit") from e

    def get(self, degree: Union[int, float], unit: Union[str, AngleUnit] = AngleUnit.DEGREE) -> List[Q]:
        """
        Determine quadrant based on degree and AngleUnit. Full circle length (Degree: 360, Gon: 400) is
        split into 4 parts and degree is normalized (between full circle length and non-negative).
        :param degree: degree given as int or float
        :param unit: unit given as str or AngleUnit
        :return: list of quadrants Q
        """
        unit = self._parse_unit(unit)
        deg_max = self._angle_max[unit]
        deg_delta = deg_max / 4

        if degree < 0:
            degree = deg_max - abs(degree) % deg_max

        degree = degree % deg_max

        if degree == 0.0:
            return Q.FIRST & Q.FOURTH
        elif degree < deg_delta:
            return [Q.FIRST]
        elif degree == deg_delta:
            return Q.FIRST & Q.SECOND
        elif degree < 2 * deg_delta:
            return [Q.SECOND]
        elif degree == 2 * deg_delta:
            return Q.SECOND & Q.THIRD
        elif degree < 3 * deg_delta:
            return [Q.THIRD]
        elif degree == 3 * deg_delta:
            return Q.THIRD & Q.FOURTH
        else:
            return [Q.FOURTH]


_POINT_TYPE = Union[Tuple[Union[int, float], Union[int, float]], Point]


class QuadrantFromCoords(_QuadrantBase):
    """QuadrantFromCoords implementation based on comparison of latlon of here and there"""

    def __init__(self, here: _POINT_TYPE):
        """

        :param here: Point that is being compared against the other location
        """
        self.here = Point(here)

    def get(self, there: _POINT_TYPE) -> List[Q]:
        """
        Determine quadrant based on latlon comparison of here and there.

        :param there: Point of other location for that the quadrant is being determined
        :return: list of quadrants Q
        """
        here = self.here
        there = Point(there)

        xdiff = there.x - here.x
        ydiff = there.y - here.y

        if xdiff == 0.0 and ydiff == 0.0:
            return Q.FIRST & Q.SECOND & Q.THIRD & Q.FOURTH
        elif xdiff > 0.0 and ydiff > 0.0:
            return [Q.FIRST]
        elif xdiff == 0.0 and ydiff > 0.0:
            return Q.FIRST & Q.SECOND
        elif xdiff < 0.0 < ydiff:
            return [Q.SECOND]
        elif xdiff < 0.0 and ydiff == 0.0:
            return Q.SECOND & Q.THIRD
        elif xdiff < 0.0 and ydiff < 0.0:
            return [Q.THIRD]
        elif xdiff == 0.0 and ydiff < 0.0:
            return Q.THIRD & Q.FOURTH
        else:
            return [Q.FOURTH]
