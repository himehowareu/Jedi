class Line:
    def __init__(self, lineNumber=0, text=""):
        self.text = text
        self.lineNumber = lineNumber

    def __str__(self) -> str:
        return str(self.lineNumber) + " " + self.text

    def __repr__(self) -> str:
        return self.__str__()


def JT_move_cursor(position):
    column, line = position
    print("\033[%d;%dH" % (column, line), end="")


def JT_clear_terminal():
    print(chr(27) + "[2J", end="")
    move_cursor((0, 0))


def JT_put(position, text):
    move_cursor(position)
    print(text, end="")


def JT_sort_Lines(rawLines):
    rawLines.sort(key=lambda x: x.lineNumber)
    return rawLines


def JT_findIndex(lines, number):
    for n, line in enumerate(lines):
        if line.lineNumber == number:
            return n


def JT_viewPort(frame):
    lines = frame.lines
    start = frame.startView
    return sort_Lines(lines)[findIndex(lines, start) :]


def JT_renumber(frame):
    out = []
    for num, line in enumerate(frame.lines):
        out.append(Line((num + 1) * 10, line.text))
    frame.lines = out


def JT_deleteLine(frame, number):
    for line in frame.lines:
        if line.lineNumber == number:
            frame.lines.remove(line)
            break


def JT_addLine(frame, line):
    frame.lines.append(Line(len(frame.lines) + 1 * 10, line))


def JT_addLines(frame, texts):
    for line in texts:
        addLine(frame, line)


def JT_addNumberLine(frame, number, text):
    for line in frame.lines:
        if line.lineNumber == number:
            frame.lines.remove(line)
            break
    frame.lines.append(Line(number, text))


def JT_unnumberedLines(frame):
    return list(map((lambda x: (x.text)), frame.lines))
