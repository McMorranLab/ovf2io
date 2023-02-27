import discretisedfield as df
import numpy as np

X = np.arange(0, 2)
Y = np.arange(0, 3)
Z = np.arange(0, 4)
x, y, z = np.meshgrid(X, Y, Z, indexing='ij')
values = np.einsum('i...->...i', np.array([x, y, z]))

mesh = df.Mesh(p1=(-0.5, -0.5, -0.5), p2=(1.5, 2.5, 3.5), cell=(1., 1., 1.))
field = df.Field(mesh=mesh, dim=3, value=values)
field.write("test_ovfs/df_bin8_rectangular.ovf", representation="bin8")
field.write("test_ovfs/df_bin4_rectangular.ovf", representation="bin4")
field.write("test_ovfs/df_text_rectangular.ovf", representation="txt")
