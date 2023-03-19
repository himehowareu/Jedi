#!/usr/bin/pyhton3

# rewriting Jedi to be extenable


import JediTricks
import os, sys, re

# from commands import editor as editorCommands
# from commands import Frame as frameCommands

lines = 1
columns = 0


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
        JediTricks.put((0, 0), Title_Bar)

    def turnicate(self, line):
        text = str(line)
        # if self.beta:
        #     text = formate(text)
        if len(text) > self.size[columns]:
            return text[: self.size[columns] - 1] + "~"
        else:
            return text

    def draw_Lines(self):
        sorted = JediTricks.viewPort(self)[self.start :]
        for y, line in enumerate(sorted):
            if y >= self.size[lines] - 2:
                break
            JediTricks.put((y + 2, 0), self.turnicate(line))
        if self.error != "":
            JediTricks.put(
                (self.size[lines] - 2, (self.size[columns] - len(self.error)) // 2),
                self.error,
            )
            self.error = ""

    def prompt(self, text="input >"):
        pos = (self.size[lines], 0)
        JediTricks.move_cursor(pos)
        return input(text)

    def draw(self):
        JediTricks.clear_terminal()
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


# some functions for use with the new setup

if __name__ == "__main__":
    manager = frameManager(command_editor)
    tempFrame = Frame("main")
    tempFrame.commands.extend(command_Frame)
    manager.addFrame(tempFrame)
    while manager.activeFrame != -1:
        activeFrame = manager.active()
        for frame in manager.frames:
            if frame.visible:
                frame.draw()
        if activeFrame.flow:
            userInput = activeFrame.prompt("Flow> ")
            if userInput == "??":
                activeFrame.flow = False
                continue
            JediTricks.addLine(activeFrame, userInput)
        else:
            userInput = activeFrame.prompt()
            activeFrame.send(userInput)

    #     elif user == "ls":
    #         temp = Frame(Title="File listing")
    #         temp.renumber()
    #         temp.addLines(os.listdir("."))
    #         temp.renumber()
    #         current = len(frames)
    #         frames.append(temp)
    #     elif user == "list":
    #         temp = Frame(Title="Fraame list")
    #         temp.renumber()
    #         temp.addLines(map(str, frames))
    #         temp.addLines(["Frame listing"])
    #         temp.renumber()
    #         current = len(frames)
    #         frames.append(temp)
    #     elif user == "!!":
    #         sys.exit("")
    #     elif user == "shell":
    #         break
