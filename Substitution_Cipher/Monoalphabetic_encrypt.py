# tkinter provides GUI objects and commands
import tkinter as tk
import tkinter.ttk as ttk

# An object (root) is created which represents the window.
# Its title and full screen property are set.
root = tk.Tk()
root.title("Monoalphabetic encryption")
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

# This function is invoked when the user selects a radio
# button corresponding to one of the various cipher modes.
# It en- and disables the entries accordingly.
# Eventually, it executes the encryption.
def ChangeMode():
    ClearFeedbackLabels()
    if GeneralMode.get() == 0:
        ComboText[0].set("a")
        UpdateCombosCaesarMode()
        ComboSubst[0]["state"] = "normal"
        for i in range(1, 26):
            ComboSubst[i]["state"] = "disabled"
    elif GeneralMode.get() == 1:
        for i in range(26):
            ComboSubst[i]["state"] = "normal"
            ComboText[i].set(chr(ord("A")+i))
    else:
        for i in range(26):
            ComboText[i].set(chr(ord("Z")-i))
            ComboSubst[i]["state"] = "disabled"
    UpdatePlaintext()

# This function fills all the combo boxes with ascending
# letters starting from the letter of the first one.
def UpdateCombosCaesarMode():
    c = ComboText[0].get()
    for i in range(1, 26):
        if c == "z":
            c = "a"
        else:
            c = chr(ord(c) + 1)
        ComboText[i].set(c)

# This function creates the list of selectable letters
# for the combo box with the given index, i.e. all
# letters that have not been chosen for other combo boxes.
def FillComboList(index):
    if GeneralMode.get() == 0:
        l = []
        skip_list = []
    else:
        l = [chr(ord("A")+index)]
        skip_list = [ComboText[i].get() for i in range(26) if i != index]
    for i in range(26):
        c = chr(ord("a")+i)
        if not c in skip_list:
            l.append(c)
    ComboSubst[index]["values"] = l

# This function is invoked when a combo box loses the
# focus. It checks if the entered string is valid,
# updates the other combo boxes and applies the
# encryption to the plaintext.
def FocusOutCombo(contents, index):
    c = contents.get()
    if len(c) == 0:
        if GeneralMode.get() == 1:
            c = chr(ord("A")+index)
        else:
            c = "a"
    else:
        c = c[-1]
        if (ord(c) < ord("a")) or (ord(c) > ord("z")):
            if GeneralMode.get() == 1:
                c = chr(ord("A")+index)
            else:
                c = "a"
    contents.set(c)
    if GeneralMode.get() == 0:
        UpdateCombosCaesarMode()
    else:
        for i in range(26):
            if i == index:
                continue
            if c == ComboText[i].get():
                ComboText[i].set(chr(ord("A")+i))
                break
    UpdatePlaintext()

# This function is invoked whenever the encryption mode
# is changed. It applies the encryption to the plaintext.
def UpdatePlaintext():
    plain = NormalizeText(TextPlain.get("1.0", "end")[:-1])
    TextPlain.delete("1.0", "end")
    TextPlain.insert("1.0", plain)
    cipher = ""
    for c in plain:
        if ((ord(c) < ord("A")) or (ord(c) > ord("Z"))):
            cipher += c
        else:
            cipher += ComboText[ord(c)-ord("A")].get()
    TextCiph.delete("1.0", "end")
    TextCiph.insert("1.0", cipher)

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
KeepBlanks = tk.StringVar(value = 0)
KeepNonalpha = tk.StringVar(value = 0)
CheckKeyKeepBlanks = ttk.Checkbutton(master = FrameKey, text = "Keep blanks",
                                     variable = KeepBlanks)
CheckKeyKeepSpecials = ttk.Checkbutton(master = FrameKey, text = "Keep non-alphabetic chars",
                                       variable = KeepNonalpha)
CheckKeyKeepBlanks.pack(side = "top", padx = 25, pady = 5, fill = "x")
CheckKeyKeepSpecials.pack(side = "top", padx = 25, pady = 5, fill = "x")
GeneralMode = tk.IntVar(value = 0)
RadioButtonAtbash = ttk.Radiobutton(master = FrameKey, text = "Atbash",
                                    value = -1, variable = GeneralMode,
                                    command = ChangeMode)
RadioButtonCaesar = ttk.Radiobutton(master = FrameKey, text = "Caesar",
                                    value = 0, variable = GeneralMode,
                                    command = ChangeMode)
RadioButtonGeneral = ttk.Radiobutton(master = FrameKey, text = "General",
                                    value = 1, variable = GeneralMode,
                                    command = ChangeMode)
RadioButtonAtbash.pack(side = "top", fill = "x", padx = 25, pady = 5)
RadioButtonCaesar.pack(side = "top", fill = "x", padx = 25, pady = 5)
RadioButtonGeneral.pack(side = "top", fill = "x", padx = 25, pady = 5)
FrameKeyPad1 = ttk.Frame(master = FrameKey)
FrameKeyPad2 = ttk.Frame(master = FrameKey)
FrameKeyPad2["borderwidth"] = 5
FrameKeyPad2["relief"] = "sunken"
FrameKeyPad3 = ttk.Frame(master = FrameKey)
FrameKeyPad1.pack(side = "left", fill = "both", padx = 25)
FrameKeyPad3.pack(side = "right", fill = "both", padx = 25)
FrameKeyPad2.pack(side = "right", fill = "both", expand = True)
FramesSubst = []
LabelSubst = []
ComboSubst = []
ComboText = []
for i in range(26):
    if i < 13:
        FramesSubst.append(ttk.Frame(master = FrameKeyPad1))
    else:
        FramesSubst.append(ttk.Frame(master = FrameKeyPad3))
    FramesSubst[i].pack(side = "top", fill = "both", expand = True)
    LabelSubst.append(ttk.Label(master = FramesSubst[i], text = chr(ord("A")+i) + " "))
    ComboText.append(tk.StringVar(value = chr(ord("A")+i)))
    ComboSubst.append(ttk.Combobox(master = FramesSubst[i],
                                   width = 2,
                                   textvariable = ComboText[i],
                                   postcommand = lambda i=i: FillComboList(i)))
    ComboSubst[i].bind("<FocusOut>", lambda event, i=i: FocusOutCombo(ComboText[i], i))   
for i in range(13):
    LabelSubst[i].pack(side = "left", fill = "x", expand = True)
    ComboSubst[i].pack(side = "right")
    LabelSubst[i+13].pack(side = "left", fill = "x", expand = True)
    ComboSubst[i+13].pack(side = "right")

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

    
ChangeMode()
root.mainloop()
