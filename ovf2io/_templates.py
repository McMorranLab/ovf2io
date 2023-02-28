# ovf2io is a utility for OOMMF Vector Field (.ovf) IO developed by WSP as a member of the McMorran Lab
# Copyright (C) 2023  William S. Parker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
rectangular_template = """# OOMMF OVF 2.0
#
# Segment count: 1
#
# Begin: Segment
# Begin: Header
#
# Title: [title]
#
[desc]
#
# meshunit: [meshunit]
#
# meshtype: rectangular
#
# xmin: [xmin]
# ymin: [ymin]
# zmin: [zmin]
# xmax: [xmax]
# ymax: [ymax]
# zmax: [zmax]
# xstepsize : [xstepsize]
# ystepsize : [ystepsize]
# zstepsize : [zstepsize]
# xbase : [xbase]
# ybase : [ybase]
# zbase : [zbase]
# xnodes : [xnodes]
# ynodes : [ynodes]
# znodes : [znodes]
#
# valuedim: [valuedim]
#
# valueunits:  [valueunits]
# valuelabels: [valuelabels]
#
# End: Header
# Begin: Data [repr]
"""

irregular_template = """# OOMMF OVF 2.0
#
# Segment count: 1
#
# Begin: Segment
# Begin: Header
#
# Title: [title]
#
[desc]
#
# meshunit: [meshunit]
#
# meshtype: irregular
#
# pointcount: [pointcount]
#
# xmin: [xmin]
# ymin: [ymin]
# zmin: [zmin]
# xmax: [xmax]
# ymax: [ymax]
# zmax: [zmax]
#
# valuedim: [valuedim]
#
# valueunits:  [valueunits]
# valuelabels: [valuelabels]
#
# End: Header
# Begin: Data [repr]
"""
