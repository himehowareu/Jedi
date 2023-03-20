#!/usr/bin/pyhton3

# rewriting Jedi to be extenable


# import JediTricks
import os, sys, re

# from commands import editor as editorCommands
# from commands import Frame as frameCommands

lines = 1
columns = 0


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
    JT_move_cursor((0, 0))


def JT_put(position, text):
    JT_move_cursor(position)
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
    return JT_sort_Lines(lines)[JT_findIndex(lines, start) :]


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
        JT_addLine(frame, line)


def JT_addNumberLine(frame, number, text):
    for line in frame.lines:
        if line.lineNumber == number:
            frame.lines.remove(line)
            break
    frame.lines.append(Line(number, text))


def JT_unnumberedLines(frame):
    return list(map((lambda x: (x.text)), frame.lines))


class Frame:
    def __init__(
        self,
        name="New Frame",
        position=(0, 0),
        size=(0, 0),
        commands=[],
        lines=[],
        visible=True,
        start=0,
        flow=False,
    ):
        self.name = name
        self.commands = commands
        self.lines = lines
        self.visible = visible
        self.startView = 0
        if size == (0, 0):
            size = os.get_terminal_size()
        self.size = size
        self.start = start
        self.flow = flow
        self.error = ""

    def draw_Title(self):
        innerSpace = 6 + (len(self.name) + 3 + len(str(len(self.lines))))
        Title_Bar = (
            (self.name + " ~ " + str(len(self.lines)))
            .center(innerSpace, " ")
            .center(self.size[columns], "=")
        )
        JT_put((0, 0), Title_Bar)

    def turnicate(self, line):
        text = str(line)
        # if self.beta:
        #     text = formate(text)
        if len(text) > self.size[columns]:
            return text[: self.size[columns] - 1] + "~"
        else:
            return text

    def draw_Lines(self):
        sorted = JT_viewPort(self)[self.start :]
        for y, line in enumerate(sorted):
            if y >= self.size[lines] - 2:
                break
            JT_put((y + 2, 0), self.turnicate(line))
        if self.error != "":
            JT_put(
                (self.size[lines] - 2, (self.size[columns] - len(self.error)) // 2),
                self.error,
            )
            self.error = ""

    def prompt(self, text="input >"):
        pos = (self.size[lines], 0)
        JT_move_cursor(pos)
        return input(text)

    def draw(self):
        JT_clear_terminal()
        self.draw_Title()
        self.draw_Lines()

    def send(self, userInput):
        for signature, command in self.commands:
            if groupedInput := re.match(signature, userInput):
                command(self, groupedInput.groups())
                break
        else:
            for signature, command in self.managerCommands:
                if groupedInput := re.match(signature, userInput):
                    command(self.manager, groupedInput.groups())
                    break
            else:
                if userInput != "":
                    self.error = userInput + ": command not found"


class frameManager:
    def __init__(self, commands):
        self.frames = []
        self.activeFrame = -1
        self.commands = commands

    def addFrame(self, frame):
        frame.managerCommands = self.commands
        frame.manager = self
        self.frames.append(frame)
        self.activeFrame = self.frames.index(frame)

    def newFrame(self):
        temp = Frame()
        self.addFrame(temp)
        return temp

    def active(self):
        return self.frames[self.activeFrame]

    def remove(self, frame):
        if self.frames.index(frame) == len(self.frames) - 1:
            self.activeFrame -= 1
        self.frames.remove(frame)


# import JediTricks
# import os


def command_addNumberedLine(frame, groups):
    (number, line) = groups
    number = int(number)
    JT_addNumberLine(frame, number, line)


def command_renumber(frame, groups):
    JT_renumber(frame)


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
        JT_addLines(frame, lines)
        JT_renumber(frame)


def command_saveFile(frame, groups):
    if groups[0] == "":
        path = frame.prompt("Save Files As ? >")
    else:
        path = groups[0]
    lines = JT_unnumberedLines(frame)
    lines = "\n".join(lines)
    with open(path, "w+") as file:
        file.writelines(lines)


def command_deleteLine(frame, groups):
    start = int(groups[0])
    if groups[1] != None:
        stop = int(groups[1])
        for lineNumber in range(start, stop + 1):
            JT_deleteLine(frame, lineNumber)
    else:
        JT_deleteLine(frame, start)


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
    JT_addLines(frame, os.listdir("."))


def command_exitEditor(manager, groups):
    manager.remove(manager.active())


command_Frame = [
    ("^ls$", command_listFiles),
    ("^exit$", command_exitEditor),
]


# some functions for use with the new setup

if __name__ == "__main__":
    manager = frameManager(command_Frame)
    tempFrame = Frame("main")
    tempFrame.commands.extend(command_editor)
    manager.addFrame(tempFrame)
    while manager.activeFrame != -1:
        activeFrame = manager.active()
        for main_frame in manager.frames:
            if main_frame.visible:
                main_frame.draw()
        if activeFrame.flow:
            userInput = activeFrame.prompt("Flow> ")
            if userInput == "??":
                activeFrame.flow = False
                continue
            JT_addLine(activeFrame, userInput)
        else:
            userInput = activeFrame.prompt()
            activeFrame.send(userInput)
