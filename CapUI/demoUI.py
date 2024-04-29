import argparse

import MousePainter as MP
from utils.misc import rdp_final

parser = argparse.ArgumentParser()
# Evaluation input filepaths
parser.add_argument('--save_file_name', type=str, help='set output file name for original input',
                    default='mouse_deltas.npy')
parser.add_argument('--rdp_file_name', type=str, help='set output file name for rdp', default='rdp_deltas.npy')
parser.add_argument('--ai_file_name', type=str, help='set output file name for AI drawing', default='ai_deltas.npy')
args = parser.parse_args()

if __name__ == "__main__":
    painter = MP.MousePainter(args)
    while not painter.exit:
        painter.run()
        # self.current_frame_index == 1 : Mouse Drawing -> RDP
        # self.current_frame_index == 2 : RDP algorithm -> AI
        # self.current_frame_index == 0 : AI -> Mouse Drawing
        if painter.current_frame_index == 0:
            print("wait for drawing reconstruction")
            print(painter.save_file_name)
            painter.load_and_reconstruct(filename=painter.save_file_name)
            #painter.deltas_draw = painter.load_and_reconstruct(filename=painter.save_file_name)
        elif painter.current_frame_index == 1:
            print("wait for RDP")
            rdp_final(painter.save_file_name, painter.rdp_file_name)
            print(painter.rdp_file_name)
            painter.load_and_reconstruct(filename=painter.rdp_file_name)
            #painter.deltas_rdp = painter.load_and_reconstruct(filename=painter.rdp_file_name)
        else:
            print("wait for AI")
            print(painter.ai_file_name)
            painter.load_and_reconstruct(filename=painter.ai_file_name)
            #painter.deltas_ai = painter.load_and_reconstruct(filename=painter.ai_file_name)

        painter.running = True
    #print("Loop termination check")