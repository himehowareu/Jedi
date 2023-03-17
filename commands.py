import JediTricks


def addNumberedLine(frame, groups):
    (number, line) = groups
    number = int(number)
    JediTricks.addNumberLine(frame, number, line)


def exitEditor(frame, groups):
    frame.exit()


def renumber(frame, groups):
    JediTricks.renumber(frame)


def openFile(frame, groups):
    if groups[0] == "":
        path = frame.prompt("Files ? >")
    else:
        path = groups[0]

    with open(path, "r") as file:
        lines = file.read().split("\n")
        frame.lines = []
        JediTricks.addLines(frame, lines)
        JediTricks.renumber(frame)


def saveFile(frame, groups):
    if groups[0] == "":
        path = frame.prompt("Save Files As ? >")
    else:
        path = groups[0]
    lines = JediTricks.unnumberedLines(frame)
    lines = "\n".join(lines)
    with open(path, "w+") as file:
        file.writelines(lines)


def deleteLine(frame, groups):
    start = int(groups[0])
    if groups[1] != None:
        stop = int(groups[1])
        for lineNumber in range(start, stop + 1):
            JediTricks.deleteLine(frame, lineNumber)
    else:
        JediTricks.deleteLine(frame, start)


def clearLines(frame, groups):
    if groups[0] == "yes":
        frame.lines = []
    elif frame.prompt("Clear lines [yes/no] ? ") == "yes":
        frame.lines = []


def gotoLine(frame, groups):
    frame.start = int(groups[0]) // 10 + 1


editor = [
    ("exit", exitEditor),
    ("(\d+) (.*)", addNumberedLine),
    ("renumber", renumber),
    ("open *(.*)", openFile),
    ("save *(.*)", saveFile),
    ("(?:del|delete) (\d+)(?:$| (\d+))", deleteLine),
    ("clear *(.*)", clearLines),
    ("(?:view|goto) (\d+)", gotoLine),
]
