
def clear(frame):
	pass

def move_cursor(position):
    line, column = position
    print("\033[%d;%dH" % (line, column), end="")

def clear_terminal():
    print(chr(27) + "[2J", end="")
    move_cursor((0, 0))

def sort_Lines(rawLines):
    rawLines.sort(key=lambda x: int(x.split(" ")[0]))
    return rawLines

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

    def deleteLine(self, number):
        for line in self.Lines:
            if line.split(" ")[0] == number:
                self.Lines.remove(line)
                break

    def addLines(self, texts):
        for line in texts:
            self.Lines.append(str(len(self.Lines) + 1 * 10) + " " + line)
        self.renumber()

    def addNumberLine(self, text):
        for line in self.Lines:
            if line.split(" ")[0] == text.split(" ")[0]:
                self.Lines.remove(line)
                break
        self.Lines.append(text)


