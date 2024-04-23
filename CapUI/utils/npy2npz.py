import numpy as np
data = np.load("/Users/yoonjiwon/PycharmProjects/demo_1st/lmser/dataset/airplane.npz", allow_pickle=True, encoding='latin1')

test_data = data['test']

print('Test Data Shape: ', test_data.shape)

# Load the .npy file
array = np.load('/Users/yoonjiwon/PycharmProjects/demo_1st/CapUI/mouse_deltas.npy')
reshaped_array = np.expand_dims(array, axis=0)

#print(reshaped_array.shape)  # numpy.ndarray의 형태 확인
#print(type(reshaped_array))
#print(reshaped_array[0].shape)  # 첫 번째 요소의 형태 확인
#print(type(reshaped_array[0]))
#print(reshaped_array[0][0])

np.savez('/Users/yoonjiwon/PycharmProjects/demo_1st/lmser/dataset/airplane.npz', test=reshaped_array)

