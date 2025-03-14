import numpy as np
import pyvista as pv
import pandas as pd
import matplotlib.pyplot as plt  # Import Matplotlib for plotting

def read_and_analyze_dat_file(filename):
    # Read the data
    data = np.loadtxt(filename)
    
    # If the data is in x,y,z,value format (4 columns)
    if data.shape[1] >= 3:  # Check if we have at least x,y,z columns
        x = np.unique(data[:, 0])
        y = np.unique(data[:, 1])
        z = np.unique(data[:, 2])
        
        nx, ny, nz = len(x), len(y), len(z)
        print(f"Grid dimensions detected: {nx} x {ny} x {nz}")
        
        # If there's a value column (4th column)
        if data.shape[1] >= 4:
            values = data[:, 3]
        else:
            values = np.ones(len(data))  # Default values if not provided
            
        return data, nx, ny, nz, values
    else:
        # If data is just a 1D array of values
        total_size = len(data)
        print(f"Total data points: {total_size}")
        # Try to determine factors
        factors = []
        for i in range(1, int(np.sqrt(total_size)) + 1):
            if total_size % i == 0:
                factors.append(i)
        print(f"Possible factors: {factors}")
        # Guess dimensions (assuming cubic or near-cubic grid)
        dim = int(np.cbrt(total_size))
        if dim**3 == total_size:
            nx = ny = nz = dim
            print(f"Data appears to be a {dim}x{dim}x{dim} cubic grid")
        else:
            raise ValueError("Could not automatically determine grid dimensions")
        
        return data, nx, ny, nz, data

# Load and analyze the data
filename = "LDG-ver52-M92-FRAC-PERMZ"
data, nx, ny, nz, values = read_and_analyze_dat_file(filename)

# Debugging: Check the shape of the data and values
print(f"Data shape: {data.shape}")  # Should be (n, 3) or (n, 4)
print(f"Values shape: {values.shape}")  # Should match the number of points

# Create a structured grid from the geological data
grid = pv.StructuredGrid()
grid.points = data[:, :3]
grid.dimensions = [nx, ny, nz]
grid.point_data["values"] = values  # Assign random values to point data

# Create a mask for opacity based on values
opacity = np.where(values < 1000, 0, 0.7)  # Set opacity to 0 for values < 3000

# Create the plotter
plotter = pv.Plotter()
plotter.add_mesh(grid, opacity=opacity, show_edges=True, edge_color='black', line_width=2)  # Set edge color and width
plotter.camera_position = 'iso'  # Set camera position to isometric view
plotter.show_grid()
plotter.show()

# After loading and analyzing the data
# Create a histogram of the permz values
# plt.figure(figsize=(10, 6))
# plt.hist(values, bins=30, color='blue', alpha=0.7)  # Adjust the number of bins as needed
# plt.title('Distribution of permz Values')
# plt.xlabel('permz Value')
# plt.ylabel('Frequency')
# plt.grid(True)
# plt.show()