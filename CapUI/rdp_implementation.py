import tkinter as tk
import numpy as np
import argparse
from rdp_tmp import rdp


def rdp_implementation(data_file_name, save_file_name):
    data = np.load(data_file_name, allow_pickle=True, encoding='latin1')
    for dx, dy, penstate in data:

    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # Evaluation input filepaths
    parser.add_argument("--data_file_name", type=str, default='mouse_deltas.npy')
    parser.add_argument('--save_file_name', type=str, help='set output file name', default='rdp_deltas.npy')
    args = parser.parse_args()

    rdp_implementation(data_file_name=args.data_file_name, save_file_name=args.save_file_name)
