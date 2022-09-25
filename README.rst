quadrantic
##########

Determination of quadrants based on angle, coordinates and others

Overview
********

This library allows you to determine quadrant(s) based on

- angle (360° or 400 Gon)
- location (latlon)

Setup
*****

Via Pip:

.. code-block:: bash

    pip install quadrantic

Via Github (latest):

.. code-block:: bash

    pip install git+https://github.com/earthobservations/quadrantic

Implementations
***************

Get quadrant for angle
======================

Determine quadrant based on

Degree

.. code-block::

    #####################
    #         # 90°     #
    #         #         #
    # 180°    #      0° #
    #####################
    #         #         #
    #         #         #
    #         # 270°    #
    #####################

or

Gon

.. code-block::

    #####################
    #         # 100°    #
    #         #         #
    # 200°    #      0° #
    #####################
    #         #         #
    #         #         #
    #         # 300°    #
    #####################

.. code-block:: python

    from quadrantic import QuadrantFromAngle, AngleUnit, Q

    quad = QuadrantFromAngle() # no args need for this method

    # Single quadrant
    quad.get(45.0, AngleUnit.DEGREE)
    # [Q.FIRST]

    # Two quadrants
    quad.get(90.0, AngleUnit.DEGREE)
    # [Q.FIRST, Q.SECOND]

    # More then full circle (360°)
    quad.get(450.0, AngleUnit.DEGREE) # same as above + 360°
    # [Q.FIRST, Q.SECOND]

    # Negative degree
    quad.get(-45.0, AngleUnit.DEGREE)
    # [Q.FOURTH]

    # Degree in Gon
    quad.get(90.0, AngleUnit.GON)
    # [Q.FIRST]

Get quadrant for coordinates
============================

.. code-block::

    #####################
    # (-1,1)  #   (1,1) #
    #         #         #
    #         # (0,0)   #
    #####################
    #         #         #
    #         #         #
    #         #         #
    #####################

.. code-block:: python

    from quadrantic import QuadrantFromCoords, AngleUnit, Q
    from shapely.geometry import Point

    # Single quadrant
    quad = QuadrantFromCoords((0.0, 0.0))
    quad.get((1.0, 1.0))
    # [Q.FIRST]

    # Two quadrants
    quad = QuadrantFromCoords((0.0, 0.0))
    quad.get((0.0, 1.0))
    # [Q.FIRST, Q.SECOND]

    # All quadrants
    quad = QuadrantFromCoords((0.0, 0.0))
    quad.get((0.0, 0.0))
    # [Q.FIRST, Q.SECOND, Q.THIRD, Q.FOURTH]

    # Single quadrant with shapely Point
    quad = QuadrantFromCoords(Point(0.0, 0.0))
    quad.get(Point(1.0, 1.0))
    # [Q.FIRST]

Examples
********

Visualized examples can be found in the ``examples`` folder.

License
*******

Distributed under the MIT License. See ``LICENSE.rst`` for more info.

Changelog
*********

Development
===========

0.1.0 (25.09.2022)
==================

- Add first version of quadrantic
