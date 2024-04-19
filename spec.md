# General

Specification can be found at:

https://math.nist.gov/oommf/doc/userguide12b4/userguide/OVF_2.0_format.html

Header and trailer.

Data block in-between - ASCII or binary.

Non-data denoted by '#'. Comment denoted by '##'.

All non-empty, non-comment lines in the header are file:value pairs.
Case is ignored, spaces and tabs are eliminated.

Format for OVF v2 is:

```
# OOMMF OVF 2.0
#
# Segment count: 1 ## Must always be 1
#
# Begin: Segment
# Begin: Header
#
# Keys : Values
# End: Header
# Begin: Data text
0.5 1.0
...
1.0 6e3
# End: Data text
# End: Segment
```

# Key : value pairs

Only those listed below are allowed. Order doesn't matter.

## Mandatory

- "title": Long file name or title.
- "meshunit": Spatial mesh unit, treated as a label. No comments allowed.
- "valueunits": units of the recorded values. List of units, either length "valuedim", or length one (will be applied to all values).
- "valuedim": dimension of the recorded values. Integer, >= 1.
- "valuelabels": list of labels for the recorded values. Length must be "valuedim", and multi-word value labels are surrounded by quotes.
- "xmin", "ymin", "zmin", "xmax", "ymax", "zmax": Six separate lines, specifying the bounding box for the mesh, in units of "meshunit".
- "meshtype": grid structure: either "rectangular" or "irregular".
  - (irregular only) "pointcount": Number of locations / data sample points. Integer.
  - (rectangular only) "xbase", "ybase", "zbase": Three separate lines, denoting the position of the first point in the data section, in units of "meshunit".
  - (rectangualr only, but allowed for irregular) "xstepsize", "ystepsize", "zstepsize": Three separate lines, the distance between adjacent grid points, in units of "meshunit".
  - (rectangular only) "xnodes", "ynodes", "znodes": Three separate lines, the number of nodes along each axis. Integer.

## Optional

- "desc": Description. May be used as many times as desired.

# Data block

Start is marked by

```
# Begin: data {representation}
```

where representation is "text", "binary 4", or "binary 8". Text mode uses ASCII. Comments allowed in text blocks, not in binary data blocks.

The binary representations are IEEE floating point in little endian order (LSB) (NOT MSB as in OVF v1.0).
To insure that the byte order is correct, and to provide a partial check that the file hasn't been sent through a non 8-bit clean channel,
the first datum is a predefined value: 1234567.0 (Hex: 38 B4 96 49) for 4-byte mode, and 123456789012345.0 (Hex: 40 DE 77 83 21 12 DC 42) for 8-byte mode.
The data immediately follow the check value.

# Data organization

## Rectangular meshes

Only the values are recorded - that is, each line will have "valuedim" entries.
They are recorded in Fortran order - x incremented first, y incremented second, z incremented third. See bottom for example.
The size of each dimension is specified by "xnodes", "ynodes", and "znodes".

For example:

```
mx(0, 0, 0) my(0, 0, 0) mz(0, 0, 0)
mx(1, 0, 0) my(0, 0, 0) mz(0, 0, 0)
mx(0, 0, 0) my(0, 1, 0) mz(0, 0, 0)
mx(1, 0, 0) my(0, 1, 0) mz(0, 0, 0)
mx(0, 0, 0) my(0, 0, 0) mz(0, 0, 1)
mx(1, 0, 0) my(0, 0, 0) mz(0, 0, 1)
mx(0, 0, 0) my(0, 1, 0) mz(0, 0, 1)
mx(1, 0, 0) my(0, 1, 0) mz(0, 0, 1)
```

## Irregular meshes

The first three columns are the x, y, and z positions. The following columns are the recorded values.

For example: 

```
0 0 0 mx(0,0,0) my(0,0,0) mz(0,0,0)
0 3 2 mx(0,3,2) my(0,3,2) mz(0,3,2)
1 0 1 mx(1,0,1) my(1,0,1) mz(1,0,1)
```