import MousePainter as MP
import argparse

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
        # self.current_frame_index == 0 : Mouse Drawing -> RDP
        # self.current_frame_index == 1 : RDP algorithm -> AI
        # self.current_frame_index == 2 : AI -> Mouse Drawing
        if painter.current_frame_index == 0 :
            pass
        elif painter.current_frame_index == 1:
            pass
        else :
            pass
        painter.running = True
