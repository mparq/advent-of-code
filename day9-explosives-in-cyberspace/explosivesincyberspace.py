#!/usr/bin/python3
"""adventofcode.com/2016/day/9

Part One
--
Input should be tokenized to create a large list that ends up being joined together to form the
output string. Input is given as one long string.
"""


FILENAME = "input.txt"


def parse_marker(input_buffer):
    """Return the parsed argument of marker (AxB) where A = num chars and B = repeat times.

    Function will be called when the opening paren of a marker has already been read, so we must
    read until the closing paren and then parse AxB string.
    """
    marker_text = ""
    char = input_buffer.read(1)
    while char != ")":
        marker_text += char
        char = input_buffer.read(1)
    return tuple(int(num) for num in marker_text.split("x"))


def read_and_repeat(input_buffer, num_chars, repeat):
    """Return a decompressed string from the file given the parameters."""
    read_chars = input_buffer.read(num_chars)
    return read_chars * repeat


def decompress_helper(input_buffer):
    """Return list of strings to be added to decompressed string after parsing a marker.

    This function must be called as we enter a marker (after reading opening paren). We will
    parse the marker components (AxB) where A is chars to read and B is number of times to repeat.
    After that, read and return the next A chars repeated B times in a list.
    """
    num_chars_to_read, repeat = parse_marker(input_buffer)
    return read_and_repeat(input_buffer, num_chars_to_read, repeat)


def decompress(input_buffer):
    """Parse input and output decompressed string."""
    finished = False
    decompressed = []
    while not finished:
        char = input_buffer.read(1)
        if char == "":
            finished = True

        # ignore whitespace
        elif char.isspace():
            continue

        else:
            if char == "(":
                # pass file buffer to helper function to parse marker and return repeated string
                decompressed.append(decompress_helper(input_buffer))
            else:
                decompressed.append(char)
    return "".join(decompressed)


if __name__ == "__main__":
    with open(FILENAME) as input_file:
        print("Length of compressed file (with markers): {}".format(len(input_file.read().strip())))
    with open(FILENAME) as input_file:
        decompressed_string = decompress(input_file)
        print(decompressed_string[:200])
        print("The length of the decompressed string is {}".format(len(decompressed_string)))
