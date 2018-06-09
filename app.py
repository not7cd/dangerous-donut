import logging
import tkinter as tk
from tkinter import scrolledtext as tkst

from io import StringIO
import sys

from simulation.world import World
from simulation.life import *
WORLD_DIMENSION = (30, 30)

logging.basicConfig(level=logging.DEBUG)


class TextHandler(logging.Handler):
    """This class allows you to log to a Tkinter Text or ScrolledText widget"""

    def __init__(self, text):
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        # Store a reference to the Text it will log to
        self.text = text

    def emit(self, record):
        msg = self.format(record)

        def append():
            self.text.configure(state="normal")
            self.text.insert(tk.END, msg + "\n")
            self.text.configure(state="disabled")
            # Autoscroll to the bottom
            self.text.yview(tk.END)

        # This is necessary because we can't modify the Text from other threads
        self.text.after(0, append)


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.pack()
        self.create_widgets()

    def create_widgets(self):

        self.turn_btn = tk.Button(self)
        self.turn_btn["text"] = "TURN ME ON"
        self.turn_btn["command"] = self.turn
        self.turn_btn.pack(side="bottom")

        self.quit_btn = tk.Button(self, text="QUIT", fg="red", command=root.destroy)
        self.quit_btn.pack(side="bottom")

        self.board_diplay = tkst.ScrolledText(self, state="disabled")
        self.board_diplay.configure(font="TkFixedFont")
        self.board_diplay.pack(side="right")

    def create_world(self):
        world = World(WORLD_DIMENSION)

        factory = OrganismFactory(WORLD_DIMENSION)

        for o in factory.generate(Plant, 10):
            world.board.place_org(o)

        for o in factory.generate(SuperPlant, 3):
            world.board.place_org(o)

        for o in factory.generate(Animal, 15):
            world.board.place_org(o)

        self.world = world
        self.update_board()

    def turn(self):
        self.world.turn()
        self.turn_btn["text"] = "TURN {}".format(self.world.turn_count)
        self.update_board()

    def update_board(self):
        # crude hack, get board from stdout
        default_stdout = sys.stdout
        sys.stdout = board_stdout = StringIO()
        self.world.print_board()
        sys.stdout = default_stdout

        # update board
        self.board_diplay.config(state=tk.NORMAL)
        self.board_diplay.delete(1.0, tk.END)
        self.board_diplay.insert(tk.END, board_stdout.getvalue())
        self.board_diplay.config(state=tk.DISABLED)
        


if __name__ == "__main__":

    root = tk.Tk()
    app = Application(master=root)

    st = tkst.ScrolledText(app, state="disabled")
    st.configure(font="TkFixedFont")
    st.pack()

    # Create textLogger
    text_handler = TextHandler(st)

    # Add the handler to logger
    logger = logging.getLogger()
    logger.addHandler(text_handler)

    app.create_world()
    app.mainloop()
