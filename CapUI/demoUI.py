import tkinter as tk
import numpy as np
import MousePainter as mp
from utils import rdp
import argparse

parser = argparse.ArgumentParser()
# Evaluation input filepaths
parser.add_argument('--savefile_name', type=str, help='set output file name', default='mouse_deltas.npy')
args = parser.parse_args()

if __name__ == "__main__":
    painter = mp.MousePainter(args)
    painter.run()


