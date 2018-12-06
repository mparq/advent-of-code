#!/usr/bin/python3
"""adventofcode.com/2016/day/9

Part One
--
Input should be tokenized to create a large list that ends up being joined together to form the
output string. Input is given as one long string.

Part Two
--
Should have known. We need to be smarter about parsing just for the length, rather
than building up another string. Seems suited for a recursive solution. I tried to
avoid reading the entire input into memory in the solution for part one, but it seems
like that's the way to go here. We could save in memory costs by creating a temporary
string every time we need to read characters in from a marker.

len(section)

length = 0
for char in section:
    if char != "(":
        length += 1
    else:
        length += parse_marker(section) 

for section in section:
    return len(section)

def parse_marker(input_buffer, max_len):
    length = 1
    marker_text = ""
    while length < max_len:
        c = input_buffer.read(1)
        length += 1
        if c == ")":
            return (length,) + tuple(int(num) for num in marker_text.split("x"))
        marker_text += c
    return length, 0, 0

def find_length(input_buffer, to_read = None):
    chars_read = 0
    len = 0
    while chars_read < to_read:
        char = input_buffer.read(1)
        if char == "(":
            after_parse, num_to_read, repeat = parse_marker(input_buffer, to_read - chars_read)
            chars_read += after_parse
            length += find_length(input_buffer, )
        chars_read += 1


(6x2)(1x2)A
AAAA

(6x2)(2x2)AB
(2x2)A(2x2)AB
A(AABAB

(6x3)(2x2)AB
(2x2)A(2x2)A(2x2)AB
A(AA(AABAB

(6x3)(2x3)AB
(2x3)A(2x3)A(2x3)AB
A(A(A(2x3)A(2x3)AB
A(A(AA(A(A(2x3)AB
A(A(AA(A(AABABAB

Edge case: (8x2)(5x2)ABC...

Decompressing (8x2) yields (5x2)ABC(5x2)ABC
Decompressing that yields ABC(5ABC(5x2)ABC
Decompressing that yields ABC(5ABCABC..ABC..

So the (5x2) marker, being encapsulated in the (8x2) marker section was expanded twice,
but we lost two characters due to overlap

repeat*len(section, num_chars)

What about (11x2)(6x3)(3x3)ABC?
(6x3)(3x3)A(6x3)(3x3)ABC
(3x3)A(3x3)A(3x3)A(6x3)(3x3)ABC
A(3A(3A(3x3)A(3x3)A(6x3)(3x3)ABC
A(3A(3AA(3A(3A(3x3)A(6x3)(3x3)ABC
A(3A(3AA(3A(3AA(6A(6A(6x3)(3x3)ABC
A(3A(3AA(3A(3AA(6A(6A(3x3)A(3x3)A(3x3)ABC
A(3A(3AA(3A(3AA(6A(6AA(3A(3A(3x3)A(3x3)ABC
A(3A(3AA(3A(3AA(6A(6AA(3A(3AA(3A(3A(3x3)ABC
A(3A(3AA(3A(3AA(6A(6AA(3A(3AA(3A(3AABCABCABC

well... anyway, it doesn't look like we need to deal with this edge case.
"""


FILENAME = "input.txt"


class PrematureParseEndException(Exception):
    """Raise this if we've reached the end of a section while parsing a paren.

    Luckily, there doesn't seem to be a case of this in the input given or else headache...
    """
    pass


def find_length(input_buffer, chars_to_read=None):
    """Find length of the next X characters in the input after decompressing.abs

    Called recursively for each marker found, passing each length up to caller to compose the
    final length of the decompressed string. Complicated and messy, but does the job for this
    case.
    """
    if chars_to_read is None:
        chars_to_read = float("inf")

    chars_read = 0
    length = 0
    char = None
    while chars_read < chars_to_read:
        char = input_buffer.read(1)

        if char.isspace():
            continue

        if char == "":
            break

        chars_read += 1
        print("read char: {} {} of {}".format(char, chars_read, chars_to_read))

        if char != "(":
            length += 1
        else:
            inner_chars_read, marker_chars, repeat = parse_marker(input_buffer)
            print("({}x{}) with {} chars to read, {} inner chars read, {} chars read".format(
                marker_chars, repeat, chars_to_read, inner_chars_read, chars_read
            ))
            chars_read += inner_chars_read
            if chars_read + marker_chars > chars_to_read:
                raise PrematureParseEndException()
            try:
                inner_length = find_length(input_buffer, marker_chars) * repeat
                print("inner_length of ({}x{}) was {}".format(marker_chars, repeat, inner_length))
            except PrematureParseEndException:
                print("({}x{}) with {} chars to read".format(
                    marker_chars, repeat, chars_to_read - chars_read))
                raise PrematureParseEndException()
            chars_read += marker_chars
            length += inner_length
        print("total length: {}".format(length))

    return length


def parse_marker(input_buffer):
    """Return the parsed argument of marker (AxB) where A = num chars and B = repeat times.

    Function will be called when the opening paren of a marker has already been read, so we must
    read until the closing paren and then parse AxB string.
    """
    marker_text = ""
    char = ""
    length = 0
    while char != ")":
        marker_text += char
        char = input_buffer.read(1)
        print("marker char: {}".format(char))
        length += 1
    return (length,) + tuple(int(num) for num in marker_text.split("x"))


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
        print("The length of the decompressed string is {}".format(find_length(input_file)))
