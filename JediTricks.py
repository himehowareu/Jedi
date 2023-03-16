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
    rawLines.sort(key=lambda x: int(x.split(" ")[0]))
    return rawLines


def findIndex(lines, number):
    for n, line in enumerate(lines):
        if line.split(" ")[0] == number:
            return n


def viewPort(frame):
    lines = frame.lines
    start = frame.startView
    return sort_Lines(lines)[findIndex(lines, start) :]


def renumber(frame):
    out = []
    for num, line in enumerate(frame.lines):
        newLine = [str((num + 1) * 10)] + line.split(" ")[1:]
        out.append(" ".join(newLine))
    frame.lines = out


def deleteLine(frame, number):
    for line in frame.lines:
        if line.split(" ")[0] == number:
            frame.lines.remove(line)
            break


def addLines(frame, texts):
    for line in texts:
        frame.lines.append(str(len(frame.lines) + 1 * 10) + " " + line)


def addNumberLine(frame, number, text):
    for line in frame.lines:
        if line.split(" ")[0] == number:
            frame.lines.remove(line)
            break
    frame.lines.append(number + " " + text)

def unnumberedLines(frame):
    return list(map(lambda x: (" ".join(x.split(" ")[1:])), frame.lines))
