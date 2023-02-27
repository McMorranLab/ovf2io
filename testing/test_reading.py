import numpy as np
import ovf2io as ovf

X = np.arange(0, 2)
Y = np.arange(0, 3)
Z = np.arange(0, 4)
x, y, z = np.meshgrid(X, Y, Z, indexing='ij')
values = np.einsum('i...->...i', np.array([x, y, z]))

def test_text_reading():
    data = ovf.read_ovf("reading_tests/df_text_rectangular.ovf")
    assert(np.allclose(data['data']['field_x'], x))
    assert(np.allclose(data['data']['field_y'], y))
    assert(np.allclose(data['data']['field_z'], z))
    assert(np.allclose(data['coords']['x'], x))
    assert(np.allclose(data['coords']['y'], y))
    assert(np.allclose(data['coords']['z'], z))


def test_bin4_reading():
    data = ovf.read_ovf("reading_tests/df_bin4_rectangular.ovf")
    assert(np.allclose(data['data']['field_x'], x))
    assert(np.allclose(data['data']['field_y'], y))
    assert(np.allclose(data['data']['field_z'], z))
    assert(np.allclose(data['coords']['x'], x))
    assert(np.allclose(data['coords']['y'], y))
    assert(np.allclose(data['coords']['z'], z))

def test_bin8_reading():
    data = ovf.read_ovf("reading_tests/df_bin8_rectangular.ovf")
    assert(np.allclose(data['data']['field_x'], x))
    assert(np.allclose(data['data']['field_y'], y))
    assert(np.allclose(data['data']['field_z'], z))
    assert(np.allclose(data['coords']['x'], x))
    assert(np.allclose(data['coords']['y'], y))
    assert(np.allclose(data['coords']['z'], z))

header_keys = {"title", "meshunit", "valueunits", "valuedim", "valuelabels", 
               "xmin", "xmax", "ymin", "ymax", "zmin", "zmax",
               "meshtype"}

def test_text_header():
    data = ovf.read_ovf("reading_tests/df_text_rectangular.ovf")
    assert(header_keys < set(data['metadata'].keys()))

def test_bin4_header():
    data = ovf.read_ovf("reading_tests/df_bin4_rectangular.ovf")
    assert(header_keys < set(data['metadata'].keys()))

def test_bin8_header():
    data = ovf.read_ovf("reading_tests/df_bin8_rectangular.ovf")
    assert(header_keys < set(data['metadata'].keys()))
