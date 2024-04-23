import tkinter as tk
import numpy as np
import reconstruct_delta as rd
import MousePainter as mp
from utils import rdp

if __name__ == "__main__":
    painter = mp.MousePainter()
    painter.run()
    d_coords = painter.deltas

