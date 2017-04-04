import numpy as np
import sys
sys.path.append('../vector_field_plot_tool')
from array_reader import ArrayReader
from plot_vector_field import plot_vector_field, plot_scalar_field
from discretisedfield import Mesh, Field

# Define a Mesh and a DiscretisedField object
c1 = (1, 1, 1)
c2 = (10, 6, 9)
d = (1, 1, 1)
mesh = Mesh(c1, c2, d)
dim = 3
# mesh
field = Field(mesh, dim=dim, name='fdfield')

# value = (1, 3, 5)
# field.value = value
def value(pos):
    x, y, z = pos

    fx = 2 * x * y
    fy = 2 * y + x
    fz = x + z

    return (fx, fy, fz)

field.value = value

# -----------------------------------------------------------------------------

coordinates = np.array([r for r in field.mesh.coordinates])

vector_field = []
for i, c in zip(mesh.indices, mesh.coordinates):
    coordinate = c
    value = field.array[i]  # or value = self.__call__(c)
    vector_field.append(value)

vector_field = np.array(vector_field)
# print(vector_field)

ar = ArrayReader(coordinates, vector_field)

# -----------------------------------------------------------------------------

ax = plot_scalar_field(ar, 1, 10, 1, 6, alpha=1, cmap='viridis_r',
                       vf_component='x',
                       clim=[np.min(vector_field),
                             np.max(vector_field)],
                       )
plot_vector_field(ar, 1, 10, 1, 6, colorbar=True, ax=ax, cmap='viridis_r',
                  vf_component='x',
                  clim=[np.min(vector_field), np.max(vector_field)],
                  quiver_type='interpolated_color',
                  savefig='test.pdf')