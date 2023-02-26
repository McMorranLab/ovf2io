import numpy as np

irregular_header = """# OOMMF OVF 2.0
#
# Segment count: 1
#
# Begin: Segment
# Begin: Header
#
# Title: Long file name or title goes here ## and a comment
#
# Desc: Optional description line 1.
# Desc: Optional description line 2.
# Desc: ...
#
## Fundamental mesh measurement unit.  Treated as a label:
# meshunit: nm
#
# meshtype: irregular
# pointcount: 5      ## Number of nodes in mesh
#
# xmin:    1.    ## Corner points defining mesh bounding box in
# ymin:    6.    ## 'meshunit'.  Floating point values.
# zmin:    11.
# xmax:   5.
# ymax:    10.
# zmax:    15.
#
# valuedim: 2    ## Value dimension
#
## Fundamental field value units, treated as labels (i.e., unparsed).
## In general, there should be one label for each value dimension.
# valueunits:  J/m^3  A/m
# valuelabels: "Zeeman energy density"  "Anisotropy field"
#
# End: Header
#
## Each data records consists of N+3 values: the (x,y,z) node
## location, followed by the N value components.  In this example,
## N+3 = 5, the two value components are in units of J/m^3 and A/m,
## corresponding to Zeeman energy density and a magneto-crystalline
## anisotropy field, respectively.
#"""

rectangular_header = """# OOMMF OVF 2.0
#
# Segment count: 1
#
# Begin: Segment
# Begin: Header
#
# Title: Long file name or title goes here ## and a comment
#
# Desc: Optional description line 1.
# Desc: Optional description line 2.
# Desc: ...
#
## Fundamental mesh measurement unit.  Treated as a label:
# meshunit: m
#
# meshtype: rectangular
#
# xmin:    -0.5    ## Corner points defining mesh bounding box in
# ymin:    -0.5    ## 'meshunit'.  Floating point values.
# zmin:    -0.5
# xmax:   1.5
# ymax:    1.5
# zmax:    1.5
# xstepsize : 1
# ystepsize : 1
# zstepsize : 1
# xbase : 0.0
# ybase : 0.0
# zbase : 0.0
# xnodes : 2
# ynodes : 3
# znodes : 4
#
# valuedim: 3    ## Value dimension
#
## Fundamental field value units, treated as labels (i.e., unparsed).
## In general, there should be one label for each value dimension.
# valueunits:  m
# valuelabels: "x_value"  "y_value" "z_value"
#
# End: Header
#"""

irregular_values = np.array([
    1.0, 6.0, 11.0, 500., 4e4,
    2.0, 7.0, 12.0, 600., 5e4,
    3.0, 8.0, 13.0, 700., 6e4,
    4.0, 9.0, 14.0, 800., 7e4,
    5.0, 10.0, 15.0, 900., 8e4,
    ])

irregular_values_text = """1.0 6.0 11.0 500. 4e4
2.0 7.0 12.0 600. 5e4
3.0 8.0 13.0 700. 6e4
4.0 9.0 14.0 800. 7e4
5.0 10.0 15.0 900. 8e4"""

rectangular_values = np.array([
0, 0, 0,
1, 0, 0,
0, 1, 0,
1, 1, 0,
0, 2, 0,
1, 2, 0,
0, 0, 1,
1, 0, 1,
0, 1, 1,
1, 1, 1,
0, 2, 1,
1, 2, 1,
0, 0, 2,
1, 0, 2,
0, 1, 2,
1, 1, 2,
0, 2, 2,
1, 2, 2,
0, 0, 3,
1, 0, 3,
0, 1, 3,
1, 1, 3,
0, 2, 3,
1, 2, 3,
    ])

rectangular_values_text = """0 0 0
1 0 0
0 1 0
1 1 0
0 2 0
1 2 0
0 0 1
1 0 1
0 1 1
1 1 1
0 2 1
1 2 1
0 0 2
1 0 2
0 1 2
1 1 2
0 2 2
1 2 2
0 0 3
1 0 3
0 1 3
1 1 3
0 2 3
1 2 3"""

# Irregular Text
with open("test_ovfs/text_irregular.ovf", "w") as f:
    f.write(irregular_header)
    f.write("# Begin: data text\n")
    f.write(irregular_values_text)
    f.write("\n")
    f.write("# End: data text\n# End: Segment")

# Irregular Bin 8
with open("test_ovfs/bin8_irregular.ovf", "w") as f:
    f.write(irregular_header)
    f.write("\n")
    f.write("# Begin: data binary 8\n")
with open("test_ovfs/bin8_irregular.ovf", "ab") as f:
    f.write(irregular_values.astype("<d").tobytes())
with open("test_ovfs/bin8_irregular.ovf", "a") as f:
    f.write("\n# End: data binary 8\n# End: Segment")

# Irregular Bin 4
with open("test_ovfs/bin4_irregular.ovf", "w") as f:
    f.write(irregular_header)
    f.write("\n")
    f.write("# Begin: data binary 4\n")
with open("test_ovfs/bin4_irregular.ovf", "ab") as f:
    f.write(irregular_values.astype("<f").tobytes())
with open("test_ovfs/bin4_irregular.ovf", "a") as f:
    f.write("\n# End: data binary 4\n# End: Segment")

# Rectangular Text
with open("test_ovfs/text_rectangular.ovf", "w") as f:
    f.write(rectangular_header)
    f.write("# Begin: data text\n")
    f.write(rectangular_values_text)
    f.write("\n")
    f.write("# End: data text\n# End: Segment")

# Rectangular Bin 8
with open("test_ovfs/bin8_rectangular.ovf", "w") as f:
    f.write(rectangular_header)
    f.write("\n")
    f.write("# Begin: data binary 8\n")
with open("test_ovfs/bin8_rectangular.ovf", "ab") as f:
    f.write(rectangular_values.astype("<d").tobytes())
with open("test_ovfs/bin8_rectangular.ovf", "a") as f:
    f.write("\n# End: data binary 8\n# End: Segment")

# Rectangular Bin 4
with open("test_ovfs/bin4_rectangular.ovf", "w") as f:
    f.write(rectangular_header)
    f.write("\n")
    f.write("# Begin: data binary 4\n")
with open("test_ovfs/bin4_rectangular.ovf", "ab") as f:
    f.write(rectangular_values.astype("<f").tobytes())
with open("test_ovfs/bin4_rectangular.ovf", "a") as f:
    f.write("\n# End: data binary 4\n# End: Segment")
