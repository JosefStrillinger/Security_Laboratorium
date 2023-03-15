# tkinter provides GUI objects and commands
import tkinter as tk
import tkinter.ttk as ttk

# An object (root) is created which represents the window.
# Its title and full screen property are set.
root = tk.Tk()
root.title("Vigenère Encryption")
root.wm_state("zoomed")

# This function normalizes the parameter text according to the
# settings "Keep blanks" and "Keep non-alphabetic chars".
def NormalizeText(text, strict = False):
    s = ""
    for c in text:
        if ((ord(c) <= ord("Z")) and (ord(c) >= ord("A"))):
            s += c
        elif ((ord(c) <= ord("z")) and (ord(c) >= ord("a"))):
            s += chr(ord(c) + ord("A") - ord("a"))
        elif ((c == "ä") or (c == "Ä")):
            s += "AE"
        elif ((c == "ö") or (c == "Ö")):
            s += "OE"
        elif ((c == "ü") or (c == "Ü")):
            s += "UE"
        elif (c == "ß"):
            s += "SS"
        elif ((c == " ") or (ord(c) == 10)):
            if ((KeepBlanks.get() == "1") and not strict):
                s += " "
        elif ((KeepNonalpha.get() == "1") and not strict):
            s += c
    return s

# The labels used to interact with the user are cleared.
def ClearFeedbackLabels():
    LabelPlainFeedback["text"] = ""
    LabelKeyFeedback["text"] = ""
    LabelCiphFeedback["text"] = ""

# This function is invoked when the user clicks the button
# "Load plaintext from file".
# It tries to open a textfile with the name specified in the
# corresponding entry field. Further, it tells the user
# whether the loading of the textfile succeeded and, if so,
# prints its contents in the text field below.
def ButtonPlainLoadClick():
    ClearFeedbackLabels()
    try:
        with open(PathPlain.get(), mode = "rt", encoding = "utf-8") as PlainFile:
            plain = PlainFile.read()
    except:
        LabelPlainFeedback["text"] = "An error occurred while reading the file."
    else:
        if plain == "":
            LabelPlainFeedback["text"] = "File empty"
        else:
            plain = NormalizeText(plain)
            TextPlain.delete("1.0", "end")
            TextPlain.insert("1.0", plain)
            LabelPlainFeedback["text"] = "File loaded successfully."

# This function is invoked when the user clicks the button
# "Save ciphertext to file".
# It tries to create or rewrite a textfile with the name
# specified in the corresponding entry field and to write
# the contents of the text field below into the file.
# Further, it tells the user whether the writing to the
# textfile succeeded.
def ButtonCiphSaveClick():
    ClearFeedbackLabels()
    ciph = TextCiph.get("1.0", "end")[:-1]
    if len(ciph) < 1:
        LabelCiphFeedback["text"] = "Nothing to save"
        return
    try:
        with open(PathCiph.get(), mode = "wt", encoding = "utf-8") as CiphFile:
            if (CiphFile.write(ciph) != len(ciph)):
                raise Exception
    except:
        LabelCiphFeedback["text"] = "An error occurred while saving to file."
    else:
        LabelCiphFeedback["text"] = "Ciphertext saved successfully."

# This function is invoked when the user clicks the button
# "Encode".
# It normalizes the plain text and the key, checks if the
# key is valid and executes the encryption.
def ButtonEncodeClick():
    ClearFeedbackLabels()   
    ciph = ""
    plain = TextPlain.get("1.0", "end")[:-1]
    plain = NormalizeText(plain)
    TextPlain.delete("1.0", "end")
    TextPlain.insert("1.0", plain)
    key = NormalizeText(Key.get(), strict = True)
    Key.set(key) 
    keylength = len(key)
    if keylength == 0:
        LabelKeyFeedback["text"] = "No valid key entered"
        return
    i = 0
    for p in plain:
        if ((ord(p) < ord("A")) or (ord(p) > ord("Z"))):
            ciph += p
        else:
            a = ord(p) + ord(key[i % keylength]) - ord("A")
            i += 1
            if a > ord("Z"):
                a -= 26
            ciph += chr(a)
    TextCiph.delete("1.0", "end")
    TextCiph.insert("1.0", ciph)

# The window is divided into three frames.
FramePlain = ttk.Frame(master = root)
FramePlain["borderwidth"] = 5
FramePlain["relief"] = "sunken"
FrameKey = ttk.Frame(master = root)
FrameKey["borderwidth"] = 5
FrameKey["relief"] = "sunken"
FrameCiph = ttk.Frame(master = root)
FrameCiph["borderwidth"] = 5
FrameCiph["relief"] = "sunken"
FramePlain.pack(side = "left", fill = "both", expand = True)
FrameKey.pack(side = "left", fill = "y")
FrameCiph.pack(side = "left", fill = "both", expand = True)

# The labels, entries, buttons and text fields
# are defined and adjusted.
LabelPlainCaption = ttk.Label(master = FramePlain, text = "Plaintext")
LabelPlainCaption.pack(side = "top", pady = 5)
FramePlainBtnEntry = ttk.Frame(master = FramePlain)
FramePlainBtnEntry.pack(side = "top", padx = 15, pady = 5, fill = "x")
ButtonPlainLoad = ttk.Button(master = FramePlainBtnEntry,
                             text = "Load plaintext from file:",
                             width = 30,
                             command = ButtonPlainLoadClick)
PathPlain = tk.StringVar(value = "./text.txt")
EntryPlain = ttk.Entry(master = FramePlainBtnEntry, text = PathPlain)
ButtonPlainLoad.pack(side = "left", padx = 10)
EntryPlain.pack(side = "left", padx = 10, fill = "x", expand = True)
LabelPlainFeedback = ttk.Label(master = FramePlain, text = "")
LabelPlainFeedback.pack(side = "top", padx = 25, pady = 5, fill = "x")
TextPlain = tk.Text(master = FramePlain, width = 10)
TextPlain.pack(side = "bottom", fill = "both", expand = True, padx = 25, pady = 10)

LabelKeyCaption = ttk.Label(master = FrameKey, text = "Key")
LabelKeyCaption.pack(side = "top", pady = 5)
Key = tk.StringVar(value = "KEY")
EntryKey = ttk.Entry(master = FrameKey, text = Key)
EntryKey.pack(side = "top", padx = 25, pady = 7, fill = "x")
LabelKeyFeedback = ttk.Label(master = FrameKey, text = "")
LabelKeyFeedback.pack(side = "top", padx = 25, pady = 5, fill = "x")
KeepBlanks = tk.StringVar(value = 0)
KeepNonalpha = tk.StringVar(value = 0)
CheckKeyKeepBlanks = ttk.Checkbutton(master = FrameKey, text = "Keep blanks",
                                     variable = KeepBlanks)
CheckKeyKeepSpecials = ttk.Checkbutton(master = FrameKey, text = "Keep non-alphabetic chars",
                                       variable = KeepNonalpha)
CheckKeyKeepBlanks.pack(side = "top", padx = 25, pady = 5, fill = "x")
CheckKeyKeepSpecials.pack(side = "top", padx = 25, pady = 5, fill = "x")
ButtonEncode = ttk.Button(master = FrameKey,
                            text = "Encode",
                            command = ButtonEncodeClick)
ButtonEncode.pack(side = "top", padx = 25, pady = 25, fill = "x")

LabelCiphCaption = ttk.Label(master = FrameCiph, text = "Ciphertext")
LabelCiphCaption.pack(side = "top", pady = 5)
FrameCiphBtnEntry = ttk.Frame(master = FrameCiph)
FrameCiphBtnEntry.pack(side = "top", padx = 15, pady = 5, fill = "x")
ButtonCiphSave = ttk.Button(master = FrameCiphBtnEntry,
                            text = "Save ciphertext to file:",
                            width = ButtonPlainLoad.cget("width"),
                            command = ButtonCiphSaveClick)
PathCiph = tk.StringVar(value = "./text.txt")
EntryCiph = ttk.Entry(master = FrameCiphBtnEntry, text = PathCiph)
ButtonCiphSave.pack(side = "left", padx = 10)
EntryCiph.pack(side = "left", padx = 10, fill = "x", expand = True)
LabelCiphFeedback = ttk.Label(master = FrameCiph, text = "")
LabelCiphFeedback.pack(side = "top", padx = 25, pady = 5, fill = "x")
TextCiph = tk.Text(master = FrameCiph, width = 10)
TextCiph.pack(side = "bottom", fill = "both", expand = True, padx = 25, pady = 10)


root.mainloop()
