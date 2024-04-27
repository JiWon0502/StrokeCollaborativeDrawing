import numpy as np


# npz file to npy array for original quickdraw dataset
# only the first index
def npz2npy_quickdraw(npz_filename):
    data = np.load(npz_filename, encoding='latin1', allow_pickle=True)
    extracted_data = data['test'][0]
    print(extracted_data)
    np.save('../npz2npy.npy', extracted_data)


# npz file to npy array for original quickdraw dataset
# all training data saved as {filename}_npz2npy_{index}.npy
def npz2npy_quickdraw_full(npz_filename):
    data = np.load(npz_filename, encoding='latin1', allow_pickle=True)
    for i in range(data['test'].shape[0]):
        extracted_data = data['test'][i]
        print(extracted_data)
        filename = '../{}_npz2npy_{}.npy'.format(npz_filename, i)
        np.save(filename, extracted_data)

# For output file of the AI model
# npz file must have
# 1. scaled with 256 * 256
# 2. inserted (start_x, start_y, True)
def npz2npy_output(npz_filename):
    # Load the .npz file
    data = np.load(npz_filename, encoding='latin1', allow_pickle=True)
    # List all the files stored in the .npz file
    #print("Files in the .npz archive:", data.files)
    #print("Files in the .npz archive:", extracted_data.files)
    print("Files in the .npz archive", data.files)
    # Load each array from the .npz file
    x_array = data['x']
    y_array = data['y']
    z_array = data['z']
    """
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
    """
    # print("rescaled : ", rescaled_array)
    # Save the extracted array as a .npy file
    stacked_data = np.stack((x_array, y_array, z_array), axis=-1)
    np.save('../npz2npy.npy', stacked_data)
    print(stacked_data)


if __name__ == "__main__":
    filename = input("Enter filename: ")
    npz2npy_output(filename)
