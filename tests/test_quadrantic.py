# """Quadrantic - Determination of quadrants based on angle, coordinates and others"""
# -*- coding: utf-8 -*-
# Copyright (C) 2022, Benjamin Gutzmann, earthobservations developers.
# Distributed under the MIT License. See LICENSE for more info.
import pytest
from shapely.geometry import Point

from quadrantic import AngleUnit, Q, QuadrantFromAngle, QuadrantFromCoords


@pytest.mark.parametrize(
    "degree,unit,expected",
    [
        # Degree
        (0.00000, AngleUnit.DEGREE, [Q.FIRST, Q.FOURTH]),
        (0.00000, "degree", [Q.FIRST, Q.FOURTH]),
        (89.99999, AngleUnit.DEGREE, [Q.FIRST]),
        (90.00000, AngleUnit.DEGREE, [Q.FIRST, Q.SECOND]),
        (95.00000, AngleUnit.DEGREE, [Q.SECOND]),
        (180.00000, AngleUnit.DEGREE, [Q.SECOND, Q.THIRD]),
        (185.00000, AngleUnit.DEGREE, [Q.THIRD]),
        (270.00000, AngleUnit.DEGREE, [Q.THIRD, Q.FOURTH]),
        (275.00000, AngleUnit.DEGREE, [Q.FOURTH]),
        (725.00000, AngleUnit.DEGREE, [Q.FIRST]),
        (900.00000, AngleUnit.DEGREE, [Q.SECOND, Q.THIRD]),
        (-45.00000, AngleUnit.DEGREE, [Q.FOURTH]),
        (-90.00000, AngleUnit.DEGREE, [Q.THIRD, Q.FOURTH]),
        (-725.00000, AngleUnit.DEGREE, [Q.FOURTH]),
        (-900.00000, AngleUnit.DEGREE, [Q.SECOND, Q.THIRD]),
        # Gon
        (0.00000, AngleUnit.GON, [Q.FIRST, Q.FOURTH]),
        (0.00000, "gon", [Q.FIRST, Q.FOURTH]),
        (99.99999, AngleUnit.GON, [Q.FIRST]),
        (100.00000, AngleUnit.GON, [Q.FIRST, Q.SECOND]),
        (105.00000, AngleUnit.GON, [Q.SECOND]),
        (200.00000, AngleUnit.GON, [Q.SECOND, Q.THIRD]),
        (205.00000, AngleUnit.GON, [Q.THIRD]),
        (300.00000, AngleUnit.GON, [Q.THIRD, Q.FOURTH]),
        (305.00000, AngleUnit.GON, [Q.FOURTH]),
        (805.00000, AngleUnit.GON, [Q.FIRST]),
        (1000.00000, AngleUnit.GON, [Q.SECOND, Q.THIRD]),
        (-50.00000, AngleUnit.GON, [Q.FOURTH]),
        (-100.00000, AngleUnit.GON, [Q.THIRD, Q.FOURTH]),
        (-805.00000, AngleUnit.GON, [Q.FOURTH]),
        (-1000.00000, AngleUnit.GON, [Q.SECOND, Q.THIRD]),
    ],
)
def test_quadrant_with_angle(degree, unit, expected):
    """Test different angles and units with QuadrantFromAngle"""
    quad = QuadrantFromAngle()
    assert quad.get(degree=degree, unit=unit) == expected


def test_quadrant_with_angle_default():
    """Test default with QuadrantFromAngle"""
    quad = QuadrantFromAngle()
    assert quad.get(degree=90.00000) == [Q.FIRST, Q.SECOND]


def test_quadrant_with_angle_unknown_unit():
    """Test unknown unit with QuadrantFromAngle"""
    quad = QuadrantFromAngle()
    with pytest.raises(KeyError) as exec_info:
        quad.get(degree=45.0, unit="abc")

    assert exec_info.value.args[0] == "abc is not a valid AngleUnit"


@pytest.mark.parametrize(
    "here,there,expected",
    [
        ((0.0, 0.0), (0.0, 0.0), [Q.FIRST, Q.SECOND, Q.THIRD, Q.FOURTH]),
        (Point(0.0, 0.0), Point(0.0, 0.0), [Q.FIRST, Q.SECOND, Q.THIRD, Q.FOURTH]),
        ((0.0, 0.0), Point(0.0, 0.0), [Q.FIRST, Q.SECOND, Q.THIRD, Q.FOURTH]),
        (Point(0.0, 0.0), (0.0, 0.0), [Q.FIRST, Q.SECOND, Q.THIRD, Q.FOURTH]),
        ((0.0, 0.0), (1.0, 1.0), [Q.FIRST]),
        (Point(0.0, 0.0), (1.0, 1.0), [Q.FIRST]),
        ((0.0, 0.0), Point(1.0, 1.0), [Q.FIRST]),
        ((0.0, 0.0), (0.0, 1.0), [Q.FIRST, Q.SECOND]),
        ((0.0, 0.0), (-1.0, 1.0), [Q.SECOND]),
        ((0.0, 0.0), (-1.0, 0.0), [Q.SECOND, Q.THIRD]),
        ((0.0, 0.0), (-1.0, -1.0), [Q.THIRD]),
        ((0.0, 0.0), (0.0, -1.0), [Q.THIRD, Q.FOURTH]),
        ((0.0, 0.0), (1.0, -1.0), [Q.FOURTH]),
    ],
)
def test_quadrant_with_coordinates(here, there, expected):
    """Test different latlons with QuadrantFromCoords"""
    quad = QuadrantFromCoords(here=here)
    assert quad.get(there=there) == expected
