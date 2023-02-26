import ovf2io as oio
from pathlib import Path
import numpy as np

X = np.arange(2)
Y = np.arange(3)
Z = np.arange(4)
x, y, z = np.meshgrid(X, Y, Z, indexing='ij')

irregular_x = np.array([1., 2., 3., 4., 5.])
irregular_y = np.array([6., 7., 8., 9., 10.])
irregular_z = np.array([11., 12., 13., 14., 15.])
irregular_zeeman = np.array([500., 600., 700., 800., 900.])
irregular_ani = np.array([4e4, 5e4, 6e4, 7e4, 8e4])

def test_irregular_text():
    data = oio.read_ovf("test_ovfs/text_irregular.ovf")
    assert(np.allclose(irregular_x, data['x']))
    assert(np.allclose(irregular_y, data['y']))
    assert(np.allclose(irregular_y, data['y']))
    assert(np.allclose(irregular_zeeman, data['Zeeman energy density']))
    assert(np.allclose(irregular_ani, data['Anisotropy field']))
def test_irregular_bin4():
    data = oio.read_ovf("test_ovfs/bin4_irregular.ovf")
    assert(np.allclose(irregular_x, data['x']))
    assert(np.allclose(irregular_y, data['y']))
    assert(np.allclose(irregular_y, data['y']))
    assert(np.allclose(irregular_zeeman, data['Zeeman energy density']))
    assert(np.allclose(irregular_ani, data['Anisotropy field']))
def test_irregular_bin8():
    data = oio.read_ovf("test_ovfs/bin8_irregular.ovf")
    assert(np.allclose(irregular_x, data['x']))
    assert(np.allclose(irregular_y, data['y']))
    assert(np.allclose(irregular_y, data['y']))
    assert(np.allclose(irregular_zeeman, data['Zeeman energy density']))
    assert(np.allclose(irregular_ani, data['Anisotropy field']))
def test_rectangular_text():
    data = oio.read_ovf("test_ovfs/text_rectangular.ovf")
    assert(np.allclose(x, data['x_value']))
    assert(np.allclose(y, data['y_value']))
    assert(np.allclose(z, data['z_value']))
def test_rectangular_bin4():
    data = oio.read_ovf("test_ovfs/bin4_rectangular.ovf")
    assert(np.allclose(x, data['x_value']))
    assert(np.allclose(y, data['y_value']))
    assert(np.allclose(z, data['z_value']))
def test_rectangular_bin8():
    data = oio.read_ovf("test_ovfs/bin8_rectangular.ovf")
    assert(np.allclose(x, data['x_value']))
    assert(np.allclose(y, data['y_value']))
    assert(np.allclose(z, data['z_value']))

