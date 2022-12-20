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
    print(chr(27) + "[2J", end="")
    move_cursor((0, 0))


def sort_Lines(rawLines):
    rawLines.sort(key=lambda x: int(x.split(" ")[0]))
    return rawLines


def formate(text):

    try:

        import highlight

        classified_text = highlight.analyze_python(text)
        return highlight.ansi_highlight(classified_text)
    except:
        return text


class Frame:
    def __init__(
        self,
        Title="New Frame",
        Size=(terminal_lines(), terminal_columns()),
        lines=[],
        start=0,
        beta=False,
    ) -> None:
        self.Lines = lines
        self.Start = start
        self.Title = Title
        self.Size = Size
        self.beta = beta
        self.flow = False

    def renumber(self):
        out = []
        for num, line in enumerate(self.Lines):
            newLine = [str((num + 1) * 10)] + line.split(" ")[1:]
            out.append(" ".join(newLine))
        self.Lines = out

    def turnicate(self, text):
        if self.beta:
            text = formate(text)
        if len(text) > self.Size[columns]:
            return text[: self.Size[columns] - 1] + "~"
        else:
            return text

    def findNumber(self, number):
        for n, line in enumerate(self.Lines):
            if line.split(" ")[0] == number:
                return n

    def deleteLine(self, number):
        for line in self.Lines:
            if line.split(" ")[0] == number:
                self.Lines.remove(line)
                break

    def addNumberLine(self, text):
        for line in self.Lines:
            if line.split(" ")[0] == text.split(" ")[0]:
                self.Lines.remove(line)
                break
        self.Lines.append(text)

    def draw_Title(self):
        innerSpace = (len(self.Title) + 3 + len(str(len(self.Lines)))) * 2
        Title_Bar = (
            (self.Title + " ~ " + str(len(self.Lines)))
            .center(innerSpace, " ")
            .center(self.Size[columns], "=")
        )
        put((0, 0), Title_Bar)

    def draw_Lines(self):
        start = self.findNumber(self.Start)
        sorted = sort_Lines(self.Lines)[start:]
        for y, line in enumerate(sorted):
            if y >= self.Size[lines] - 2:
                break
            put((y + 2, 0), self.turnicate(line))

    def prompt(self, text="input >"):
        pos = (self.Size[lines], 0)
        move_cursor(pos)
        return input(text)

    def loadFile(self, path):
        self.Title = path
        self.Lines = []
        linenumber = 10
        with open(path, "r") as file:
            for line in file.readlines():
                self.addNumberLine(str(linenumber) + " " + line)
                linenumber += 10

    def saveFile(self, path):
        textLines = list(map(lambda x: (" ".join(x.split(" ")[1:])), self.Lines))
        print(textLines)
        with open(path, "w+") as file:
            file.writelines(textLines)

    def draw(self):
        clear_terminal()
        self.draw_Title()
        self.draw_Lines()

    def clear(self):
        if self.prompt("clear lines? [yes\\no]") == "yes":
            self.Lines = []

    def user_input(self):
        userInput = self.prompt()
        return userInput

    def setView(self, linenumber):
        self.Start = linenumber

    def reSize(self):
        self.Size = (terminal_lines(), terminal_columns())


root = Frame()

running = True

while running:
    root.draw()
    user = root.user_input()
    if root.flow:
        if user == "??":
            root.flow = False
        else:
            linenumber = len(root.Lines) + 1 * 10
            root.addNumberLine(str(linenumber) + " " + user + "\n")
    elif user == "flow":
        root.renumber()
        root.flow = True
    elif user == "exit":
        running = False
    elif user.split(" ")[0].isnumeric():
        root.addNumberLine(user + "\n")
    elif user == "renumber":
        root.renumber()
    elif user.startswith("open"):
        root.loadFile(user.split(" ")[1])
    elif user.startswith("delete"):
        root.deleteLine(user.split(" ")[1])
    elif user.startswith("save"):
        root.saveFile(user.split(" ")[1])
    elif user == "clear":
        root.clear()
    elif user.startswith("view") or user.startswith("goto"):
        root.setView(user.split(" ")[1])
    elif user == "resize":
        root.reSize()
    elif user == "home":
        root.setView("10")
    elif user == "beta":
        root.beta = not root.beta


clear_terminal()
