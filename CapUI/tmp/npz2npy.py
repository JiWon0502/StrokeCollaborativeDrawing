import numpy as np

# Load the .npz file
data = np.load("../../lmser/results/0.1/xyz/airplane/1.npz", encoding='latin1', allow_pickle=True)

# List all the files stored in the .npz file
print("Files in the .npz archive:", data.files)

# Load each array from the .npz file
x_array = data['x']
y_array = data['y']
z_array = data['z']

# Rescale 'x' and 'y' arrays to the range 0 to 255
x_min = x_array.min()
x_max = x_array.max()
y_min = y_array.min()
y_max = y_array.max()

sum_x = np.cumsum(x_array, axis=0)
sum_y = np.cumsum(y_array, axis=0)

rescaled_x_array = ((x_array - x_min) / (sum_x.max() - sum_x.min())) * 255
rescaled_y_array = ((y_array - y_min) / (sum_y.max() - sum_y.min())) * 255

# Combine rescaled 'x' and 'y' arrays with 'z' array
rescaled_data = np.stack((rescaled_x_array, rescaled_y_array, z_array), axis=-1)

# Convert the rescaled array to integers (0 to 255)
rescaled_array = rescaled_data.astype(np.uint8)

print("rescaled : ", rescaled_array)
# Save the extracted array as a .npy file
np.save('../extracted_array.npy', rescaled_array)
