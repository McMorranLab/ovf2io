import numpy as np
import ovf2io as ovf
import discretisedfield as df
from pathlib import Path

X = np.arange(0, 2)
Y = np.arange(0, 3)
Z = np.arange(0, 4)
x, y, z = np.meshgrid(X, Y, Z, indexing='ij')
rect_data = np.einsum('i...->...i', np.array([x, y, z]))
irreg_data = np.array([[i, j, k] for k in range(4) for j in range(3) for i in range(2)])
p0 = (X[0], Y[0], Z[0])
cellsize = (X[1]-X[0], Y[1]-Y[0], Z[1]-Z[0])

############ BINARY 4 ########################

###### Rectangular
def test_rect_bin4xyz():
    fname = "test_rect_bin4xyz.ovf"
    fname = Path("writing_tests").joinpath(fname)
    ovf.write_ovf_rectangular(rect_data, fname, x=X, y=Y, z=Z, representation="bin4")
    field = df.Field.fromfile(fname)
    assert(np.allclose(field.value, rect_data))
    assert(np.allclose(field.mesh.midpoints.x, X))

def test_rect_bin4p0cell():
    fname = "test_rect_bin4p0cell.ovf"
    fname = Path("writing_tests").joinpath(fname)
    ovf.write_ovf_rectangular(rect_data, fname, p0=p0, cellsize=cellsize, representation="bin4")
    field = df.Field.fromfile(fname)
    assert(np.allclose(field.value, rect_data))
    assert(np.allclose(field.mesh.midpoints.x, X))

def test_rect_bin4_defaults():
    fname = "test_rect_bin4_defaults.ovf"
    fname = Path("writing_tests").joinpath(fname)
    ovf.write_ovf_rectangular(rect_data, fname, representation="bin4")
    field = df.Field.fromfile(fname)
    assert(np.allclose(field.value, rect_data))
    assert(np.allclose(field.mesh.midpoints.x, X))

####### Irregular
def test_irreg_bin4_defaults():
    fname = "test_irreg_bin4_defaults.ovf"
    fname = Path("writing_tests").joinpath(fname)
    ovf.write_ovf_irregular(irreg_data, fname, representation="bin4")
    data = ovf.read_ovf(fname)
    assert(np.allclose(data['data']['value_0'], irreg_data[:,0]))
    assert(np.allclose(data['coords']['x'], np.arange(len(irreg_data))))

def test_irreg_bin4_points_given():
    fname = "test_irreg_bin4_points_given.ovf"
    fname = Path("writing_tests").joinpath(fname)
    ovf.write_ovf_irregular(irreg_data, fname, points=irreg_data, representation="bin4")
    data = ovf.read_ovf(fname)
    assert(np.allclose(data['data']['value_0'], irreg_data[:,0]))
    assert(np.allclose(data['coords']['x'], irreg_data[:,0]))

############ BINARY 8 ########################

###### Rectangular
def test_rect_bin8xyz():
    fname = "test_rect_bin8xyz.ovf"
    fname = Path("writing_tests").joinpath(fname)
    ovf.write_ovf_rectangular(rect_data, fname, x=X, y=Y, z=Z, representation="bin8")
    field = df.Field.fromfile(fname)
    assert(np.allclose(field.value, rect_data))
    assert(np.allclose(field.mesh.midpoints.x, X))

def test_rect_bin8p0cell():
    fname = "test_rect_bin8p0cell.ovf"
    fname = Path("writing_tests").joinpath(fname)
    ovf.write_ovf_rectangular(rect_data, fname, p0=p0, cellsize=cellsize, representation="bin8")
    field = df.Field.fromfile(fname)
    assert(np.allclose(field.value, rect_data))
    assert(np.allclose(field.mesh.midpoints.x, X))

def test_rect_bin8_defaults():
    fname = "test_rect_bin8_defaults.ovf"
    fname = Path("writing_tests").joinpath(fname)
    ovf.write_ovf_rectangular(rect_data, fname, representation="bin8")
    field = df.Field.fromfile(fname)
    assert(np.allclose(field.value, rect_data))
    assert(np.allclose(field.mesh.midpoints.x, X))

####### Irregular
def test_irreg_bin8_defaults():
    fname = "test_irreg_bin8_defaults.ovf"
    fname = Path("writing_tests").joinpath(fname)
    ovf.write_ovf_irregular(irreg_data, fname, representation="bin8")
    data = ovf.read_ovf(fname)
    assert(np.allclose(data['data']['value_0'], irreg_data[:,0]))
    assert(np.allclose(data['coords']['x'], np.arange(len(irreg_data))))

def test_irreg_bin8_points_given():
    fname = "test_irreg_bin8_points_given.ovf"
    fname = Path("writing_tests").joinpath(fname)
    ovf.write_ovf_irregular(irreg_data, fname, points=irreg_data, representation="bin8")
    data = ovf.read_ovf(fname)
    assert(np.allclose(data['data']['value_0'], irreg_data[:,0]))
    assert(np.allclose(data['coords']['x'], irreg_data[:,0]))

############ TEXT ########################

###### Rectangular
def test_rect_textxyz():
    fname = "test_rect_textxyz.ovf"
    fname = Path("writing_tests").joinpath(fname)
    ovf.write_ovf_rectangular(rect_data, fname, x=X, y=Y, z=Z, representation="text")
    field = df.Field.fromfile(fname)
    assert(np.allclose(field.value, rect_data))
    assert(np.allclose(field.mesh.midpoints.x, X))

def test_rect_textp0cell():
    fname = "test_rect_textp0cell.ovf"
    fname = Path("writing_tests").joinpath(fname)
    ovf.write_ovf_rectangular(rect_data, fname, p0=p0, cellsize=cellsize, representation="text")
    field = df.Field.fromfile(fname)
    assert(np.allclose(field.value, rect_data))
    assert(np.allclose(field.mesh.midpoints.x, X))

def test_rect_text_defaults():
    fname = "test_rect_text_defaults.ovf"
    fname = Path("writing_tests").joinpath(fname)
    ovf.write_ovf_rectangular(rect_data, fname, representation="text")
    field = df.Field.fromfile(fname)
    assert(np.allclose(field.value, rect_data))
    assert(np.allclose(field.mesh.midpoints.x, X))

####### Irregular
def test_irreg_text_defaults():
    fname = "test_irreg_text_defaults.ovf"
    fname = Path("writing_tests").joinpath(fname)
    ovf.write_ovf_irregular(irreg_data, fname, representation="text")
    data = ovf.read_ovf(fname)
    assert(np.allclose(data['data']['value_0'], irreg_data[:,0]))
    assert(np.allclose(data['coords']['x'], np.arange(len(irreg_data))))

def test_irreg_text_points_given():
    fname = "test_irreg_text_points_given.ovf"
    fname = Path("writing_tests").joinpath(fname)
    ovf.write_ovf_irregular(irreg_data, fname, points=irreg_data, representation="text")
    data = ovf.read_ovf(fname)
    assert(np.allclose(data['data']['value_0'], irreg_data[:,0]))
    assert(np.allclose(data['coords']['x'], irreg_data[:,0]))

