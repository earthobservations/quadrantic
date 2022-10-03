# """Quadrantic - Determination of quadrants based on angle, coordinates and others"""
# -*- coding: utf-8 -*-
# Copyright (C) 2022, Benjamin Gutzmann, earthobservations developers.
# Distributed under the MIT License. See LICENSE for more info.
import matplotlib.pyplot as plt
from wetterdienst import Parameter
from wetterdienst.provider.dwd.observation import DwdObservationRequest
from quadrantic import QuadrantFromCoords
from collections import Counter

plt.style.use("ggplot")


def visualize_wd_station_distribution(parameter, latitude, longitude, distance):
    """Example visualization of german weather stations in quadrants"""

    def _get_axis_quarters():
        xlim = plt.gca().get_xlim()
        xdiff = xlim[1] - xlim[0]
        ylim = plt.gca().get_ylim()
        ydiff = ylim[1] - ylim[0]

        xfirst, xthird = xlim[0] + 1 / 4 * xdiff, xlim[0] + 3 / 4 * xdiff
        yfirst, ythird = ylim[0] + 1 / 4 * ydiff, ylim[0] + 3 / 4 * ydiff

        return (xthird, ythird), (xfirst, ythird), (xfirst, yfirst), (xthird, yfirst)

    qfc = QuadrantFromCoords((longitude, latitude))
    stations = DwdObservationRequest(parameter, "daily").filter_by_distance(latitude, longitude, distance)
    quadrant_counter = Counter()
    stations.df[["latitude", "longitude"]].apply(lambda row: qfc.get((row[1], row[0])), axis=1).apply(
        lambda quadrants: quadrant_counter.update([q.value for q in quadrants])
    )

    fig, ax = plt.subplots()

    stations.df.plot("longitude", "latitude", kind="scatter", ax=ax)

    ax.axhline(y=latitude, color="black")
    ax.axvline(x=longitude, color="black")

    for quadrant, (x, y) in zip((1, 2, 3, 4), _get_axis_quarters()):
        qcounts = quadrant_counter.get(quadrant, 0)
        ax.text(x, y, str(qcounts), color="red", size=20)

    title = f"Quadrant counts of german weather stations"
    ax.set_title(title)
    ax.set_xlabel("longitude [°]")
    ax.set_ylabel("latitude [°]")

    plt.show()


def main():
    """Run visualize_quadrant_from_angle with config"""
    parameter = Parameter.TEMPERATURE_AIR_MEAN_200
    latitude = 50.0
    longitude = 8.9
    distance = 40.0

    visualize_wd_station_distribution(parameter, latitude, longitude, distance)


if __name__ == "__main__":
    main()
