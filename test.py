import os

# from enum import Enum

screen = os.get_terminal_size()

# lines = screen.lines
# cols = screen.columns

text_lines = ["10-", "123", "123123", "!123123123123123", "2"]
starting_line=0


#  a.sort(key=lambda x:int(x.split(" ")[0]))

# Commands = Enum("Command", ["TEXT", "FILE", "EDITOR", ""])


def put(y, x, text):
    print("\033[%d;%dH%s" % (y, x, text), end="")


def cls():
    put(0, 0, chr(27) + "[2J")


def topline(title):
    space = int(os.get_terminal_size().columns / 2) - len(title)
    innerSpace = len(title)
    return "=" * space + " " * innerSpace + title + " " * innerSpace + "=" * space


def drawScreen():
    put(0, 0, topline("testing"))
    for y, line in enumerate(text_lines):
        put(y + 2, 0, line)


def prompt():
    put(os.get_terminal_size().lines, 0, "input ")
    text = input(">")
    return text


def TEXT(text):
    pass


def FILE(text):
    pass


def EDITOR(text):
    pass


def FUN(text):
    pass


def parse(userInput):
    terms = userInput.split(" ")
    if terms[0].isnumeric():
        TEXT(" ".join(terms[1:]))
    elif terms[0].lower() == "file":
        FILE(" ".join(terms[1:]))
    elif terms[0].lower() == "ed":
        EDITOR(" ".join(terms[1:]))
    elif terms[0].lower() == "exit":
        global running
        running = False
        cls()
    else:
        FUN(" ".join(terms[1:]))


running = True

while running:
    cls()
    drawScreen()
    print(running)
    userInput = prompt()
    parse(userInput)
