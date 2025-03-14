import numpy as np
import pyvista as pv
from scipy.interpolate import griddata
import matplotlib.pyplot as plt

def read_and_analyze_dat_file(filename):
    # Read the data, skipping the first two lines (header)
    data = np.loadtxt(filename, skiprows=2)
    
    # Extract X, Y, Z coordinates and permeability values
    x = data[:, 0]
    y = data[:, 1]
    z = data[:, 2]
    values = data[:, 3]
    
    return x, y, z, values

def analyze_distribution(values):
    """Analyze the distribution of permeability values"""
    print("\nPermeability Distribution Analysis:")
    print(f"Min value: {values.min():.2f}")
    print(f"Max value: {values.max():.2f}")
    print(f"Mean value: {values.mean():.2f}")
    print(f"Median value: {np.median(values):.2f}")
    
    # Count values above threshold
    threshold = 100
    count = np.sum(values > threshold)
    percentage = (count / len(values)) * 100
    print(f"\nValues above {threshold}: {count} ({percentage:.2f}%)")
    if count > 0:
        print(f"Unique values above {threshold}: {np.unique(values[values > threshold])}")

def visualize_with_pyvista(x, y, z, values, threshold=100, resolution=50):
    # Create high-resolution grid
    x_min, x_max = x.min(), x.max()
    y_min, y_max = y.min(), y.max()
    z_min, z_max = z.min(), z.max()
    
    # Create regular grid points
    x_grid = np.linspace(x_min, x_max, resolution)
    y_grid = np.linspace(y_min, y_max, resolution)
    z_grid = np.linspace(z_min, z_max, resolution)
    
    # Create meshgrid
    X, Y, Z = np.meshgrid(x_grid, y_grid, z_grid)
    
    # Prepare points for interpolation
    points = np.column_stack((x, y, z))
    grid_points = np.column_stack((X.flatten(), Y.flatten(), Z.flatten()))
    
    # Interpolate values
    print("Interpolating values...")
    interpolated_values = griddata(points, values, grid_points, method='linear', fill_value=0)
    interpolated_values = interpolated_values.reshape(resolution, resolution, resolution)
    
    # Create PyVista structured grid
    grid = pv.ImageData()
    grid.dimensions = [resolution, resolution, resolution]
    grid.origin = [x_min, y_min, z_min]
    grid.spacing = [(x_max-x_min)/(resolution-1), 
                   (y_max-y_min)/(resolution-1), 
                   (z_max-z_min)/(resolution-1)]
    
    # Add the interpolated values to the grid
    grid.point_data["values"] = interpolated_values.flatten(order="F")
    
    # Create threshold mesh for grid visualization
    threshed = grid.threshold([threshold, grid.point_data["values"].max()])
    
    # Create plotter
    plotter = pv.Plotter()
    
    # Add the thresholded mesh with edges
    plotter.add_mesh(threshed,
                    scalars="values",
                    show_edges=True,
                    edge_color='black',
                    line_width=1,
                    opacity=0.7,
                    cmap="viridis",
                    clim=[threshold, values.max()],
                    log_scale=True,
                    show_scalar_bar=True,
                    scalar_bar_args={'title': 'Permeability', 
                                    'n_labels': 5,
                                    'fmt': '%.1f'})
    
    # Add a helper mesh to show the full grid structure
    outline = grid.outline()
    plotter.add_mesh(outline, color='black', opacity=1.0)
    
    # Set camera position for better view
    plotter.camera_position = 'iso'
    
    # Add axes
    plotter.add_axes()
    
    # Show the grid
    plotter.show_grid()
    
    # Set background color to white
    plotter.set_background('white')
    
    # Show the plot
    plotter.show()
    

def plot_permeability_distribution(values, filename_prefix):
    """Create and save a histogram of permeability values"""
    plt.figure(figsize=(10, 6))
    
    # Create histogram with both linear and log scale
    plt.subplot(1, 2, 1)
    plt.hist(values, bins=50, edgecolor='black')
    plt.title('Permeability Distribution (Linear Scale)')
    plt.xlabel('Permeability')
    plt.ylabel('Frequency')
    
    plt.subplot(1, 2, 2)
    plt.hist(values, bins=50, edgecolor='black')
    plt.xscale('log')
    plt.title('Permeability Distribution (Log Scale)')
    plt.xlabel('Permeability')
    plt.ylabel('Frequency')
    
    plt.tight_layout()
    plt.savefig(f'{filename_prefix}_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()

# Load and analyze the data
filename = "LDG-ver52-M92-FRAC-PERMZ"
x, y, z, values = read_and_analyze_dat_file(filename)

# Analyze the distribution
analyze_distribution(values)

# Plot and save the distribution
plot_permeability_distribution(values, filename)

# Create visualization with threshold
visualize_with_pyvista(x, y, z, values, threshold=100, resolution=50)