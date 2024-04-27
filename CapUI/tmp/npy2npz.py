import numpy as np
"""
data = np.load("/Users/yoonjiwon/PycharmProjects/demo_1st/lmser/dataset/airplane.npz", allow_pickle=True,
               encoding='latin1')

test_data = data['test']

print('Test Data Shape: ', test_data.shape)

# Load the .npy file
array = np.load('/CapUI/mouse_deltas.npy')
reshaped_array = np.expand_dims(array, axis=0)

# print(reshaped_array.shape)  # numpy.ndarray의 형태 확인
# print(type(reshaped_array))
# print(reshaped_array[0].shape)  # 첫 번째 요소의 형태 확인
# print(type(reshaped_array[0]))
# print(reshaped_array[0][0]) # 첫번째 좌표 dx, dy, pen_state

np.savez('/Users/yoonjiwon/PycharmProjects/demo_1st/lmser/dataset/airplane.npz', test=reshaped_array)

"""

def check(npz_filename):
    data1 = np.load(npz_filename, encoding='latin1', allow_pickle=True)
    data2 = np.load("/Users/yoonjiwon/PycharmProjects/demo_1st/lmser/dataset/bus.npz", encoding='latin1', allow_pickle=True)
    for key in data1.keys():
        print("data1 : ", key)
    for key in data2.keys():
        print("data2 : ", key)
    print(type(data1), type(data2))
    print(data1["test"].shape)  # Check the shape of the "test" array
    print(data2["test"].shape)  # Check the shape of the "test" array
    print(type(data1["test"]))
    print(type(data2["test"]))
    print(data1["test"][0].shape)  # Check the first coordinate (dx, dy, pen_state)
    print(data2["test"][0].shape)  # Check the first coordinate (dx, dy, pen_state)
    print(data1["test"][0][0])  # Check the first coordinate (dx, dy, pen_state)
    print(data2["test"][0][0])  # Check the first coordinate (dx, dy, pen_state)
    print(len(data1["test"]))
    print(len(data2["test"]))


# npy file (dx, dy, pen_state) to npz file ["test"][0] = [(dx, dy, pen_state)]
def npy2npz(npy_filename, npz_filename):
    data = np.load(npy_filename, encoding='latin1', allow_pickle=True)
    npz_data = {"test": [], "train": [], "val": []}
    data_tmp = np.empty(1, dtype=object)
    data_tmp[0] = data
    #reshaped_array = np.reshape(reshaped_array, (1,))
    print(data_tmp.shape)
    print(data_tmp[0].shape)
    npz_data['test'] = data_tmp
    np.savez_compressed(npz_filename, **npz_data)
    """
    data = np.load(npy_filename, encoding='latin1', allow_pickle=True)
    save_data = {'test': []}
    save_data['test'].append(data)
    np.savez_compressed(npz_filename, **save_data)
    print(save_data)  # numpy.ndarray의 형태 확인
    #print(type(save_data))
    print(save_data["test"].shape)  # 첫 번째 요소의 형태 확인
    print(type(save_data["test"]))
    print(save_data["test"][0]) # 첫번째 좌표 dx, dy, pen_state
    """


if __name__ == "__main__":
    npyfilename = input("Enter filename: ")
    npzfilename = input("Enter filename: ")
    npy2npz(npyfilename, npzfilename)
    check(npzfilename)