import tkinter as tk
import numpy as np
import argparse

class MousePainter:
    def __init__(self, args):
        self.root = tk.Tk()
        # drawing frame, RDP frame, AI frame
        self.frame_draw = tk.Frame(self.root)
        self.frame_rdp = tk.Frame(self.root)
        self.frame_ai = tk.Frame(self.root)

        self.current_frame_index = 0
        self.frames = [self.frame_draw, self.frame_rdp, self.frame_ai]

        # --savefile_name to change the name of the stroke npy file
        self.save_file_name = args.save_file_name
        self.rdp_file_name = args.rdp_file_name
        self.ai_file_name = args.ai_file_name

        self.last_x = 0
        self.last_y = 0
        self.is_pressed = False

        # ( dx, dy, penstate )
        self.deltas = []

        # initialize canvas
        self.frame_draw_init()
        self.frame_rdp_init()
        self.frame_ai_init()

    # initialize last_x, last_y, is_pressed, deltas
    def init_drawing_vars(self):
        # initialize all drawings
        self.last_x = 0
        self.last_y = 0
        self.is_pressed = False
        self.deltas = []

    # Initialize for stroke drawing
    # button !!!!!!
    def frame_draw_init(self):
        self.frame_draw.root = self.root
        self.frame_draw.root.title("Drawing with Mouse")

        self.frame_draw.canvas = tk.Canvas(self.frame_draw.root, width=256, height=256, bg="white")
        self.frame_draw.canvas.pack()

        self.frame_draw.canvas.bind("<Button-1>", self.start_paint)
        self.frame_draw.canvas.bind("<ButtonRelease-1>", self.stop_paint)
        self.frame_draw.canvas.bind("<B1-Motion>", self.paint)

        self.frame_draw.erase_button = tk.Button(self.frame_draw.root, text="Erase", command=self.init_drawing_vars)
        self.frame_draw.erase_button.pack(side="left")

        self.frame_draw.exit_button = tk.Button(self.frame_draw.root, text="Exit", command=self.exit_application)
        self.frame_draw.exit_button.pack(side="left")

        self.frame_draw.save_button = tk.Button(self.frame_draw.root, text="Save Deltas", command=self.save_deltas)
        self.frame_draw.save_button.pack(side="left")

    # button Implementation!!!!!!
    def frame_rdp_init(self):
        self.frame_rdp.root = self.root
        self.frame_rdp.root.title("Drawing after RDP")

        self.frame_rdp.canvas = tk.Canvas(self.frame_rdp.root, width=256, height=256, bg="white")
        self.frame_rdp.canvas.pack()

        self.frame_rdp.next_button = tk.Button(self.frame_rdp.root, text="Next", command=self.init_drawing_vars)
        self.frame_rdp.next_button.pack(side="left")

        self.frame_rdp.exit_button = tk.Button(self.frame_rdp.root, text="Exit", command=self.exit_application)
        self.frame_rdp.exit_button.pack(side="left")

        self.load_and_reconstruct(current_frame=self.frame_rdp, filename=self.rdp_file_name)

    # button Implementation!!!!!!
    def frame_ai_init(self):
        self.frame_ai.root = self.root
        self.frame_ai.root.title("Drawing after AI")

        self.frame_ai.canvas = tk.Canvas(self.frame_ai.root, width=256, height=256, bg="white")
        self.frame_ai.canvas.pack()

        self.frame_ai.next_button = tk.Button(self.frame_ai.root, text="Next", command=self.init_drawing_vars)
        self.frame_ai.next_button.pack(side="left")

        self.frame_ai.exit_button = tk.Button(self.frame_ai.root, text="Exit", command=self.exit_application)
        self.frame_ai.exit_button.pack(side="left")

        self.load_and_reconstruct(current_frame=self.frame_ai, filename=self.ai_file_name)

    # load npy file and draw
    def load_and_reconstruct(self, current_frame, filename='mouse_deltas.npy'):
        try:
            self.deltas = np.load(filename)
            self.reconstruct_drawing(current_frame)
        except FileNotFoundError:
            print("No saved data file found.")

    def paint(self, event):
        x, y = event.x, event.y
        dx = x - self.last_x
        dy = y - self.last_y
        self.deltas.append((dx, dy, not self.is_pressed))
        if self.is_pressed:
            self.canvas.create_line((self.last_x, self.last_y, x, y), fill="black", width=2)
        self.last_x, self.last_y = x, y

    # called from load_and_reconstruct function
    def reconstruct_drawing(self, current_frame):
        data = self.deltas
        if len(data) == 0:
            print("No input data.")
            return

        for i in range(len(data) - 1):
            x1, y1, pen_state1 = data[i]
            x2, y2, pen_state2 = data[i + 1]
            if pen_state1 == 0:
                current_frame.root.create_line(x1, y1, x2, y2, fill="black", width=2)

    # called from paint function
    def start_paint(self, event):
        dx = event.x - self.last_x
        dy = event.y - self.last_y
        self.deltas.append((dx, dy, not self.is_pressed))
        self.last_x, self.last_y = event.x, event.y
        self.is_pressed = True

    # called from paint function
    def stop_paint(self, event):
        self.is_pressed = False

    # called with the button in frame_draw
    def save_deltas(self):
        np.save( self.save_file_name, np.array(self.deltas))

    def run(self):
        self.root.mainloop()

    # called with the button exit in every frame
    def exit_application(self):
        self.root.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # Evaluation input filepaths
    parser.add_argument('--savefile_name', type=str, help='set output file name for original input', default='mouse_deltas.npy')
    parser.add_argument('--rdp_file_name', type=str, help='set output file name for rdp', default='rdp_deltas.npy')
    parser.add_argument('--ai_file_name', type=str, help='set output file name for AI drawing', default='ai_deltas.npy')
    args = parser.parse_args()

    painter = MousePainter(args)
    painter.run()

