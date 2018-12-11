# -*- coding: utf-8 -*-
# This file is part of pygal
#
# A python svg graph plotting library
# Copyright © 2012-2016 Kozea
#
# This library is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pygal. If not, see <http://www.gnu.org/licenses/>.
"""
BoxLine chart: Display values as series of boxes
"""

from __future__ import division

from math import log10

from pygal.graph.dot import Dot
from pygal.util import alter, cached_property, decorate, safe_enumerate


class BoxLine(Dot):
    """Box Line graph class"""

    def dot(self, serie, r_max):
        """Draw a box line"""
        width = (self.view.x(1) - self.view.x(0))
        serie_node = self.svg.serie(serie)
        view_values = list(map(self.view, serie.points))
        
        for i, value in safe_enumerate(serie.values):
            x, y = view_values[i]

            if self.logarithmic:
                log10min = log10(self._min) - 1
                log10max = log10(self._max or 1)

                if value != 0:
                    size = r_max * ((log10(abs(value)) - log10min) /
                                    (log10max - log10min))
                else:
                    size = 0
            else:
                size = r_max * (abs(value) / (self._max or 1))
                
            metadata = serie.metadata.get(i)
            dots = decorate(
                self.svg, self.svg.node(serie_node['plot'], class_="dots"),
                metadata
            )
            
            alter(
                self.svg.node(
                    dots,
                    'rect',
                    x=x-0.5*width,
                    y=(y-size) if value>0 else y,
                    width=width,
                    height=size,
                    class_='dot reactive tooltip-trigger' +
                    (' negative' if value < 0 else '')
                ), metadata
            )

            val = self._format(serie, i)
            self._tooltip_data(
                dots, val, x, y, '', self._get_x_label(i)
            )
            self._static_value(serie_node, val, x, y, metadata)
