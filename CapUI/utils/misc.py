import os
import numpy as np

# npy file format
"""
npy2npz.py function : converts npy to npz
(start_point_x, start_point_y, pen_state=1)
(dx, dy, pen_state) * 반복
"""

"""
npz2npy.py : 
convert npz to npy
append start_point_x, start_point_y, pen_state at first

"""


"""
todo
1. npz2npy랑 UI 그림 추가 안되는 부분 수정 -> jiwon
2. stroke ordering
3. rdp algorithm ->  *rdp_tmp.py 사용 가능, delta to coords도 가능
4. npz stroke rescale
5. evaluation : classification
세윤 -> 2 + 4, 3 순서 
지민 -> 5, 3 순서
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
