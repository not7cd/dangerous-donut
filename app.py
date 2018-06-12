import logging
import tkinter as tk
import tkinter.ttk as ttk

from gui import Dialog, TextHandler, BoardStylist, LoggerScrolledText
from gui.board import WorldBoard

WORLD_DIMENSION = (16, 16)

logging.basicConfig(level=logging.INFO)


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


class Application(tk.Frame):
    def __init__(self, master=None):
        super(Application, self).__init__(master)
        self.world = None
        self.autoplay = tk.BooleanVar()

        self.pack()
        self.create_widgets()
        self.place()

    def create_widgets(self):
        """create and bind control buttons and place them"""
        self.turn_btn = ttk.Button(
            self, text="TURN", command=self.turn, style="TButton"
        )
        self.quit_btn = ttk.Button(
            self, text="QUIT", command=root.destroy, style="TButton"
        )
        self.regen_btn = ttk.Button(self, text="REGENERATE", style="TButton")

        self.play_btn = tk.Checkbutton(
            self,
            text="PLAY",
            variable=self.autoplay,
            command=self.autoplay_turn,
            onvalue=True,
            offvalue=False,
        )

        self.logging_text = LoggerScrolledText(self)

        self.board_display = WorldBoard(self, WORLD_DIMENSION)

    def create_world(self, dimensions=WORLD_DIMENSION):
        """construct world, create board"""
        if self.world:
            raise Exception("world exists")

        self.world.generate()

        self.regen_btn["command"] = self.regen_world

        BoardStylist(self.world.factory.organisms)

        self.update_board()
        self.place()

    def place(self):
        self.board_display.pack(side="right", padx=10, pady=10)
        self.logging_text.pack(side="top")
        self.turn_btn.pack(side="left", padx=5)
        self.play_btn.pack(side="left", padx=5)
        self.quit_btn.pack(side="left", padx=5)
        self.regen_btn.pack(side="left", padx=5)

    def turn(self):
        """Will execute world turn and update UI board with data from world"""
        self.world.turn()
        self.turn_btn["text"] = "TURN {}".format(self.world.turn_count)
        self.update_board()

    def update_board(self):
        self.board_display.update_with(self.world.board)

    def regen_world(self):
        self.world.generate()
        self.world.turn_count = 0
        self.update_board()

    def autoplay_turn(self):
        if self.autoplay.get():
            self.turn()
            self.after(200, self.autoplay_turn)


if __name__ == "__main__":

    root = tk.Tk()
    root.title("Dangerous Donut")

    app = Application(master=root)

    # create logging handler from text widget inside app
    logger = logging.getLogger()
    logger.addHandler(TextHandler(app.logging_text))

    # ask for initial conditions and create world with them
    # dialog = WorldSizeDialog(root, "Enter world size")
    # app.create_world(dialog.result)

    # enter main loop
    app.mainloop()
