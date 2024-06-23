import plotly.express as px


class ColorGird:
    """
    Colors represented by numbers, 0-10
    Grid represented by 2D list of colors

    Example grid: [[[0, 7, 7], [7, 7, 7], [0, 7, 7]]]
    """

    def __init__(self, grid):
        self.grid = grid
        self.colors = sorted(set([color for row in grid for color in row]))

    def __repr__(self):
        repr = ""
        for row in self.grid:
            repr += f"{row}\n"
        return repr

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        return self.grid == other.grid

    def __ne__(self, other):
        return not self.__eq__(other)

    def show(self):
        fig = px.imshow(
            self.grid,
            range_color=[0, 10],
            color_continuous_scale=[
                "black",
                "blue",
                "red",
                "green",
                "yellow",
                "grey",
                "pink",
                "orange",
                "teal",
                "maroon",
            ],
        )

        return fig


class InputOutputPair:
    def __init__(self, input, output):
        self.input = ColorGird(input)
        self.output = ColorGird(output)

    def __repr__(self):
        return f"Input:\n{self.input}\nOutput:\n{self.output}"

    def __str__(self):
        return self.__repr__()

    def show(self):
        print("Input:")
        self.input.show().show()

        print("Output:")
        self.output.show().show()
