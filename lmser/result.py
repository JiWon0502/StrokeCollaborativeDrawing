import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import os

for a in range(100):
    file_path = f"/Users/jungseyoon/Lmser-pix2seq/result/second/{a}.npz" # first, second, ...
    if os.path.exists(file_path):
        data = np.load(file_path, allow_pickle=True, encoding='latin1')
        test_data = data['test']
        print('Test Data Shape: ', test_data.shape)

        points = test_data[0]
        points[:, 1] = - points[:, 1]
        cumsum = np.cumsum(points, axis=0)

        start_point = np.array([0, 0, 0])
        cumsum = np.vstack((start_point, cumsum))
        
        plt.figure()  # 새로운 figure 생성
        
        #for i in range(1, len(cumsum)):
            #if points[i - 1, 2] != 0: # (i - 1)번째 점이 "누름" 상태가 아닌 경우
                #plt.plot(cumsum[i - 1 : i + 1, 0], cumsum[i - 1 : i + 1, 1], marker='o', color='red') # (i - 1)번째 점과 i번째 점 잇기
            #else:
                #plt.plot(cumsum[i - 1 : i + 1, 0], cumsum[i - 1 : i + 1, 1], marker='o', color='blue') # (i - 1)번째 점과 i번째 점 잇기

        for i in range(0, len(points)):
            if points[i, 2] != 0:
                plt.plot(cumsum[i : i + 2, 0], cumsum[i : i + 2, 1], marker='o', color='red')
            else:
                plt.plot(cumsum[i : i + 2, 0], cumsum[i : i + 2, 1], marker='o', color='blue')
        
        plt.title(i)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.grid(True)
        plt.savefig(f"/Users/jungseyoon/Lmser-pix2seq/result/second/{a}.png") # first, second, ...
        #plt.show()
        plt.close()
        
    else:
        print("File does not exist.")
    a = a + 1
