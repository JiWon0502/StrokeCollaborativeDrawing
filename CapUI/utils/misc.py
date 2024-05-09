import os
import numpy as np
from . import rdpfunc

"""
def npy2npz(npy_filename, npz_filename) : converts npy to npz
# hyper_params.py -> self.category = [npz_filename]으로 두고 inference.py 돌리면 돌아감

(start_point_x, start_point_y, pen_state=1)
(dx, dy, pen_state) * 반복
"""

"""
convert npz to npy - misc.py에 저장
1. def npz2npy_output(npz_filename, npy_filename) : ai model에서 나온 output 기반 Npy로 변환. (가정 : Scale, 시작 좌표 이미 다 계산됨)
2. def npz2npy_quickdraw(npz_filename) : data['test'][0]에 있는 (dx, dy, penstate) "npz2npy.npy"로 저장
3. def npz2npy_quickdraw_full(npz_filename): 2번에서 하는 걸 모든 index에 대해 실행. "{filename}_npz2npy_{index}.npy"로 저장
"""

# append start_point_x, start_point_y, pen_state first...

"""
todo
1. npz2npy, UI 그림 추가 안되는 부분 수정 (완)
2. stroke ordering
3. rdp algorithm (완)
4. npz stroke rescale
5. evaluation : classification
세윤 -> 2 + 4
지민 -> 5
지원 1, 3
"""


# Generate a new filename with an index appended to it
def generate_filename_with_index(base_filename, index):
    # Split the base filename and extension
    name, ext = os.path.splitext(base_filename)
    # Concatenate the index to the name part
    new_filename = f"{name}_{index}{ext}"
    return new_filename


# Create a directory with the name of the index and save files within that directory
def save_with_indexed_directory(base_directory, index, filename, data):
    # Generate directory name with the index
    directory_name = os.path.join(base_directory, f"index_{index}")
    # Create the directory if it doesn't exist
    os.makedirs(directory_name, exist_ok=True)
    # Modify the file name
    file = generate_filename_with_index(filename, index)
    # Save the file within the directory
    file_path = os.path.join(directory_name, file)
    np.save(file_path, data)


# npz file to npy array for original quickdraw dataset
# only the first index
def npz2npy_quickdraw(npz_filename, npy_filename):
    data = np.load(npz_filename, encoding='latin1', allow_pickle=True)
    extracted_data = data['test'][0]
    # print(extracted_data)
    np.save(npy_filename, extracted_data)


# npz file to npy array for original quickdraw dataset
# all training data saved as {filename}_npz2npy_{index}.npy
def npz2npy_quickdraw_full(npz_filename):
    data = np.load(npz_filename, encoding='latin1', allow_pickle=True)
    for i in range(data['test'].shape[0]):
        extracted_data = data['test'][i]
        # print(extracted_data)
        filename = '../{}_npz2npy_{}.npy'.format(npz_filename, i)
        np.save(filename, extracted_data)


# For output file of the AI model
# npz file must have
# 1. scaled with 256 * 256
# 2. inserted (start_x, start_y, True)
def npz2npy_output(npz_filename):
    # Load the .npz file
    data = np.load(npz_filename, encoding='latin1', allow_pickle=True)
    x_array = data['x']
    y_array = data['y']
    z_array = data['z']
    stacked_data = np.stack((x_array, y_array, z_array), axis=-1)
    np.save('../npz2npy.npy', stacked_data)
    # print(stacked_data)


# For input file of the AI model
# hyper_params.py -> self.category = [npz_filename]으로 두고 inference.py 돌리면 돌아감
# npy file (dx, dy, pen_state) to npz file ["test"][0] = [(dx, dy, pen_state)]
def npy2npz(npy_filename, npz_filename):
    data = np.load(npy_filename, encoding='latin1', allow_pickle=True)
    # Check if npz_filename ends with ".npy"
    if npz_filename.endswith(".npy"):
        # Replace ".npy" with ".npz"
        npz_filename = npy2npz_name(npz_filename)
    npz_data = {"test": [], "train": [], "val": []}
    data_tmp = np.empty(1, dtype=object)
    data_tmp[0] = data
    # reshaped_array = np.reshape(reshaped_array, (1,))
    # print(data_tmp.shape)
    # print(data_tmp[0].shape)
    npz_data['test'] = data_tmp
    np.savez_compressed(npz_filename, **npz_data)


def npy2npz_name(npy_filename):
    npz_filename = os.path.splitext(npy_filename)[0] + ".npz"
    return npz_filename

def coords_to_deltas(coords, lastx, lasty):
    # print("coords_to_deltas - coords shape : ", coords.shape)
    dx_dy = np.diff(coords, axis=0)
    pen_states = np.zeros((len(dx_dy), 1))
    deltas = np.hstack((dx_dy, pen_states))
    arr_reshaped = coords[0].reshape(1, -1)
    arr_reshaped = arr_reshaped - np.array([lastx, lasty])
    arr_reshaped = np.hstack((arr_reshaped, np.array([[1]])))
    # print("coords_to_deltas - reshaped array :", arr_reshaped)
    result = np.vstack((arr_reshaped, deltas)).astype(int)
    # print("coords_to_deltas - result shape : ", result.shape)
    # print("coords_to_deltas - result : ", result)
    # print("deltas, penstate, concat, coords[0]",dx_dy.shape, pen_states.shape, deltas.shape, arr_reshaped.shape)
    lastx, lasty = coords[-1]
    # print("last x, last y : ", lastx, lasty)
    return result, lastx, lasty


def rdp_final(data_file_name, save_file_name):
    lines = rdpfunc.extract_lines_from_npy(data_file_name)
    deltas = None
    lastx, lasty = 0, 0
    for l in lines:
        # print("line before rdp")
        # print(l)
        # print("rdp processed line")
        # print(rdpfunc.rdp(l, epsilon=0.5))
        tmp = rdpfunc.rdp(l, epsilon=2.0)
        # print("coords : ", tmp)
        # print("deltas : ", misc.coords_to_deltas(tmp))
        if deltas is None:
            d_tmp, lastx, lasty = coords_to_deltas(tmp, lastx, lasty)
            deltas = d_tmp
        else:
            d_tmp, lastx, lasty = coords_to_deltas(tmp, lastx, lasty)
            deltas = np.vstack((deltas, d_tmp))
    # print(deltas)
    # print("how long is rdp processed deltas : ", deltas.__len__())
    deltas = np.array(deltas)
    np.save(save_file_name, deltas)


# ******************************************************************************** #
# from here, Reference : inference_sketch_processing.py from Lmser-pix2seq model
# ******************************************************s************************** #

# base the starting point of the drawing to canvas left/up
# and calculate size from all coordinates in the sketch
# canvas_size_google function from inference_sketch_processing.py
# [int(start_x), int(start_y), int(h), int(w)]
# must call "scale_sketch" first !!!!!!!!!!!!!!!
def find_start_point_and_size(sketch):
    """
    :param sketch: output .npz file from ai model with sketch information
    :return: int list,[x, y, h, w]

    # 문제1 : 만약에 sketch array수가 0~1 사이면 w,h가 0으로 return 된다.
    # 문제2 : 왠지 모르겠는데 sketch에 float 값들이 들어가거나 int 값이 들어간 경우가 두가지 다 있는데 이러면 int()로 씌웠을 때 값이 0.x인경우 0으로 바뀌어버린다. 그런데 w, h는 0이 될 수 없다... rescale을 하거나 이미 int로 바뀌어진 상태에서 들어와야 하는듯
    """
    # get canvas size
    vertical_sum = np.cumsum(sketch[1:], axis=0)
    # get minimum, maximum pixel coordinate
    xmin, ymin, _ = np.min(vertical_sum, axis=0)
    xmax, ymax, _ = np.max(vertical_sum, axis=0)
    # calculate whole canvas size
    w = xmax - xmin
    h = ymax - ymin
    # calculate starting point
    start_x = - xmin - sketch[0][0]
    start_y = - ymin - sketch[0][1]

    return [int(start_x), int(start_y), int(h), int(w)]


# deprecated version : float32
# np.float32 -> float
def scale_sketch(sketch, size=(256, 256)):
    [_, _, h, w] = find_start_point_and_size(sketch)
    if h >= w:
        sketch_normalize = sketch / np.array([[h, h, 1]], dtype=float)
    else:
        sketch_normalize = sketch / np.array([[w, w, 1]], dtype=float)
    sketch_rescale = sketch_normalize * np.array([[size[0], size[1], 1]], dtype=float)
    return sketch_rescale.astype("int16")


if __name__ == "__main__":
    # rdp.extract_lines_from_npy(args.data_file_name)
    rdp_final(data_file_name='../mouse_deltas.npy', save_file_name='../rdp_deltas.npy')
