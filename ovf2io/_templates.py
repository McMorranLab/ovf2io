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
