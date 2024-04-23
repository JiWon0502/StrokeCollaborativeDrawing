import numpy as np

# Load the .npz file
#data = np.load("../lmser/results/0.1/xyz/airplane/0.npz", encoding='latin1', allow_pickle=True)
data = np.load("../lmser/dataset/airplane.npz", encoding='latin1', allow_pickle=True)

# List all the files stored in the .npz file
print("Files in the .npz archive:", data.files)

# Access the 'train' array directly and work with it
train_data = data['train']

# Print the shape of the train_data array
print("Shape of train_data:", train_data.shape)

# Print the data type of the train_data array
print("Data type of train_data:", train_data.dtype)

# Print the content of the train_data array
print("Content of train_data:")
print(train_data)

# Extract a .npy file (assuming it's named 'array.npy')
array_npy = train_data[0]

# Save the extracted array as a .npy file
np.save('extracted_array.npy', array_npy)
