import tkinter as tk
import numpy as np
import argparse
from CapUI.utils import misc
import sys


class MousePainter:
    def __init__(self, args):
        self.running = True
        self.exit = False
        self.save_index = 0
        self.ai_index = 0
        # number of strokes to generate
        self.stroke_number = 3
        # tkinter initialize
        self.root = tk.Tk()
        # Set the title of the window
        self.root.title("Stroke-based Collaborative Drawing of AI and Human")

        # drawing frame, RDP frame, AI frame
        self.frame_draw = tk.Frame(self.root)
        self.frame_rdp = tk.Frame(self.root)
        self.frame_ai = tk.Frame(self.root)

        # Grid frames horizontally
        self.frame_draw.grid(row=0, column=0, sticky="new")
        self.frame_rdp.grid(row=0, column=1, sticky="new")
        self.frame_ai.grid(row=0, column=2, sticky="new")

        # --savefile_name to change the name of the stroke npy file
        self.save_file_name = args.save_file_name
        self.rdp_file_name = args.rdp_file_name
        self.ai_file_name = args.ai_file_name

        # initialize canvas
        self.frame_draw_init()
        self.frame_rdp_init()
        self.frame_ai_init()

        # current_frame_index
        # == 0 : draw enabled
        # == 1, 2 : drawing deactivated
        self.current_frame_index = 0
        self.frames = [self.frame_draw, self.frame_rdp, self.frame_ai]

        self.create_buttons()
        self.init_drawing_vars()

    # initialize last_x, last_y, is_pressed, deltas
    def init_drawing_vars(self):
        # initialize all drawings
        self.last_x = 0
        self.last_y = 0
        self.is_pressed = False
        self.deltas_draw = []
        self.deltas_rdp = []
        self.deltas_ai = []

    # Initialize the buttons
    def create_buttons(self):
        # Create buttons
        self.next_button = tk.Button(self.root, text="Next Step", command=self.next_application)
        self.save_button = tk.Button(self.root, text="Save Process / Results", command=self.save_application)
        self.exit_button = tk.Button(self.root, text="Press here to Exit", command=self.exit_application)

        # Place buttons
        self.next_button.grid(row=1, column=0, sticky="ew")
        self.save_button.grid(row=1, column=1, sticky="ew")
        self.exit_button.grid(row=1, column=2, sticky="ew")

    # Initialize for stroke drawing
    def frame_draw_init(self):
        self.frame_draw.label_frame = tk.LabelFrame(self.frame_draw, text="Drawing with Mouse")
        self.frame_draw.label_frame.grid(row=0, column=0, columnspan=3, sticky="nsew")

        self.frame_draw.canvas = tk.Canvas(self.frame_draw.label_frame, width=256, height=256, bg="white")
        self.frame_draw.canvas.grid(row=1, column=0, sticky="nsew")

        self.frame_draw.canvas.bind("<Button-1>", self.start_paint)
        self.frame_draw.canvas.bind("<ButtonRelease-1>", self.stop_paint)
        self.frame_draw.canvas.bind("<B1-Motion>", self.paint)

        erase_button = tk.Button(self.frame_draw, text="Erase", command=self.clear_canvas)
        erase_button.grid(row=2, column=0, sticky="se")

        save_button = tk.Button(self.frame_draw, text="Save Deltas", command=self.save_deltas)
        save_button.grid(row=2, column=1, sticky="se")

    # button Implementation!!!!!!
    def frame_rdp_init(self):
        self.frame_rdp.label_frame = tk.LabelFrame(self.frame_rdp, text="Drawing after RDP")
        self.frame_rdp.label_frame.grid(row=0, column=0, sticky="nsew")

        self.frame_rdp.canvas = tk.Canvas(self.frame_rdp.label_frame, width=256, height=256, bg="white")
        self.frame_rdp.canvas.grid(row=1, column=0, sticky="nsew")

    # Initialize for AI drawing
    def frame_ai_init(self):
        self.frame_ai.label_frame = tk.LabelFrame(self.frame_ai, text="Drawing after AI")
        self.frame_ai.label_frame.grid(row=0, column=0, sticky="nsew")

        self.frame_ai.canvas = tk.Canvas(self.frame_ai.label_frame, width=256, height=256, bg="white")
        self.frame_ai.canvas.grid(row=1, column=0, sticky="nsew")

    # load npy file and draw
    def load_and_reconstruct(self, filename='mouse_deltas.npy'):
        try:
            if self.current_frame_index == 0:
                self.deltas_draw = np.load(filename, allow_pickle=True, encoding='latin1')
                if isinstance(self.deltas_draw, np.ndarray):
                    self.deltas_draw = self.deltas_draw.tolist()
                if self.deltas_draw is not None:
                    self.reconstruct_drawing(self.frame_draw.canvas)
            elif self.current_frame_index == 1:
                self.deltas_rdp = np.load(filename, allow_pickle=True, encoding='latin1')
                if self.deltas_rdp is not None:
                    self.reconstruct_drawing(self.frame_rdp.canvas)
            else:
                self.deltas_ai = np.load(filename, allow_pickle=True, encoding='latin1')
                if self.deltas_ai is not None:
                    self.reconstruct_drawing(self.frame_ai.canvas)
        except FileNotFoundError:
            print("No saved data file found.")

    # called from load_and_reconstruct function
    def reconstruct_drawing(self, canvas=None):
        canvas.delete("all")
        if self.current_frame_index == 0:
            deltas = self.deltas_draw
        elif self.current_frame_index == 1:
            deltas = self.deltas_rdp
        else:
            deltas = self.deltas_ai
        if len(deltas) == 0:
            print("No input data.")
            return
        start_x = start_y = current_x = current_y = 0
        for dx, dy, mouse_button_pressed in deltas:
            # Update current coordinates
            current_x += dx
            current_y += dy

            # If the mouse button was pressed, draw a line
            if not mouse_button_pressed:
                canvas.create_line(start_x, start_y, current_x, current_y, fill="black", width=2)

            start_x, start_y = current_x, current_y

    # paint with a mouse
    def paint(self, event):
        if self.current_frame_index != 0:
            return
        x, y = event.x, event.y
        dx = x - self.last_x
        dy = y - self.last_y
        # print("paint function called", self.deltas_draw)
        self.deltas_draw.append((dx, dy, not self.is_pressed))
        if self.is_pressed:
            self.frame_draw.canvas.create_line((self.last_x, self.last_y, x, y), fill="black", width=2)
        # else:
            # print("from print function : last_x, last_y", self.last_x, self.last_y)
        self.last_x, self.last_y = x, y

    # called when mouse button first pressed
    def start_paint(self, event):
        if self.current_frame_index != 0:
            return
        # print("Type of arr:", type(self.deltas_draw))
        # print("start_paint function called")
        dx = event.x - self.last_x
        dy = event.y - self.last_y
        # print("(last x, last y)", self.last_x, self.last_y)
        # print("(event x, event y)", event.x, event.y)
        # print("append", dx, dy, not self.is_pressed)
        self.deltas_draw.append((dx, dy, not self.is_pressed))
        self.last_x, self.last_y = event.x, event.y
        self.is_pressed = True

    # called when mouse button unpressed
    def stop_paint(self, event):
        if self.current_frame_index != 0:
            return
        # print("stop_paint function called,\n (last x, last y)", self.last_x, self.last_y)
        self.is_pressed = False

    # called with the button in frame_draw
    def save_deltas(self):
        if self.current_frame_index != 0:
            return
        np.save(self.save_file_name, np.array(self.deltas_draw))

    # run while self.running == True
    def run(self):
        while self.running:
            self.root.mainloop()

    # called with the button erase in frame_draw
    def clear_canvas(self):
        if self.current_frame_index != 0:
            return
        # Delete all items drawn on the canvas
        self.frame_draw.canvas.delete("all")
        self.init_drawing_vars()

    # called with next_button -> stop the tkinter and return to main function
    def next_application(self):
        # print(self.current_frame_index, self.frames[self.current_frame_index])
        # self.current_frame_index == 0 : Mouse Drawing -> RDP
        # self.current_frame_index == 1 : RDP algorithm -> AI
        # self.current_frame_index == 2 : AI -> Mouse Drawing
        self.current_frame_index = (self.current_frame_index + 1) % len(self.frames)
        self.running = False
        self.root.quit()

    def save_application(self):
        misc.save_with_indexed_directory("results", self.save_index, self.save_file_name, self.deltas_draw)
        misc.save_with_indexed_directory("results", self.save_index, self.rdp_file_name, self.deltas_rdp)
        misc.save_with_indexed_directory("results", self.save_index, self.ai_file_name, self.deltas_ai)
        self.save_index += 1

    # called with the button exit in every frame
    def exit_application(self):
        self.exit = True
        self.running = False
        self.root.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # Evaluation input filepaths
    parser.add_argument('--save_file_name', type=str, help='set output file name for original input',
                        default='mouse_deltas.npy')
    parser.add_argument('--rdp_file_name', type=str, help='set output file name for rdp', default='rdp_deltas.npy')
    parser.add_argument('--ai_file_name', type=str, help='set output file name for AI drawing', default='ai_deltas.npy')
    args = parser.parse_args()

    painter = MousePainter(args)
    painter.run()
