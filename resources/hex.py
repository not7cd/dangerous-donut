from tkinter import *


class HexaCanvas(Canvas):
    """ A canvas that provides a create-hexagone method """

    def __init__(self, master, *args, **kwargs):
        Canvas.__init__(self, master, *args, **kwargs)

        self.hexa_size = 20

    def set_hexa_size(self, number):
        self.hexa_size = number

    def create_hexagone(
        self,
        x,
        y,
        color="black",
        fill="blue",
        color1=None,
        color2=None,
        color3=None,
        color4=None,
        color5=None,
        color6=None,
    ):
        """ 
        Compute coordinates of 6 points relative to a center position.
        Point are numbered following this schema :

        Points in euclidiean grid:  
                    6

                5       1
                    .
                4       2

                    3

        Each color is applied to the side that link the vertex with same number to its following.
        Ex : color 1 is applied on side (vertex1, vertex2)

        Take care that tkinter ordinate axes is inverted to the standard euclidian ones.
        Point on the screen will be horizontally mirrored.
        Displayed points:

                    3
              color3/      \color2      
                4       2
            color4|     |color1
                5       1
              color6\      /color6
                    6

        """
        size = self.hexa_size
        δx = (size ** 2 - (size / 2) ** 2) ** 0.5

        point1 = (x + δx, y + size / 2)
        point2 = (x + δx, y - size / 2)
        point3 = (x, y - size)
        point4 = (x - δx, y - size / 2)
        point5 = (x - δx, y + size / 2)
        point6 = (x, y + size)

        # this setting allow to specify a different color for each side.
        if color1 is None:
            color1 = color
        if color2 is None:
            color2 = color
        if color3 is None:
            color3 = color
        if color4 is None:
            color4 = color
        if color5 is None:
            color5 = color
        if color6 is None:
            color6 = color

        self.create_line(point1, point2, fill=color1, width=2)
        self.create_line(point2, point3, fill=color2, width=2)
        self.create_line(point3, point4, fill=color3, width=2)
        self.create_line(point4, point5, fill=color4, width=2)
        self.create_line(point5, point6, fill=color5, width=2)
        self.create_line(point6, point1, fill=color6, width=2)

        if fill is not None:
            self.create_polygon(
                point1, point2, point3, point4, point5, point6, fill=fill
            )


class HexagonalGrid(HexaCanvas):
    """ A grid whose each cell is hexagonal """

    def __init__(self, master, scale, grid_width, grid_height, *args, **kwargs):

        δx = (scale ** 2 - (scale / 2.0) ** 2) ** 0.5
        width = 2 * δx * grid_width + δx
        height = 1.5 * scale * grid_height + 0.5 * scale

        HexaCanvas.__init__(
            self,
            master,
            background="white",
            width=width,
            height=height,
            *args,
            **kwargs
        )
        self.set_hexa_size(scale)

    def set_cell(self, x_cell, y_cell, *args, **kwargs):
        """
        Create a content in the cell of coordinates x and y.
        :param x_cell:
        :param y_cell:
        :param args:
        :param kwargs:
        :return:
        """

        # compute pixel coordinate of the center of the cell:
        size = self.hexa_size
        δx = (size ** 2 - (size / 2) ** 2) ** 0.5

        pix_x = δx + 2 * δx * x_cell
        if y_cell % 2 == 1:
            pix_x += δx

        pix_y = size + y_cell * 1.5 * size

        self.create_hexagone(pix_x, pix_y, *args, **kwargs)


if __name__ == "__main__":
    root = Tk()

    grid = HexagonalGrid(root, scale=20, grid_width=10, grid_height=10)
    grid.grid(row=0, column=0, padx=5, pady=5)

    def correct_quit(tk):
        tk.destroy()
        tk.quit()

    quit_btn = Button(root, text="Quit", command=lambda: correct_quit(root))
    quit_btn.grid(row=1, column=0)

    grid.set_cell(0, 0, fill="blue")
    grid.set_cell(1, 0, fill="red")
    grid.set_cell(0, 1, fill="green")
    grid.set_cell(1, 1, fill="yellow")
    grid.set_cell(2, 0, fill="cyan")
    grid.set_cell(0, 2, fill="teal")
    grid.set_cell(2, 1, fill="silver")
    grid.set_cell(1, 2, fill="white")
    grid.set_cell(2, 2, fill="gray")

    root.mainloop()
