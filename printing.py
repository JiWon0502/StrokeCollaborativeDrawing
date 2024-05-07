import numpy as np
import tensorflow as tf
import subprocess
import os


p = 4 # number of maximum added strokes
q = 4 # number of initial strokes

for a in range(1):

    print("------------------------------masking------------------------------", a)

    # first loop ~
    data = np.load("/Users/jungseyoon/Lmser-pix2seq/dataset/airplane_real.npz", allow_pickle=True, encoding='latin1')
    test_data = data['test']
    points = test_data[a]

    index = q - 1 # q개의 stroke만 선택
    if len(points) <= q:
        print("마스킹 실패")
    else:
        points = points[:index + 1, :] # 0 ~ index까지 저장 (총 index + 1 개의 stroke 저장)
        list = []
        list.append(points.reshape(points.shape))
        reshaped_list = np.array(list)
        np.savez('/Users/jungseyoon/Lmser-pix2seq/dataset/airplane_test.npz', test=reshaped_list)
