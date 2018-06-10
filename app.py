import logging
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import scrolledtext as tkst

from gui import Dialog, TextHandler
from simulation.coordinate import GridCoordinate as Coord
from simulation.world import World

WORLD_DIMENSION = (5, 5)

logging.basicConfig(level=logging.DEBUG)


class WorldSizeDialog(Dialog):
    def body(self, master):
        tk.Label(master, text="X:").grid(row=0)
        tk.Label(master, text="Y:").grid(row=1)

        self.e1 = tk.Entry(master)
        self.e2 = tk.Entry(master)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        return self.e1  # initial focus

    def validate(self):
        return int(self.e1.get()) > 0 and int(self.e2.get()) > 0

    def apply(self):
        x = int(self.e1.get())
        y = int(self.e2.get())

        self.result = (x, y)


class WorldBoard(tk.Frame):
    def __init__(self, master=None, dimensions=WORLD_DIMENSION, mode="grid"):
        """
        :param master: parent widget
        :param dimensions: tuple of world size (x, y)
        :param mode: "grid" or "hex"
        """
        super().__init__(master)
        self.dimensions = dimensions
        self.btns = {}
        self.display_mode = mode
        # self.rows = []

        self.build_grid()

    def build_grid(self):
        """build grid of buttons"""
        if self.btns:
            raise Exception("grid exists")
            # TODO: delete all children instead raising exc

        for y in range(self.dimensions[1]):
            row = tk.Frame(self)
            # TODO: should check for subclass of coord
            if self.display_mode == "grid":
                row.grid(row=y, column=0)
            elif self.display_mode == "hex":
                offset = 1 if y % 2 else 0
                row.grid(row=y, column=offset, columnspan=2)

                side = 0 if y % 2 else 2
                tk.Frame(self, width=7, height=20).grid(row=y, column=side)

            for x in range(self.dimensions[0]):
                btn = ttk.Button(row)
                btn["text"] = " "
                btn.grid(row=0, column=x)
                self.btns[Coord(x, y)] = btn

    def update_with(self, board):
        """
        update grid with data in board
        :param board: board object with accessible by coord
        """
        for coord in self.btns:
            if board.is_occupied(coord):
                organism = board.get_by_coord(coord)
                self.btns[coord]["text"] = str(organism)
                # self.btns[coord]["fg"] = organism.color
            else:
                self.btns[coord]["text"] = " "


class Application(tk.Frame):
    def __init__(self, master=None):
        super(Application, self).__init__(master)
        self.board_display = None
        self.quit_btn = None
        self.turn_btn = None

        self.logging_stext = None

        self.world = None

        self.pack()
        self.create_widgets()

    def create_widgets(self):
        """create and bind control buttons and place them"""
        self.turn_btn = tk.Button(self, text="TURN", command=self.turn)
        self.quit_btn = tk.Button(self, text="QUIT", fg="red",
                                  command=root.destroy)

        self.logging_stext = tkst.ScrolledText(self, state="disabled")
        self.logging_stext.configure(font="TkDefaultFont")

        self.logging_stext.pack(side="left")
        self.turn_btn.pack(side="bottom")
        self.quit_btn.pack(side="bottom")

    def create_world(self, dimensions=WORLD_DIMENSION):
        """construct world, create board"""
        if self.world:
            raise Exception("world exists")

        world = World(dimensions)
        world.generate()

        self.world = world

        self.board_display = WorldBoard(self, world.dimensions)
        self.board_display.pack(side="right", padx=10, pady=10)
        self.update_board()

    def turn(self):
        """Will execute world turn and update UI board with data from world"""
        self.world.turn()
        self.turn_btn["text"] = "TURN {}".format(self.world.turn_count)
        self.update_board()

    def update_board(self):
        self.board_display.update_with(self.world.board)


if __name__ == "__main__":

    root = tk.Tk()
    ttk.Style().configure(
        "TButton", padding=1, width=2, height=15, relief="flat", background="green"
    )

    app = Application(master=root)

    # create logging handler from text widget inside app
    text_handler = TextHandler(app.logging_stext)
    logger = logging.getLogger()
    logger.addHandler(text_handler)

    # ask for initial conditions and create world with them
    dialog = WorldSizeDialog(root, "Enter world size")
    app.create_world(dialog.result)

    # enter main loop
    app.mainloop()
