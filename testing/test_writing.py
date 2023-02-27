import numpy as np
import ovf2io as ovf
import discretisedfield as df

X = np.arange(0, 2)
Y = np.arange(0, 3)
Z = np.arange(0, 4)
x, y, z = np.meshgrid(X, Y, Z, indexing='ij')
rect_data = np.einsum('i...->...i', np.array([x, y, z]))
irreg_data = np.array([[i, j] for j in range(3) for i in range(2)])

def test_rect_bin4():
    fname = "writing_tests/rect_bin4.ovf"
    ovf.write_ovf(rect_data, fname, representation="bin4")
    field = df.Field.fromfile("writing_tests/rect_bin4.ovf")
    assert(np.allclose(field.value, rect_data))

def test_rect_bin8():
    ovf.write_ovf(rect_data, "writing_tests/rect_bin8.ovf", representation="bin8")
    field = df.Field.fromfile("writing_tests/rect_bin8.ovf")
    assert(np.allclose(field.value, rect_data))

def test_rect_text():
    ovf.write_ovf(rect_data, "writing_tests/rect_text.ovf", representation="text")
    field = df.Field.fromfile("writing_tests/rect_text.ovf")
    assert(np.allclose(field.value, rect_data))

def test_irreg_bin4():
    fname = "writing_tests/irreg_bin4.ovf"
    ovf.write_ovf(irreg_data, fname, representation="bin4")
    data = ovf.read_ovf(fname)
    assert(np.allclose(data['data']['value_0'], irreg_data[:,0]))

def test_irreg_bin8():
    fname = "writing_tests/irreg_bin8.ovf"
    ovf.write_ovf(irreg_data, fname, representation="bin8")
    data = ovf.read_ovf(fname)
    assert(np.allclose(data['data']['value_0'], irreg_data[:,0]))

def test_irreg_text():
    fname = "writing_tests/irreg_text.ovf"
    ovf.write_ovf(irreg_data, fname, representation="text")
    data = ovf.read_ovf(fname)
    assert(np.allclose(data['data']['value_0'], irreg_data[:,0]))
