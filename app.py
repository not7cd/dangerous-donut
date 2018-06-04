import tkinter as tk

from io import StringIO
import sys


from simulation.world import World
from simulation.life import *

WORLD_DIMENSION = (20, 20)
TURNS = 20

world = World(WORLD_DIMENSION)

factory = OrganismFactory(WORLD_DIMENSION)

world.organisms += list(factory.generate(Organism, 5))
world.organisms += list(factory.generate(Plant, 5))
world.organisms += list(factory.generate(Animal, 5))
world.organisms += list(factory.generate(Wolf, 5))



class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):

        self.entrythingy = tk.Entry()
        self.entrythingy.pack()

        # here is the application variable
        self.contents = tk.StringVar()
        # set it to some value
        self.contents.set('huh')
        # tell the entry widget to watch this variable
        self.entrythingy["textvariable"] = self.contents

        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.turn
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=root.destroy)
        self.quit.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")

    def turn(self):
        world.turn()

        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()

        world.print_board()

        sys.stdout = old_stdout

        self.contents.set(mystdout.getvalue())  




root = tk.Tk()
app = Application(master=root)
app.mainloop()