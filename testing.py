#!/usr/bin/pyhton3

# rewriting Jedi to be extenable


# import JediTricks
import os, sys, re


lines = 1
columns = 0

debuging = False
if debuging:
    import logging

    logging.basicConfig(filename="debug.log", level=logging.INFO)


def debug(func):
    def doStuff(*args, **kwargs):
        if debuging:
            logging.info((str(func) + "(" + str(args) + str(kwargs) + ")"))
        R = func(*args, **kwargs)
        if debuging and R:
            logging.warning(str(R))
        return R

    return doStuff


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


@debug
def JT_addLine(frame, line):
    frame.lines.append(Line(len(frame.lines) + 1 * 10, line))


def JT_addLines(frame, texts):
    for line in texts:
        JT_addLine(frame, line)


@debug
def JT_addNumberLine(frame, number, text):
    for line in frame.lines:
        if line.lineNumber == number:
            frame.lines.remove(line)
            break
    frame.lines.append(Line(number, text))


def JT_unnumberedLines(frame):
    return list(map((lambda x: (x.text)), frame.lines))


def JT_help(commands):
    out = []
    for command in commands:
        try:
            out.append(command[2] + " " + command[1].__doc__)
        except:
            out.append(str(command))
    return out


class Frame:
    def __init__(
        self,
        name="New Frame",
        position=(0, 0),
        size=(0, 0),
        commands=[],
        visible=False,
        start=0,
        flow=False,
    ):
        self.name = name
        self.commands = commands
        self.lines = []
        self.visible = visible
        self.startView = 0
        if size == (0, 0):
            size = os.get_terminal_size()
        self.size = size
        self.start = start
        self.flow = flow
        self.error = ""

    def __repr__(self) -> str:
        return f"<Frame @ {id(self)}>"

    @debug
    def draw_Title(self):
        innerSpace = 6 + (len(self.name) + 3 + len(str(len(self.lines))))
        Title_Bar = (
            (self.name + " ~ " + str(len(self.lines)))
            .center(innerSpace, " ")
            .center(self.size[columns], "=")
        )
        JT_put((0, 0), Title_Bar)

    def tunicate(self, line):
        text = str(line)
        # if self.beta:
        #     text = formate(text)
        if len(text) > self.size[columns]:
            return text[: self.size[columns] - 1] + "~"
        else:
            return text

    @debug
    def draw_Lines(self):
        sorted = JT_viewPort(self)[self.start :]
        for y, line in enumerate(sorted):
            if y >= self.size[lines] - 2:
                break
            JT_put((y + 2, 0), self.tunicate(line))
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
        for signature, command, name in self.commands:
            if groupedInput := re.match(signature, userInput):
                command(self, groupedInput.groups())
                break
        else:
            for signature, command, name in self.managerCommands:
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

    def __repr__(self) -> str:
        return "frameManager"

    @debug
    def addFrame(self, frame):
        frame.managerCommands = self.commands
        frame.manager = self
        self.frames.append(frame)
        self.activeFrame = self.frames.index(frame)

    @debug
    def newFrame(self):
        temp = Frame("temp")
        self.addFrame(temp)
        return self.frames.index(temp)

    @debug
    def active(self):
        return self.getFrame(self.activeFrame)

    @debug
    def getFrame(self, number):
        return self.frames[number]

    def remove(self, frame):
        if self.frames.index(frame) == len(self.frames) - 1:
            self.activeFrame -= 1
        self.frames.remove(frame)


def command_addNumberedLine(frame, groups):
    """adds a line at the line number to the current frame"""
    (number, line) = groups
    number = int(number)
    JT_addNumberLine(frame, number, line)


@debug
def command_renumber(frame, groups):
    """renumbers the frame"""
    JT_renumber(frame)


def command_openFile(frame, groups):
    """opens file [file name]"""
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
    """saves file [file name]"""
    if groups[0] == "":
        path = frame.prompt("Save Files As ? >")
    else:
        path = groups[0]
    lines = JT_unnumberedLines(frame)
    lines = "\n".join(lines)
    with open(path, "w+") as file:
        file.writelines(lines)


def command_deleteLine(frame, groups):
    """deletes the lines"""
    start = int(groups[0])
    if groups[1] != None:
        stop = int(groups[1])
        for lineNumber in range(start, stop + 1):
            JT_deleteLine(frame, lineNumber)
    else:
        JT_deleteLine(frame, start)


def command_clearLines(frame, groups):
    """clears the frame !! all data is lost !!"""
    if groups[0] == "yes":
        frame.lines = []
    elif frame.prompt("Clear lines [yes/no] ? ") == "yes":
        frame.lines = []


def command_gotoLine(frame, groups):
    """go to the line given"""
    target = int(groups[0]) // 10 - 1
    totalLines = len(frame.lines)
    if target > totalLines:
        target = totalLines - (frame.size[1] // 2)
    frame.start = target


def command_gotoHome(frame, groups):
    """brings you to the start of the file"""
    frame.start = 0


def command_replace(frame, groups):
    """replce [target] [to]"""
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
    """this command lets you continually type until you enter ??"""
    frame.flow = True


command_editor = [
    ("^(\d+) (.*)$", command_addNumberedLine, "10 text"),
    ("^renumber$", command_renumber, "renumber"),
    ("^open *(.*)$", command_openFile, "open [fileName]"),
    ("^save *(.*)$", command_saveFile, "save [fileName]"),
    (
        "^(?:del|delete) (\d+)(?:$| (\d+))$",
        command_deleteLine,
        "del[ete] line [To Line]",
    ),
    ("^clear *(.*)$", command_clearLines, "clear"),
    ("^(?:view|goto) (\d+)$", command_gotoLine, "goto Line"),
    ("^home$", command_gotoHome, "home"),
    ("^replace *\\b(\S*) *\\b(\S*)$", command_replace, "replace [Target] [TO]"),
    ("^flow$", command_enableFlow, "flow"),
]


def command_listFiles(manager, groups):
    """makes a new frame with a list of files in the current folder"""
    frameID = manager.newFrame()
    frame = manager.getFrame(frameID)
    frame.name = "files"
    JT_addLines(frame, os.listdir("."))


def command_exitEditor(manager, groups):
    """exits the editor"""
    exit("need to make better")


def command_exitFrame(manaager, groups):
    """closes the current frame"""
    manager.remove(manager.active())


def command_help(manager, groups):
    """displays this help page"""
    frameID = manager.newFrame()
    frame = manager.getFrame(frameID)
    frame.name = "help"
    JT_addLine(frame, "Editor commands ")
    JT_addLines(frame, JT_help(command_editor))
    JT_addLines(frame, JT_help(command_Frame))


command_Frame = [
    ("^ls$", command_listFiles, "ls"),
    ("^!!$", command_exitFrame, "!!"),
    ("^exit$", command_exitEditor, "exit"),
    ("^help$", command_help, "help"),
]


# some functions for use with the new setup

if __name__ == "__main__":
    manager = frameManager(command_Frame)
    _Frame = Frame("main")
    _Frame.commands.extend(command_editor)
    manager.addFrame(_Frame)
    while manager.activeFrame != -1:
        activeFrame = manager.active()
        activeFrame.draw()
        if activeFrame.flow:
            userInput = activeFrame.prompt("Flow> ")
            if userInput == "??":
                activeFrame.flow = False
                continue
            JT_addLine(activeFrame, userInput)
        else:
            userInput = activeFrame.prompt()
            activeFrame.send(userInput)
