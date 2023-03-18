import JediTricks
import os


def addNumberedLine(frame, groups):
    (number, line) = groups
    number = int(number)
    JediTricks.addNumberLine(frame, number, line)


def renumber(frame, groups):
    JediTricks.renumber(frame)


def openFile(frame, groups):
    if groups[0] == "":
        path = frame.prompt("Files ? >")
    else:
        path = groups[0]

    if not os.path.exists(path):
        frame.error = "File not found"
        return
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
    target = int(groups[0]) // 10 - 1
    totalLines = len(frame.lines)
    if target > totalLines:
        target = totalLines - (frame.size[1] // 2)
    frame.start = target


def gotoHome(frame, groups):
    frame.start = 0


def replace(frame, groups):
    if groups[0] == "":
        target = frame.prompt("what would you like to replace ?")
    else:
        target = groups[0]
    if groups[1] == "":
        to = frame.prompt("what would you like to replace it with ?")
    else:
        to = groups[1]

    for lineNumber, line in enumerate(frame.lines):
        frame.lines[lineNumber].text = line.text.replace(target, to)


def enableFlow(frame, groups):
    frame.flow = True


editor = [
    ("^(\d+) (.*)$", addNumberedLine),
    ("^renumber$", renumber),
    ("^open *(.*)$", openFile),
    ("^save *(.*)$", saveFile),
    ("^(?:del|delete) (\d+)(?:$| (\d+))$", deleteLine),
    ("^clear *(.*)$", clearLines),
    ("^(?:view|goto) (\d+)$", gotoLine),
    ("^home$", gotoHome),
    ("^replace *\\b(\S*) *\\b(\S*)$", replace),
    ("^flow$", enableFlow),
]


def listFiles(manager, groups):
    frame = manager.newFrame()
    frame.name = "files"
    JediTricks.addLines(frame, os.listdir("."))


def exitEditor(manager, groups):
    manager.remove(manager.active())


Frame = [
    ("^ls$", listFiles),
    ("^exit$", exitEditor),
]
