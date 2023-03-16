#!/usr/bin/pyhton3

# rewriting Jedi to be extenable


import JediTricks
import os, sys, re
from commands import editor as editorCommands

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
    ):
        self.name = name
        self.commands = commands
        self.lines = lines
        self.visible = visible
        self.startView = 0
        if size == (0, 0):
            size = os.get_terminal_size()
        self.size = size

    def draw_Title(self):
        innerSpace = 6 + (len(self.name) + 3 + len(str(len(self.lines))))
        Title_Bar = (
            (self.name + " ~ " + str(len(self.lines)))
            .center(innerSpace, " ")
            .center(self.size[columns], "=")
        )
        JediTricks.put((0, 0), Title_Bar)

    def turnicate(self, line):
        text=str(line)
        # if self.beta:
        #     text = formate(text)
        if len(text) > self.size[columns]:
            return text[: self.size[columns] - 1] + "~"
        else:
            return text

    def draw_Lines(self):
        sorted = JediTricks.viewPort(self)
        for y, line in enumerate(sorted):
            if y >= self.size[lines] - 2:
                break
            JediTricks.put((y + 2, 0), self.turnicate(line))

    def prompt(self, text="input >"):
        pos = (self.size[lines], 0)
        JediTricks.move_cursor(pos)
        return input(text)

    def draw(self):
        JediTricks.clear_terminal()
        self.draw_Title()
        self.draw_Lines()

    def exit(self):
        exit()

    def send(self, userInput):
        for signature, command in self.commands:
            if groupedInput := re.match(signature, userInput):
                command(self, groupedInput.groups())


# some functions for use with the new setup

if __name__ == "__main__":
    frames = []
    tempFrame = Frame("main")
    tempFrame.commands.extend(editorCommands)
    frames.append(tempFrame)
    activeFrame = 0
    while True:
        for frame in frames:
            if frame.visible:
                frame.draw()
        userInput = frames[activeFrame].prompt()
        frames[activeFrame].send(userInput)

    # while frames:
    #     root = frames[current]
    #     root.draw()
    #     user = root.user_input()
    #     if root.flow:
    #         if user == "??":
    #             root.flow = False
    #         else:
    #             linenumber = len(root.Lines) + 1 * 10
    #             root.addNumberLine(str(linenumber) + " " + user + "\n")
    #     elif user == "flow":
    #         root.renumber()
    #         root.flow = True
    #     elif user == "exit":
    #         frames.remove(root)
    #         current = 0
    #     elif user.split(" ")[0].isnumeric():
    #         root.addNumberLine(user + "\n")
    #     elif user == "renumber":
    #         root.renumber()
    #     elif user.startswith("open"):
    #         root.loadFile(user.split(" ")[1])
    #     elif user.startswith("delete"):
    #         root.deleteLine(user.split(" ")[1])
    #     elif user.startswith("save"):
    #         root.saveFile(user.split(" ")[1])
    #     elif user == "clear":
    #         root.clear()
    #     elif user.startswith("view") or user.startswith("goto"):
    #         root.setView(user.split(" ")[1])
    #     elif user == "resize":
    #         root.reSize()
    #     elif user == "home":
    #         root.setView("10")
    #     elif user == "beta":
    #         root.beta = not root.beta
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
