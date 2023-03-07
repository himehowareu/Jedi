#!/usr/bin/pyhton3

# rewriting Jedi to be extenable


import JediTricks

class Fame();
    def __init__(name="New Frame",functions=[],commands=[]):
        self.name = name
        self.commands=commands






if __name__ == "__main__":
    frames = []
    mainFrame = Frame("main")





    while frames:
        root = frames[current]
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
            frames.remove(root)
            current = 0
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
        elif user == "ls":
            temp = Frame(Title="File listing")
            temp.renumber()
            temp.addLines(os.listdir("."))
            temp.renumber()
            current = len(frames)
            frames.append(temp)
        elif user == "list":
            temp = Frame(Title="Fraame list")
            temp.renumber()
            temp.addLines(map(str, frames))
            temp.addLines(["Frame listing"])
            temp.renumber()
            current = len(frames)
            frames.append(temp)
        elif user == "!!":
            sys.exit("")
        elif user == "shell":
            break
    
