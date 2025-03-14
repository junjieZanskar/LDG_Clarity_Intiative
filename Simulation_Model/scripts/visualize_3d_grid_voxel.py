import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LinearSegmentedColormap
from scipy.interpolate import griddata

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

def visualize_with_threshold(x, y, z, values, threshold=100, resolution=50):
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
    
    # Create binary grid and colors based on threshold
    grid = interpolated_values > threshold
    colors = np.zeros(grid.shape + (4,))  # RGBA colors
    
    # Set colors based on interpolated values
    mask = interpolated_values > threshold
    max_val = interpolated_values.max()
    normalized_values = (interpolated_values - threshold) / (max_val - threshold)
    colors[mask] = np.column_stack((
        np.zeros(np.sum(mask)),  # Red
        np.zeros(np.sum(mask)),  # Green
        np.ones(np.sum(mask)),   # Blue
        normalized_values[mask]   # Alpha (opacity)
    ))
    
    # Create figure with a specific size and layout
    fig = plt.figure(figsize=(15, 8))
    gs = fig.add_gridspec(1, 2, width_ratios=[20, 1])
    
    # Create the 3D axes for the voxel plot
    ax = fig.add_subplot(gs[0], projection='3d')
    
    # Plot voxels
    ax.voxels(grid, facecolors=colors, edgecolor='k', alpha=0.5)
    
    # Set labels with actual coordinate values
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    ax.set_zlabel('Z Coordinate')
    
    # Set axis ticks to show actual coordinate values
    ax.set_xticks(np.linspace(0, resolution-1, 5))
    ax.set_yticks(np.linspace(0, resolution-1, 5))
    ax.set_zticks(np.linspace(0, resolution-1, 5))
    
    ax.set_xticklabels([f'{x:.0f}' for x in np.linspace(x_min, x_max, 5)])
    ax.set_yticklabels([f'{y:.0f}' for y in np.linspace(y_min, y_max, 5)])
    ax.set_zticklabels([f'{z:.0f}' for z in np.linspace(z_min, z_max, 5)])
    
    # Set title
    ax.set_title(f'3D Voxel Visualization\n(Permeability > {threshold})')
    
    # Create custom colormap
    cmap = LinearSegmentedColormap.from_list('custom', ['lightblue', 'darkblue'])
    norm = plt.Normalize(threshold, max_val)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    
    # Add colorbar in the second subplot position
    cax = fig.add_subplot(gs[1])
    plt.colorbar(sm, cax=cax, label='Permeability')
    
    plt.tight_layout()
    plt.show()

    # Create histogram of permeability values
    plt.figure(figsize=(10, 6))
    plt.hist(values[values > threshold], bins=30, color='blue', alpha=0.7)
    plt.xlabel('Permeability')
    plt.ylabel('Frequency')
    plt.title(f'Permeability Distribution\n(Values > {threshold})')
    plt.grid(True)
    plt.show()

# Load and analyze the data
filename = "LDG-ver52-M92-FRAC-PERMZ"
x, y, z, values = read_and_analyze_dat_file(filename)

# Analyze the distribution
analyze_distribution(values)

# Create visualization with threshold
visualize_with_threshold(x, y, z, values, threshold=100, resolution=50)

# Print some statistics about the coordinate distribution
print("\nCoordinate Distribution Statistics:")
print(f"X range: {x.min():.2f} to {x.max():.2f}")
print(f"Y range: {y.min():.2f} to {y.max():.2f}")
print(f"Z range: {z.min():.2f} to {z.max():.2f}")
print("\nUnique coordinate counts:")
print(f"Unique X values: {len(np.unique(x))}")
print(f"Unique Y values: {len(np.unique(y))}")
print(f"Unique Z values: {len(np.unique(z))}")