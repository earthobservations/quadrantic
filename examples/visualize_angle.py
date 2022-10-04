# """Quadrantic - Determination of quadrants based on angle, coordinates and others"""
# -*- coding: utf-8 -*-
# Copyright (C) 2022, Benjamin Gutzmann, earthobservations developers.
# Distributed under the MIT License. See LICENSE for more info.
import random

from matplotlib.patches import Rectangle

from quadrantic import QuadrantFromAngle, AngleUnit, Q
import matplotlib.pyplot as plt

plt.style.use("ggplot")


def visualize_quadrant_from_angle(degree: float, unit: AngleUnit):
    """Example visualization from angle"""
    quad = QuadrantFromAngle()
    qs = quad.get(degree=degree, unit=unit)
    qs_string = ",".join([str(q.value) for q in qs])
    fig, ax = plt.subplots()
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    ax.text(0.9, 0, "0°")
    ax.text(0, 0.9, "90°")
    ax.text(-1, 0, "180°")
    ax.text(0, -1, "270°")

    plt.axhline(y=0, color="black")
    plt.axvline(x=0, color="black")

    for q in qs:
        if q == Q.FIRST:
            rect = Rectangle((0, 0), 1, 1, color="red")
        elif q == Q.SECOND:
            rect = Rectangle((0, 0), -1, 1, color="red")
        elif q == Q.THIRD:
            rect = Rectangle((0, 0), -1, -1, color="red")
        elif q == Q.FOURTH:
            rect = Rectangle((0, 0), 1, -1, color="red")

        ax.add_patch(rect)

    title = f"Quadrants from angle {degree}°\nVisualized Quadrant(s): {qs_string}"
    ax.set_title(title)

    plt.show()


def main():
    """Run visualize_quadrant_from_angle with config"""
    degree = random.choice(range(0, 360, 10))
    unit = AngleUnit.DEGREE

    visualize_quadrant_from_angle(degree=degree, unit=unit)


if __name__ == "__main__":
    main()
