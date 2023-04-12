# tkinter provides GUI objects and commands
import tkinter as tk
import tkinter.ttk as ttk

# An object (root) is created which represents the window.
# Its title and full screen property are set.
root = tk.Tk()
root.title("One-time pad crib drag")
root.wm_state("zoomed")

# This function is invoked when the user clicks the button
# "Load cipher data from file".
# According to the option "Load as text file" it either:
# - tries to open a text file containing correctly formatted
#   hexadecimal numbers
# - tries to open a binary file with the name specified
# in the corresponding entry field. Further, it tells the
# user whether the loading of the file succeeded and, if so,
# prints its contents in the text field below as a string
# of hexadecimal values for each byte separated by spaces.
def ButtonCiphLoadClick():
    LabelCiphFeedback["text"] = ""
    ciph = ""
    try:
        if LoadAsText.get() == "1":
            with open(PathCiph.get(), mode = "rt", encoding = "utf-8") as CiphFile:
                ciph = CiphFile.read()
                try:
                    CheckHex(ciph)
                except:
                    LabelCiphFeedback["text"] = "Text in the file is incorrectly formatted."
        else:
            with open(PathCiph.get(), mode = "br") as CiphFile:
                ciph = ToHexStr(CiphFile.read())
    except:
        LabelCiphFeedback["text"] = "An error occurred while reading the file."
    else:
        if ciph == "":
            LabelCiphFeedback["text"] = "File empty"
        else:
            TextCiph.delete("1.0", "end")
            TextCiph.insert("1.0", ciph)
            LabelCiphFeedback["text"] = "File loaded successfully."
            if LoadAsText.get() == "1":
                CiphChanged()

# This function formats the input data as a string of
# hexadecimal values for each byte separated by spaces,
# e.g. "a3 e2 00"
def ToHexStr(data):
    data = list(data)
    DataList = [format(int(data[i]), "x").zfill(2) for i in range(len(data))]
    return " ".join(DataList)

# This function checks if the received string is
# a hexadecimal value between 0 and 255. 
def CheckHex(ciph):
    FeedbackMessage = ""
    try:
        ciph = ciph.split("\n")
        for i in range(len(ciph)):
            ciph[i] = ciph[i].split()
        if (len(ciph) < 2) or (len(ciph[1]) < 1):
            FeedbackMessage = "Text contains only one line."
            raise Exception
        n = len(ciph[0])
        for i in range(len(ciph)):
            if len(ciph[i]) > n:
                FeedbackMessage = "One line is longer than the first line."
                raise Exception
            if (len(ciph[i]) < n) and (i < len(ciph)-1):
                FeedbackMessage = "One line (and not the last one) is shorter than the first."
                raise Exception
            for j in range(len(ciph[i])):
                try:
                    k = int(ciph[i][j], 16)
                    if (k < 0) or (k > 255):
                        raise Exception
                except:
                    FeedbackMessage = "Some entries are not a hexadecimal number from 0 to 255."
                    raise
    except:
        if FeedbackMessage == "":
            FeedbackMessage = "Incorrectly formatted ciphertext"
        LabelCiphFeedback["text"] = FeedbackMessage
        return None
    return ciph

# This function formats the * and letters in PlainGrid
# as a string and prints in the TextPlain field.
def PrintPlaintext():
    s = "\n".join(["".join(PlainGrid[i]) for i in range(len(PlainGrid))])
    TextPlain.insert("1.0", s[:-1])

# This function is invoked when the user click the button
# "Process ciphertext".
# The global variables are assigned the new dimensions and
# filled with letters and "*" respectively.
def CiphChanged():
    global CiphGrid
    global PlainGrid
    TextPlain.delete("1.0", "end")
    ciph = CheckHex(TextCiph.get("1.0", "end")[:-1])
    if ciph == None:
        return
    LabelCiphFeedback["text"] = ""
    CiphGrid = [[0 for j in range(len(ciph[i]))] for i in range(len(ciph))]
    PlainGrid = [["*" for j in range(len(ciph[i]))] for i in range(len(ciph))]
    for i in range(len(ciph)):
        for j in range(len(ciph[i])):
            CiphGrid[i][j] = int(ciph[i][j], 16)
    PrintPlaintext()
    GuessChanged(Guess.get())

# This function is invoked when the users changes his guess
# in the EntryGuess.
# It sorts all results by the number of unlikely characters
# they contain.
def GuessChanged(Guess):

    def UpdateFrameGuesses():
        for i in range(len(ListFramesGuess)):
            if i < len(ResultsList):
                ListFramesGuess[i].pack(side = "top", fill = "x")
                ListLabelGuess[i]["text"] = ResultsList[i][2]
                ListButtonGuess[i]["command"] = lambda i=ResultsList[i][0], k=ResultsList[i][1]: GuessChosen(i, k, Guess)
            else:
                ListFramesGuess[i].pack_forget()
        return True

    ResultsList = []
    if len(CiphGrid) == 0:
        LabelCiphFeedback["text"] = "Missing ciphertext"
        return UpdateFrameGuesses()
    LabelCiphFeedback["text"] = ""
    if len(Guess) > len(CiphGrid[1]):
        LabelCiphFeedback["text"] = "Guess must not be longer than assumed key."
        return UpdateFrameGuesses()
    if len(Guess) == 0:
        return UpdateFrameGuesses()
    for c in Guess:
        if ord(c) > 255:
            return False
    GuessGrid = [ord(c) for c in Guess]
    for i in range(len(CiphGrid)):
        for k in range(len(CiphGrid[i]) - len(Guess) + 1):
            s = ""
            UnlikelyCharacters = 0
            for j in range(len(CiphGrid)):
                if (j == i) or (k > len(CiphGrid[j]) - len(Guess)):
                    continue
                for l in range(len(Guess)):
                    c = chr(ord(Guess[l]) ^ CiphGrid[i][k + l] ^ CiphGrid[j][k + l])
                    s += c
                    if ((c not in [".", ",", ":", ";", "-", "!", "?", "'", " ", '"']) and
                        ((ord(c) > ord("Z")) or (ord(c) < ord("A"))) and
                        ((ord(c) > ord("z")) or (ord(c) < ord("a"))) and
                        ((ord(c) > ord("9")) or (ord(c) < ord("0")))):
                        UnlikelyCharacters += 1
                s += "\n"
            ResultsList.append([i, k, s, UnlikelyCharacters])
    if len(ResultsList) == 0:
        LabelCiphFeedback["text"] = "Guess too long for this ciphertext."
        return False
    ResultsList.sort(key = lambda x: x[3])
    return UpdateFrameGuesses()

# This function is invoked when the user chooses one of the
# suggested guesses. It reveals the corresponding part of
# the plain text according to the guess.
def GuessChosen(i, k, Guess):
    global PlainGrid
    TextPlain.delete("1.0", "end")
    for j in range(len(CiphGrid)):
        for l in range(len(Guess)):
            if k + l >= len(CiphGrid[j]):
                break
            PlainGrid[j][k + l] = chr(ord(Guess[l]) ^ CiphGrid[i][k + l] ^ CiphGrid[j][k + l])
    PrintPlaintext()

# The window is divided into two frames.
FrameTexts = ttk.Frame(master = root)
FrameTexts["borderwidth"] = 5
FrameTexts["relief"] = "sunken"
FrameGuesses = ttk.Frame(master = root)
FrameGuesses["borderwidth"] = 5
FrameGuesses["relief"] = "sunken"
FrameTexts.pack(side = "left", fill = "both", expand = True)
FrameGuesses.pack(side = "left", fill = "both")

# The labels, entries, buttons and text fields
# are defined and adjusted.
LabelCiphCaption = ttk.Label(master = FrameTexts,
                             text = """Ciphertext (hex values, separated by whitespaces, each line encrypted with the same key)""")
LabelCiphCaption.pack(side = "top", fill = "x", padx = 25, pady = 5)
FrameCiphBtnEntry = ttk.Frame(master = FrameTexts)
FrameCiphBtnEntry.pack(side = "top", padx = 15, pady = 5, fill = "x")
ButtonCiphLoad = ttk.Button(master = FrameCiphBtnEntry,
                            text = "Load cipher data from file:",
                            width = 30,
                            command = ButtonCiphLoadClick)
PathCiph = tk.StringVar(value = "./text.txt")
EntryCiph = ttk.Entry(master = FrameCiphBtnEntry, text = PathCiph)
ButtonCiphLoad.pack(side = "left", padx = 10)
EntryCiph.pack(side = "left", padx = 10, fill = "x", expand = True)
LoadAsText = tk.StringVar(value = 1)
CheckLoadAsText = ttk.Checkbutton(master = FrameTexts,
                                  text = "Load hex values as text instead of binary",
                                  variable = LoadAsText)
CheckLoadAsText.pack(side = "top", padx = 25, pady = 5, fill = "x")
LabelCiphFeedback = ttk.Label(master = FrameTexts, text = "")
LabelCiphFeedback.pack(side = "top", padx = 25, pady = 5, fill = "x")
TextCiph = tk.Text(master = FrameTexts, width = 10, wrap = "none")
TextCiph.pack(side = "top", fill = "both", expand = True, padx = 25, pady = 10)
FrameProcessCiph = ttk.Frame(master = FrameTexts)
FrameProcessCiph.pack(side = "top", fill = "both", pady = 5)
ButtonProcessCiph = ttk.Button(master = FrameProcessCiph,
                               text = "Process ciphertext",
                               width = 30,
                               command = CiphChanged)
ButtonProcessCiph.pack(side = "left", padx = 25)
LabelPlainCaption = ttk.Label(master = FrameTexts,
                             text = "Current state of your cracking attempts:")
LabelPlainCaption.pack(side = "top", fill = "x", padx = 25, pady = 5)
TextPlain = tk.Text(master = FrameTexts, width = 10, wrap = "none")
TextPlain.pack(side = "top", fill = "both", expand = True, padx = 25, pady = 10)

LabelGuessCaption = ttk.Label(master = FrameGuesses, text = "Guess for contained text:")
LabelGuessCaption.pack(side = "top", pady = 5)
Guess = tk.StringVar(value = "")
EntryGuess = ttk.Entry(master = FrameGuesses, textvariable = Guess)
EntryGuess.pack(side = "top", fill = "x", pady = 5)
GuessChangedRegistration = root.register(GuessChanged)
EntryGuess.config(validate = "key", validatecommand =  (GuessChangedRegistration, "%P"))
LabelOrderExplanation = ttk.Label(master = FrameGuesses,
                                  text = """Results that only contain A-Za-z0-9.,:;-!?' \" appear first""")
LabelOrderExplanation.pack(side = "top", pady = 5)


ListFramesGuess = [ttk.Frame(master = FrameGuesses) for i in range(40)]
ListLabelGuess = [ttk.Label(master = ListFramesGuess[i]) for i in range(len(ListFramesGuess))]
ListButtonGuess = [ttk.Button(master = ListFramesGuess[i],
                              text = "Use", width = 4) for i in range(len(ListFramesGuess))]
for i in range(len(ListFramesGuess)):
    ListButtonGuess[i].pack(side = "left")
    ListLabelGuess[i].pack(side = "left", fill = "x", expand = True)


#ListFramesGuess[i].pack(side = "top", fill = "x")
CiphGrid = []
PlainGrid = []


root.mainloop()
