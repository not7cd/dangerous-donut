import logging
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import scrolledtext as tkst

from io import StringIO
import sys
import os

from simulation.world import World
from simulation.coordinate import GridCoordinate as Coord
from simulation.life import *

WORLD_DIMENSION = (5, 5)

logging.basicConfig(level=logging.DEBUG)


class Dialog(tk.Toplevel):

    def __init__(self, parent, title = None):
        super(Dialog, self).__init__(parent)
        self.transient(parent)

        if title:
            self.title(title)

        self.parent = parent

        self.result = None

        body = tk.Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))

        self.initial_focus.focus_set()

        self.wait_window(self)

    #
    # construction hooks

    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden

        pass

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons

        box = tk.Frame(self)

        w = tk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    #
    # standard button semantics

    def ok(self, event=None):

        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        self.apply()

        self.cancel()

    def cancel(self, event=None):

        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    #
    # command hooks

    def validate(self):

        return 1 # override

    def apply(self):

        pass # override


class WorldSizeDialog(Dialog):

    def body(self, master):

        tk.Label(master, text="X:").grid(row=0)
        tk.Label(master, text="Y:").grid(row=1)

        self.e1 = tk.Entry(master)
        self.e2 = tk.Entry(master)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        return self.e1 # initial focus

    def apply(self):
        x = int(self.e1.get())
        y = int(self.e2.get())

        self.result = (x, y)


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



class WorldBoard(tk.Frame):
    def __init__(self, master=None, dimensions=WORLD_DIMENSION):
        super().__init__(master)
        self.dimensions = dimensions
        self.btns = {}
        self.rows = []

        for y in range(dimensions[1]):
            row = tk.Frame(self)
            row.grid(row=y, column=0)
            # padding = 1 if y % 2 else 0
            # row.grid(row=y, column=padding, columnspan=2)


            # padding = 0 if y % 2 else 2
            # bumper = tk.Frame(self, width=20, height=20).grid(row=y, column=padding)

            for x in range(dimensions[0]):
                btn = ttk.Button(row)
                btn["text"] = "{},{}".format(x, y)
                btn.grid(row=0, column=x)
                self.btns[Coord(x, y)] = btn



    def update_with(self, board):
        for coord in self.btns:
            if board.is_occupied(coord):
                organism = board.get_by_coord(coord)
                self.btns[coord]["text"] = str(organism)
                # self.btns[coord]["fg"] = organism.color
            else:
                self.btns[coord]["text"] = "."


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

        
        # self.board_diplay.pack(side="right")

    def create_world(self, dimensions=WORLD_DIMENSION):
        self.dimensions = dimensions
        world = World(dimensions)

        world.generate()

        self.world = world

        self.board_diplay = WorldBoard(self, dimensions)
        self.board_diplay.config(bg="black")
        self.board_diplay.pack(side="right")
        self.update_board()

    def turn(self):
        self.world.turn()
        self.turn_btn["text"] = "TURN {}".format(self.world.turn_count)
        self.update_board()

    def update_board(self):
        self.world.print_board()
        self.board_diplay.update_with(self.world.board)



if __name__ == "__main__":

    root = tk.Tk()
    ttk.Style().configure("TButton", padding=1, width=1, height=15, relief="flat", background="green")

    app = Application(master=root)

    logging_st = tkst.ScrolledText(app, state="disabled")
    logging_st.configure(font="TkDefaultFont")
    logging_st.pack(side="left")

    # Create textLogger
    text_handler = TextHandler(logging_st)

    # Add the handler to logger
    logger = logging.getLogger()
    logger.addHandler(text_handler)

    dialog = WorldSizeDialog(root)
    app.create_world(dialog.result)

    app.mainloop()
