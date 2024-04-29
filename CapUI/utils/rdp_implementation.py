import tkinter as tk
import numpy as np
import argparse
import rdp_image
import misc


def rdp_implementation(data_file_name, save_file_name):
    lines = rdp_image.extract_lines_from_npy(data_file_name)
    deltas = None
    for l in lines:
        # print("line before rdp")
        # print(l)
        # print("rdp processed line")
        # print(rdp_im.rdp(l, epsilon=0.5))
        tmp = rdp_image.rdp(l, epsilon=2.0)
        # print("coords : ", tmp)
        # print("deltas : ", misc.coords_to_deltas(tmp))
        if deltas is None:
            deltas = misc.coords_to_deltas(tmp)
        else:
            deltas = np.vstack((deltas, misc.coords_to_deltas(tmp)))
    deltas = np.array(deltas)
    np.save(save_file_name, deltas)
    # print(deltas)
    # print(deltas.shape)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # Evaluation input filepaths
    parser.add_argument("--data_file_name", type=str, default='mouse_deltas.npy')
    parser.add_argument('--save_file_name', type=str, help='set output file name', default='rdp_deltas.npy')
    args = parser.parse_args()

    # rdp.extract_lines_from_npy(args.data_file_name)
    rdp_implementation(data_file_name=args.data_file_name, save_file_name=args.save_file_name)
