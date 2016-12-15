#!/usr/bin/python3
"""adventofcode.com/2016/day/8

Part One
--
Need to parse input instructions into commands. These commands will be
fed to an object representing the display screen (of class TinyLED).abs
This object will keep track of the screen's display state.
"""


FILENAME = "input.txt"


class TinyLED:
    """Data structure representing the led screen specified in puzzle.

    Instance variables:
    board -- 2d list representing the led pixel screen
    width -- width of screen
    height -- height of screen
    num_pixels_on -- number of pixels that are ON in the screen

    Instance methods:
    rect -- turns on all pixels in a rectangle at top-left of screen
    rotate_row -- shifts pixels right in a row, rotating at boundary
    rotate_column -- shifts pixels down in a column, rotating at boundary
    print_screen -- prints led screen in a human-friendly format
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = [[False for j in range(width)] for i in range(height)]

    @property
    def num_pixels_on(self):
        """Return number of pixels that are marked ON in screen."""
        return sum(sum(1 for cell in row if cell) for row in self.screen)

    def rect(self, width, height):
        """Turn ON pixels in a rectangle at top-left of screen.

        Rectangle dimensions determined by input. Assume that the input
        rectangle falls within the dimensions of the screen.
        """
        for i in range(height):
            for j in range(width):
                self.screen[i][j] = True

    def rotate_row(self, row, shift):
        """Shift pixels right in the row, rotating at boundary.

        Pixels that would fall off the right end appear at the left end
        of the row after rotating. Assume that row falls within screen
        dimensions.

        We first determine which pixels are ON in the row, then we
        shift all those pixels rolling over at SCREENWIDTH
        """
        screen_row = self.screen[row]
        shifted_pixels = [(index + shift) % self.width
                          for index, pixel in enumerate(screen_row)
                          if pixel]
        for column in range(self.width):
            if column in shifted_pixels:
                self.screen[row][column] = True
            else:
                self.screen[row][column] = False

    def rotate_column(self, column, shift):
        """Shift pixels down in the column, rotating at boundary.

        Pixels that would fall off the bottom appear at the top of the
        column after rotating. Assume that column falls within screen
        dimensions.

        We first determine which pixels are ON in the row, then we
        shift all those pixels rolling over at SCREENWIDTH
        """
        on_pixels = (index for index in range(self.height)
                     if self.screen[index][column])
        shifted_pixels = [(index + shift) % self.height
                          for index in on_pixels]
        for row in range(self.height):
            if row in shifted_pixels:
                self.screen[row][column] = True
            else:
                self.screen[row][column] = False

    def print_screen(self):
        """Print pretty-formatted state of led screen."""
        for row in self.screen:
            print(" ".join("#" if cell else "." for cell in row))


if __name__ == "__main__":
    with open(FILENAME) as inputFile:
        for line in inputFile:
            print(line.strip())
