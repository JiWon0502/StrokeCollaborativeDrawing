import tkinter as tk
import numpy as np
import argparse

class MousePainter:
    def __init__(self, args):
        self.root = tk.Tk()
        # Set the title of the window
        self.root.title("Stroke-based Collaborative Drawing of AI and Human")
        self.running = True
        self.exit = False

        # drawing frame, RDP frame, AI frame
        self.frame_draw = tk.Frame(self.root)
        self.frame_rdp = tk.Frame(self.root)
        self.frame_ai = tk.Frame(self.root)

        # Grid frames horizontally
        self.frame_draw.grid(row=0, column=0, sticky="new")
        self.frame_rdp.grid(row=0, column=1, sticky="new")
        self.frame_ai.grid(row=0, column=2, sticky="new")

        self.current_frame_index = 0
        self.frames = [self.frame_draw, self.frame_rdp, self.frame_ai]

        # --savefile_name to change the name of the stroke npy file
        self.save_file_name = args.save_file_name
        self.rdp_file_name = args.rdp_file_name
        self.ai_file_name = args.ai_file_name

        # initialize canvas
        self.frame_draw_init()
        self.frame_rdp_init()
        self.frame_ai_init()

        self.create_buttons()
        self.init_drawing_vars()

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
        save_button.grid(row=2, column=1,sticky="se")

    # button Implementation!!!!!!
    def frame_rdp_init(self):
        label_frame = tk.LabelFrame(self.frame_rdp, text="Drawing after RDP")
        label_frame.grid(row=0, column=0, sticky="ew")

        canvas = tk.Canvas(label_frame, width=256, height=256, bg="white")
        canvas.grid(row=1, column=0, columnspan=2)

        #exit_button = tk.Button(label_frame, text="Exit", command=self.exit_application)
        #exit_button.grid(row=2, column=0)

    # Initialize for AI drawing
    def frame_ai_init(self):
        label_frame = tk.LabelFrame(self.frame_ai, text="Drawing after AI")
        label_frame.grid(row=0, column=0, sticky="ew")

        canvas = tk.Canvas(label_frame, width=256, height=256, bg="white")
        canvas.grid(row=1, column=0, columnspan=2)

        #exit_button = tk.Button(label_frame, text="Exit", command=self.exit_application)
        #exit_button.grid(row=2, column=0)

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
            self.frame_draw.canvas.create_line((self.last_x, self.last_y, x, y), fill="black", width=2)
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

    # run while self.running == True
    def run(self):
        while self.running :
            self.root.mainloop()
        else :
            self.root.quit()

    # called with the button erase in frame_draw
    def clear_canvas(self):
        # Delete all items drawn on the canvas
        self.frame_draw.canvas.delete("all")

    # called with next_button -> stop the tkinter and return to main function
    def next_application(self):
        print(self.current_frame_index, self.frames[self.current_frame_index])
        # self.current_frame_index == 0 : Mouse Drawing -> RDP
        # self.current_frame_index == 1 : RDP algorithm -> AI
        # self.current_frame_index == 2 : AI -> Mouse Drawing
        self.running = False
        self.current_frame_index = (self.current_frame_index + 1) % len(self.frames)

    def save_application(self):
        pass

    # called with the button exit in every frame
    def exit_application(self):
        self.exit = True
        self.root.quit()

    # initialize last_x, last_y, is_pressed, deltas
    def init_drawing_vars(self):
        # initialize all drawings
        self.last_x = 0
        self.last_y = 0
        self.is_pressed = False
        self.deltas = []


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # Evaluation input filepaths
    parser.add_argument('--save_file_name', type=str, help='set output file name for original input', default='mouse_deltas.npy')
    parser.add_argument('--rdp_file_name', type=str, help='set output file name for rdp', default='rdp_deltas.npy')
    parser.add_argument('--ai_file_name', type=str, help='set output file name for AI drawing', default='ai_deltas.npy')
    args = parser.parse_args()

    painter = MousePainter(args)
    painter.run()

