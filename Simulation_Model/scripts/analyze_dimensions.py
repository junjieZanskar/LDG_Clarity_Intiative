import numpy as np

def analyze_dat_file(filename):
    data = np.loadtxt(filename)
    print(f"Data shape: {data.shape}")
    
    if data.shape[1] >= 3:  # If we have x,y,z coordinates
        x = np.unique(data[:, 0])
        y = np.unique(data[:, 1])
        z = np.unique(data[:, 2])
        
        print(f"Number of unique X coordinates: {len(x)}")
        print(f"Number of unique Y coordinates: {len(y)}")
        print(f"Number of unique Z coordinates: {len(z)}")
        print(f"X range: {x.min()} to {x.max()}")
        print(f"Y range: {y.min()} to {y.max()}")
        print(f"Z range: {z.min()} to {z.max()}")
    else:
        print("Data appears to be 1D array of values")
        print(f"Total number of points: {len(data)}")
        print(f"Possible cubic dimension: {int(np.cbrt(len(data)))}")

filename = "/Users/zanskar_junjie/Downloads/LDG-ver5-L90.DAT"
analyze_dat_file(filename) 