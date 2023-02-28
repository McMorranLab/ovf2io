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

"""ovf2io contains utilities to read and write OOMMF Vector Field (.ovf) files. 

Examples: 

1. Read an (.ovf) file. 

```python
file_dict = ovf2io.read_ovf("file.ovf")
print(file_dict['data']['m_x']) # ndarray of m_x values
print(file_dict['coords']['x']) # 1darray of x-coords
```

2. Write an (.ovf) file, giving coordinate values.

```python
import numpy as np
X = np.linspace(0, 1, 10)
x, y, z = np.meshgrid(X, X, X, indexing='ij') # indexing='ij' to make x=axis 0, y=axis 1
f = np.cos(x)[...,np.newaxis] # shape is (10, 10, 10, 1)

ovf2io.write_ovf_rectangular(f, "file.ovf", x=X, y=Y, z=Z)
```

3. Write an (.ovf) file, giving initial point and cellsize. 
```python
import numpy as np
X = np.linspace(0, 1, 10)
x, y, z = np.meshgrid(X, X, X, indexing='ij') # indexing='ij' to make x=axis 0, y=axis 1
f = np.cos(x)[...,np.newaxis] # shape is (10, 10, 10, 1)

xmin, ymin, zmin = X[0], X[0], X[0]
dx = X[1]-X[0]
dy = X[1]-X[0]
dz = X[1]-X[0]

ovf2io.write_ovf_rectangular(f, "file.ovf", p0=(xmin, ymin, zmin), cellsize=(dx, dy, dz))
```
"""
from . import _utils as ut
import numpy as np
from pathlib import Path
from warnings import warn

__all__ = ["read_ovf",
           "write_ovf_irregular",
           "write_ovf_rectangular"]

def read_ovf(fname):
    """Returns a dictionary containing the information read from an .ovf file.
    
    The returned dictionary has three items: 

    1. `'data'`, the actual values. 
    2. `'coords'`, generated coordinates based on xmin, xstepsize, and xnodes etc. 
    3. `'metadata'`, all of the information contained in the header. 

    `'data'` contains an entry for each axis of data stored, for example <br />
    `read_ovf(fname)['data']['Zeeman energy density']` or <br />
    `read_ovf(fname)['data']['m_x']`

    `'coords'` contains coordinates generated from the header info, for example 
    `read_ovf(fname)['coords']['x']`

    If meshtype is `'rectangular'`, the shape of each `'data'` entry and each `'coords'` 
    entry will be `(xnodes, ynodes, znodes)`. If meshtype is `'irregular'`, each 
    `'data'` and `'coords'` entry will be 1-dimensional. 

    **Parameters**

    * **fname** : _str or Path_ <br />
    The filename. <br />

    **Returns**

    * **file_dict** : _dict_ <br />
    A dictionary containing the data, metadata, and generated coordinates.

    """
    fname = Path(fname)
    with open(fname, "rb") as f:
        if not b"2.0" in next(f):
            raise ValueError("This file does not appear to be OVF 2.0. "
                             "ovf2io does not support older OVF formats. ")
        # Skip ahead to the header
        while b"# begin: header" not in next(f).lower():
            pass
        header = ut._parse_header(f)
        nbytes = ut._advance_to_data_block(f)
        data = ut._parse_data(f, header, nbytes)
    coords = ut._gen_coords(data, header)
    header['repr'] = "text" if nbytes is None else f"Binary {nbytes}"
    out = {
            'data': data,
            'coords': coords,
            'metadata': header
        }
    return out

def write_ovf(data, fname, **kwargs):
    """Write data to an OOMMF Vector Field (.ovf) file. 

    Macro for `write_ovf_rectangular()` and `write_ovf_irregular`. 
    """
    warn("This function is deprecated, and is now essentially just a proxy for "
            "`write_ovf_rectangular` and `write_ovf_rectangular`. "
            "It is recommended to use either of those directly instead. ")
    if len(data.shape) == 4:
        write_ovf_rectangular(data, fname, **kwargs)
    elif len(data.shape) == 2:
        write_ovf_irregular(data, fname, **kwargs)
    else:
        raise Exception("Shape of data not recognized. Should be "
                        "(N_x, N_y, N_z, N_data_components) for rectangular meshes "
                        "or (N_points, N_data_components) for irregular meshes. ")

def write_ovf_rectangular(data, fname, p0=(0., 0., 0.,), cellsize=None,
        x=None, y=None, z=None, title="title", desc=[], meshunit="m",
        valueunits=[], valuelabels=[], representation="bin8",
    ):
    """Write data from a rectangular mesh to an OOMMF Vector Field (.ovf) file.

    **Parameters**

    * **data** : _ndarray_ <br />
    Data should have shape `(N_x, N_y, N_z, N_data_components)`. For example, 
    a vector field with 3 components, 10 samples in the x-direction, 5 samples 
    in the y-direction, and 2 samples in the z-direction would have shape (10, 5, 2, 3). 

    * **fname** : _str or Path_ <br />
    The name of the file to write. Will be overwritten if it exists already. 
    Intermediate directories are not created automatically. 

    * **p0** : _tuple, optional_ <br />
    The coordinates of the first data point, in units of `meshunit`. 
    Note these are NOT the coordinates of the edge of the bounding box. 
    Ignored when **x**, **y**, and **z** are given. <br />
    Default is `p0=(0., 0., 0.)`. 

    * **cellsize** : _tuple, optional_ <br />
    The distance between adjacent grid points, in units of `meshunit`. 
    Ignored when **x**, **y**, and **z** are given. <br />
    Default is `cellsize=(1., 1., 1.)`.

    * **x** : _ndarray, optional_ <br />
    X-coordinates, 1-dimensional array. Length must match the first axis of the data. 
    If not given, **p0** and **cellsize** will be used. 
    If given, **y** and **z** must also be given, and **p0** and **cellsize** will be ignored. 

    * **y** : _ndarray, optional_ <br />
    Y-coordinates, 1-dimensional array. Length must match the second axis of the data. 
    If not given, **p0** and **cellsize** will be used.
    If given, **x** and **z** must also be given, and **p0** and **cellsize** will be ignored. 

    * **z** : _ndarray, optional_ <br />
    Z-coordinates, 1-dimensional array. Length must match the third axis of the data. 
    If not given, **p0** and **cellsize** will be used.
    If given, **x** and **y** must also be given, and **p0** and **cellsize** will be ignored. 

    * **title** : _str, optional_ <br />
    Title to be stored in metadata. <br />
    Default is `title = "title"`.

    * **desc** : _list, optional_ <br />
    Multi-line description; each entry in the list is a separate line. 

    * **meshunit** : _str, optional_ <br />
    The unit of x, y, and z coordinates. <br />
    Default is `meshunit = "m"`.

    * **valueunits** : _list, optional_ <br />
    The units for each value stored. Length should match the number of data components, 
    or can be length 1 if all data components share the same units. If not given, 
    all data components will be given units "1". 

    * **valuelabels** : _list, optional_ <br />
    Labels for each data component. Length should match the number of data components. 
    If not given, components will be labelled "value_0", "value_1", etc.

    * **representation** : _str, optional_ <br />
    The storage mode for the data itself. One of "text", "bin4", and "bin8". 
    Comments are allowed in text mode, which uses the UTF-8 encoding. 
    Note that the original specification specifies ASCII which is a subset of UTF-8. <br />
    Default is `representation = "bin8"`. 
    """
    data = np.array(data)
    if len(data.shape) != 4:
        raise Exception("Data should have shape (N_x, N_y, N_z, N_data_components).")

    # Add a line to desc saying generated by ovf2io
    desc = ut._shape_desc(desc)
    valuedim = data.shape[-1]

    # Generate valueunits and valuelabels
    valueunits = ut._generate_valueunits_list(valueunits, valuedim)
    valuelabels = ut._generate_valuelabels_list(valuelabels, valuedim)

    if x is not None and y is not None and z is not None:
        if len(x) != data.shape[0] or len(y) != data.shape[1] or len(z) != data.shape[2]:
            raise ValueError("Coordinate dimensions incorrect; lengths of x, y, and z "
                             "should match the data's first, second, and third axes, respectively. ")
        p0 = (x[0], y[0], z[0])
        cellsize = (np.abs(x[1]-x[0]), np.abs(y[1]-y[0]), np.abs(z[1]-z[0]))
    elif x is not None or y is not None or z is not None:
        raise Exception("x, y, and z should all be given or none given.")
    # If no x/y/z, but also no cellsize
    elif cellsize is None:
        cellsize = (1., 1., 1.)
        meshunit = "pt"
    header = {
        "title": title, "desc": desc, "meshunit": meshunit, "meshtype": "rectangular",
        "valueunits": valueunits, "valuelabels": valuelabels, "valuedim": valuedim,
        "xbase": p0[0], "ybase": p0[1], "zbase": p0[2], 
        "xstepsize": cellsize[0], "ystepsize": cellsize[1], "zstepsize": cellsize[2],
        "xnodes": data.shape[0], "ynodes": data.shape[1], "znodes": data.shape[2],
        "xmin": p0[0] - 0.5 * cellsize[0], "xmax": p0[0] + (data.shape[0] - 0.5) * cellsize[0],
        "ymin": p0[1] - 0.5 * cellsize[1], "ymax": p0[1] + (data.shape[1] - 0.5) * cellsize[1],
        "zmin": p0[2] - 0.5 * cellsize[2], "zmax": p0[2] + (data.shape[2] - 0.5) * cellsize[2]
    }
    if not representation.lower() in {"text", "bin4", "bin8"}:
        raise ValueError("Representation must be either 'text', 'bin4', or 'bin8'.")
    reshaped = data.reshape((-1, data.shape[-1]), order='F')
    frontmatter = ut._make_header(header, representation)
    ut._write_file(fname, frontmatter, representation, reshaped)

def write_ovf_irregular(data, fname, points=None, cellsize=(0., 0., 0.),
        title="title", desc=[], meshunit="m", 
        valueunits=[], valuelabels=[], representation="bin8"
    ):
    """Write data from an irregular mesh to an OOMMF Vector Field (.ovf) file. 

    **Parameters**

    * **data** : _ndarray_ <br />
    The data to be written. Should have shape `(N_points, N_data_components)`. 

    * **fname** : _str or Path_ <br />
    The name of the file to write. Will be overwritten if it exists already. 
    Intermediate directories are not created automatically. 

    * **points** : _ndarray, optional_ <br />
    Coordinates of the mesh. Should have shape `(N_points, 3)`. If not given, 
    x will be used as an index for the data entries. 

    * **cellsize** : _tuple, optional_ <br />
    Tuple specifying the spacing between grid points, which is used by some programs 
    as a display hint.

    * **title** : _str, optional_ <br />
    Title to be stored in metadata. <br />
    Default is `title = "title"`.

    * **desc** : _list, optional_ <br />
    Multi-line description; each line should be a separate entry in the list. 

    * **meshunit** : _str, optional_ <br />
    The unit of x, y, and z coordinates. <br />
    Default is `meshunit = "m"`.

    * **valueunits** : _list, optional_ <br />
    The units for each value stored. Length should match the number of data components, 
    or can be length 1 if all data components share the same units. If not given, 
    all data components will be given units "1". 

    * **valuelabels** : _list, optional_ <br />
    Labels for each data component. Length should match the number of data components. 
    If not given, components will be labelled "value_0", "value_1", etc.

    * **representation** : _str, optional_ <br />
    The storage mode for the data itself. One of "text", "bin4", and "bin8". 
    Comments are allowed in text mode, which uses the UTF-8 encoding. 
    Note that the original specification specifies ASCII which is a subset of UTF-8. <br />
    Default is `representation = "bin8"`. 
    """
    data = np.array(data)
    if len(data.shape) != 2:
        raise Exception("Data should have shape (N_points, N_data_components).")

    # Add a line to desc saying generated by ovf2io
    desc = ut._shape_desc(desc)
    valuedim = data.shape[-1]
    valueunits = ut._generate_valueunits_list(valueunits, valuedim)
    valuelabels = ut._generate_valuelabels_list(valuelabels, valuedim)

    if points is None:
        points = np.array([[i, 0., 0.] for i in range(data.shape[0])])
        cellsize = (1., 1., 1.)
        meshunit = "pt"

    header = {
        "title": title, "desc": desc, "meshunit": meshunit, "meshtype": "irregular",
        "valueunits": valueunits, "valuelabels": valuelabels, "valuedim": valuedim,
        "pointcount": data.shape[0],
        "xmin": np.min(points[:,0]) - 0.5 * cellsize[0], "xmax": np.max(points[:,0]) + 0.5 * cellsize[0],
        "ymin": np.min(points[:,1]) - 0.5 * cellsize[1], "ymax": np.max(points[:,1]) + 0.5 * cellsize[1],
        "zmin": np.min(points[:,2]) - 0.5 * cellsize[2], "zmax": np.max(points[:,2]) + 0.5 * cellsize[2],
    }
    if not representation.lower() in {"text", "bin4", "bin8"}:
        raise ValueError("Representation must be either 'text', 'bin4', or 'bin8'.")
    reshaped = np.zeros((data.shape[0], data.shape[1] + 3))
    reshaped[:, :3] = points
    reshaped[:, 3:] = data
    frontmatter = ut._make_header(header, representation)
    ut._write_file(fname, frontmatter, representation, reshaped)
