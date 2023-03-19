import JediTricks
import os


def command_addNumberedLine(frame, groups):
    (number, line) = groups
    number = int(number)
    JediTricks.addNumberLine(frame, number, line)


def command_renumber(frame, groups):
    JediTricks.renumber(frame)


def command_openFile(frame, groups):
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


def command_saveFile(frame, groups):
    if groups[0] == "":
        path = frame.prompt("Save Files As ? >")
    else:
        path = groups[0]
    lines = JediTricks.unnumberedLines(frame)
    lines = "\n".join(lines)
    with open(path, "w+") as file:
        file.writelines(lines)


def command_deleteLine(frame, groups):
    start = int(groups[0])
    if groups[1] != None:
        stop = int(groups[1])
        for lineNumber in range(start, stop + 1):
            JediTricks.deleteLine(frame, lineNumber)
    else:
        JediTricks.deleteLine(frame, start)


def command_clearLines(frame, groups):
    if groups[0] == "yes":
        frame.lines = []
    elif frame.prompt("Clear lines [yes/no] ? ") == "yes":
        frame.lines = []


def command_gotoLine(frame, groups):
    target = int(groups[0]) // 10 - 1
    totalLines = len(frame.lines)
    if target > totalLines:
        target = totalLines - (frame.size[1] // 2)
    frame.start = target


def command_gotoHome(frame, groups):
    frame.start = 0


def command_replace(frame, groups):
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


def command_enableFlow(frame, groups):
    frame.flow = True


command_editor = [
    ("^(\d+) (.*)$", command_addNumberedLine),
    ("^renumber$", command_renumber),
    ("^open *(.*)$", command_openFile),
    ("^save *(.*)$", command_saveFile),
    ("^(?:del|delete) (\d+)(?:$| (\d+))$", command_deleteLine),
    ("^clear *(.*)$", command_clearLines),
    ("^(?:view|goto) (\d+)$", command_gotoLine),
    ("^home$", command_gotoHome),
    ("^replace *\\b(\S*) *\\b(\S*)$", command_replace),
    ("^flow$", command_enableFlow),
]


def command_listFiles(manager, groups):
    frame = manager.newFrame()
    frame.name = "files"
    JediTricks.addLines(frame, os.listdir("."))


def command_exitEditor(manager, groups):
    manager.remove(manager.active())


command_Frame = [
    ("^ls$", command_listFiles),
    ("^exit$", command_exitEditor),
]
