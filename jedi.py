import os

lines = 0
columns = 1


def terminal_lines():
    return os.get_terminal_size().lines


def terminal_columns():
    return os.get_terminal_size().columns


def move_cursor(position):
    line, column = position
    print("\033[%d;%dH" % (line, column), end="")


def put(position, text):
    move_cursor(position)
    print(text, end="")


def clear_terminal():
    print((0, 0), chr(27) + "[2J", end="")
    move_cursor((0, 0))


def sort_Lines(rawLines):
    rawLines.sort(key=lambda x: int(x.split(" ")[0]))
    # return (list(map(lambda x:" ".join(x.split[1:]),rawLines)))
    return rawLines


class Frame:
    def __init__(
        self,
        Title="New Frame",
        Size=(terminal_lines(), terminal_columns()),
        Position=(0, 0),
    ) -> None:
        self.Lines = ["10 test text"]
        self.Title = Title
        self.Size = (Size[lines] - Position[lines], Size[columns] - Position[columns])
        self.Position = Position

    def relative(self, position):
        line, column = position
        line += self.Position[lines]
        column += self.Position[columns]
        return (line, column)

    def renumber(self):
        out = []
        for num, line in enumerate(self.Lines):
            newLine = [str((num + 1) * 10)] + line.split(" ")[1:]
            out.append(" ".join(newLine))
        self.Lines = out

    def turnicate(self, text):
        if len(text) > self.Size[columns] - self.Position[columns]:
            return text[: self.Size[columns] - self.Position[columns] - 1] + "~"
        else:
            return text

    def addNumberLine(self, text):
        for line in self.Lines:
            if line.split(" ")[0] == text.split(" ")[0]:
                self.Lines.remove(line)
                break
        self.Lines.append(text)

    def draw_Title(self):
        # space = int(self.Size[columns] / 2) - len(self.Title)
        innerSpace = len(self.Title) * 2
        Title_Bar = self.Title.center(innerSpace, " ").center(
            self.Size[columns] - self.Position[columns], "="
        )

        pos = self.relative((0, 0))
        put(pos, Title_Bar)

    def draw_Lines(self):
        pos = self.relative((0, 0))
        # pos = (pos[lines] + 1, pos[columns])  # title line
        sorted = sort_Lines(self.Lines)
        if len(sorted) > self.Size[lines] - 2:
            sorted = sorted[len(sorted) - self.Size[lines] + 2 :]
        for y, line in enumerate(sorted):
            pos = (pos[lines] + 1, pos[columns])  # title line
            put(pos, self.turnicate(line))

    def prompt(self, text="input >"):
        pos = (self.Size[lines], 0)
        pos = self.relative(pos)
        move_cursor(pos)
        return input(text)

    def loadFile(self, path):
        self.Lines = []
        linenumber = 10
        with open(path, "r") as file:
            for line in file.readlines():
                self.addNumberLine(str(linenumber) + " " + line)
                linenumber += 10

    def saveFile(self, path):
        textLines = list(map(lambda x: " ".join(x.split(" ")[1:] + "\n"), self.Lines))
        print(textLines)
        with open(path, "w+") as file:
            file.writelines(textLines)

    def draw(self):
        self.draw_Title()
        self.draw_Lines()

    def user_input(self):
        userInput = self.prompt()
        return userInput


"""
goto
clear
home
continues / flow
view 
"""

root = Frame(Position=(10, 10))

running = True

while running:
    clear_terminal()
    root.draw()
    user = root.user_input()
    if user == "exit":
        running = False
    elif user.split(" ")[0].isnumeric():
        root.addNumberLine(user)
    elif user == "renumber":
        root.renumber()
    elif user.startswith("open"):
        root.loadFile(user.split(" ")[1])
    elif user.startswith("save"):
        root.saveFile(user.split(" ")[1])

clear_terminal()
