class Line:
    def __init__(self, lineNumber=0, text=""):
        self.text = text
        self.lineNumber = lineNumber

    def __str__(self) -> str:
        return str(self.lineNumber) + " " + self.text

    def __repr__(self) -> str:
        return self.__str__()


def move_cursor(position):
    column, line = position
    print("\033[%d;%dH" % (column, line), end="")


def clear_terminal():
    print(chr(27) + "[2J", end="")
    move_cursor((0, 0))


def put(position, text):
    move_cursor(position)
    print(text, end="")


def sort_Lines(rawLines):
    rawLines.sort(key=lambda x: x.lineNumber)
    return rawLines


def findIndex(lines, number):
    for n, line in enumerate(lines):
        if line.lineNumber == number:
            return n


def viewPort(frame):
    lines = frame.lines
    start = frame.startView
    return sort_Lines(lines)[findIndex(lines, start) :]


def renumber(frame):
    out = []
    for num, line in enumerate(frame.lines):
        out.append(Line((num + 1) * 10, line.text))
    frame.lines = out


def deleteLine(frame, number):
    for line in frame.lines:
        if line.lineNumber == number:
            frame.lines.remove(line)
            break


def addLines(frame, texts):
    for line in texts:
        frame.lines.append(Line(len(frame.lines) + 1 * 10, line))


def addNumberLine(frame, number, text):
    for line in frame.lines:
        if line.lineNumber == number:
            frame.lines.remove(line)
            break
    frame.lines.append(Line(number, text))


def unnumberedLines(frame):
    return list(map((lambda x: (x.text)), frame.lines))
