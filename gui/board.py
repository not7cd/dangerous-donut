import tkinter as tk

from gui import ToolTip


class FieldButton(tk.Button):
    """Wraped Button for easier size manipulation"""

    def __init__(self, master, height=20, width=20, **kwargs):
        self.wrapper = tk.Frame(master, height=height, width=width)
        self.wrapper.pack_propagate(False)

        super(FieldButton, self).__init__(self.wrapper, **kwargs)
        super(FieldButton, self).pack(fill=tk.BOTH, expand=1)

    def grid(self, *args, **kwargs):
        # passing position config to wrapper
        self.wrapper.grid(*args, **kwargs)

    def pack(self, *args, **kwargs):
        # passing position config to wrapper
        self.wrapper.pack(*args, **kwargs)

    def config(self, height=None, width=None, **kwargs):
        # passing height, width config to wrapper
        if height:
            self.wrapper.config(height=height)
        if width:
            self.wrapper.config(width=width)
        super(FieldButton, self).config(**kwargs)


class WorldBoard(tk.Frame):
    def __init__(self, master=None, dimensions=(16, 16)):
        """
        :param master: parent widget
        :param dimensions: tuple of world size (x, y)
        """
        super(WorldBoard, self).__init__(master)
        self.dimensions = dimensions
        self.btns = {}

        self.build_grid()

    def build_grid(self):
        """build grid of buttons"""
        if self.btns:
            raise Exception("grid exists")

        for y in range(self.dimensions[1]):
            row = tk.Frame(self)
            row.grid(row=y, column=0)

            for x in range(self.dimensions[0]):
                btn = FieldButton(row, text=" ")
                btn.grid(row=0, column=x)
                ToolTip(btn, msg="{}, {}".format(x, y), delay=0.1)

                self.btns[(x, y)] = btn

    def update_with(self, board):
        """
        update grid with data in board
        :param board: board object with accessible by coord
        """
        for coord in self.btns:
            if board.is_occupied(coord):
                organism = board.get_by_coord(coord)
                self.btns[coord]["text"] = str(organism)
                self.btns[coord]["style"] = "{}.Board.TButton".format(
                    organism.__class__.__name__
                )
            else:
                self.btns[coord]["text"] = " "
                self.btns[coord]["style"] = "Board.TButton"
