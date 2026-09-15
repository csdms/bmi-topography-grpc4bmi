# Run the Topography Data Component through *grpc4bmi*

import pathlib
import numpy as np
import matplotlib.pyplot as plt
from grpc4bmi.bmi_client_docker import BmiClientDocker


# Set variables:
# * which Docker image to use,
# * the port exposed through the image, and
# * the location of the configuration file used for the tool.
DOCKER_IMAGE = "csdms/bmi-topography-grpc4bmi"
BMI_PORT = 55555
CONFIG_FILE = pathlib.Path("config.yaml")

# Create a model instance, `m`, through the grpc4bmi Docker client.
# It may take moment to download the model image from Docker Hub.
m = BmiClientDocker(image=DOCKER_IMAGE, image_port=BMI_PORT, work_dir=".")

# The first step in using a BMI is calling the `initialize` method.
# This method requires a configuration file that provides initial values for the `Topography` library wrapped by the BMI.
# This step may take a moment as the `Topography` library fetches and downloads the data from the OpenTopography server.
m.initialize(str(CONFIG_FILE))

# Display the name of the one variable exposed through the BMI.
m.get_output_var_names()

# Find the data type of the elevation data.
dtype = m.get_var_type("land_surface__elevation")
print(dtype)

# Get the grid index for the elevation variable.
grid = m.get_var_grid("land_surface__elevation")
print(grid)

# Find the total size of the elevation data.
size = m.get_grid_size(grid)
print(size)

# Get the elevation data.
elevation = np.ndarray(size, dtype)
m.get_value("land_surface__elevation", elevation)

# Note that the elevation array is one-dimensional.
print(elevation.shape)

# Determine the dimensionality of the elevation variable.
rank = m.get_grid_rank(grid)
print(rank)

# Get the dimensions of the elevation data, first creating an array to store their values.
shape = np.ndarray(rank, dtype=int)
print(shape)
m.get_grid_shape(grid, shape)

# Reshape the elevation data, creating a new array.
elevation2D = elevation.reshape(shape)

# Visualize the elevation data as an image.
plt.imshow(elevation2D)

# Stop the model and clean up the resources it allocates.
m.finalize()

# Stop the container running through grpc4bmi.
# This is needed by grpc4bmi to properly deallocate the resources it uses.
# It may take a few moments.
del m
