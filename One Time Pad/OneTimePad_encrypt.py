# tkinter provides GUI objects and commands
# random provides random numbers for the
# generation of random keys
import tkinter as tk
import tkinter.ttk as ttk
import random

# An object (root) is created which represents the window.
# Its title and full screen property are set.
root = tk.Tk()
root.title("One-time pad encryption")
root.wm_state("zoomed")

# This function formats the input data as a string of
# hexadecimal values for each byte separated by spaces,
# e.g. "a3 e2 00"
def ToHexStr(data):
    data = list(data)
    DataList = [format(int(data[i]), "x").zfill(2) for i in range(len(data))]
    return " ".join(DataList)

# The labels used to interact with the user are cleared.
def ClearFeedbackLabels():
    LabelPlainFeedback["text"] = ""
    LabelKeyFeedback["text"] = ""
    LabelCiphFeedback["text"] = ""

# This function is invoked when the user clicks the button
# "Load plain data from file".
# It tries to open a binary file with the name specified
# in the corresponding entry field. Further, it tells the
# user whether the loading of the file succeeded and, if so,
# prints its contents in the text field below as a string
# of hexadecimal values for each byte separated by spaces.
def ButtonPlainLoadClick():
    ClearFeedbackLabels()
    plain = ""
    try:
        with open(PathPlain.get(), mode = "br") as PlainFile:
            plain = ToHexStr(PlainFile.read())
    except:
        LabelPlainFeedback["text"] = "An error occurred while reading the file."
    else:
        if plain == "":
            LabelPlainFeedback["text"] = "File empty"
        else:
            TextPlain.delete("1.0", "end")
            TextPlain.insert("1.0", plain)
            LabelPlainFeedback["text"] = "File loaded successfully."

# This function is invoked when the user clicks the button
# "Save cipher data to file".
# It tries to create or rewrite a file with the name
# specified in the corresponding entry field and to write
# the contents of the text field below into the file.
# Further, it tells the user whether the writing to the
# file succeeded.
# It expects the text field to contain a string of
# hexadecimal numbers between 00 and ff separated by spaces.
# Accordingly to the checkboxes it creates
# - a binary file,
# - a textfile with hexadecimal values separated by spaces
# - a textfile with hexadecimal values separated by spaces
#   where each line is as long as the deliberately limited key.
def ButtonCiphSaveClick():
    ClearFeedbackLabels()
    ciph = TextCiph.get("1.0", "end")[:-1]
    if len(ciph) < 1:
        LabelCiphFeedback["text"] = "Nothing to save"
        return    
    ciph = ciph.split()
    CiphList = [0 for i in range(len(ciph))]
    try:
        for i in range(len(ciph)):
            CiphList[i] = int(ciph[i], 16)
            if CiphList[i] < 0 or CiphList[i] > 255:
                raise Exception
    except:
        LabelKeyFeedback["text"] = "Invalid cipher data"
        return
    try:
        if SaveAsText.get() == "0":
            with open(PathCiph.get(), mode = "bw") as CiphFile:
                if (CiphFile.write(bytearray(CiphList)) != len(CiphList)):
                    raise Exception
        else:
            if InsertNewlines.get() == "0":
                ciph = " ".join(ciph)
            else:
                n = int(SpinboxKeyLength.get())
                s = ""
                for i in range((len(ciph) // n) + (1 if len(ciph) % n != 0 else 0)):
                    s += " ".join(ciph[i*n:(i+1)*n]) + "\n"
                ciph = s.rstrip()
            with open(PathCiph.get(), mode = "tw", encoding = "utf-8") as CiphFile:
                if (CiphFile.write(ciph) != len(ciph)):
                    raise Exception
    except:
        LabelCiphFeedback["text"] = "An error occurred while saving to file."
    else:
        LabelCiphFeedback["text"] = "Cipher saved successfully."

# This function updates the text of the InsertNewlines
# checkbox, when the limited key length is changed.
def KeyLengthChanged():
    CheckInsertNewlines["text"] = "Insert newlines every " + SpinboxKeyLength.get() + " bytes"

# This function disables the InsertNewlines checkbox
# when the SaveAsText option is unchecked.
def CheckSaveAsTextChanged(var, index, mode):
    CheckInsertNewlines["state"] = "normal" if SaveAsText.get() == "1" else "disabled"

# This function is invoked when the user clicks the button
# "Load key from file".
# It tries to open a binary file with the name specified
# in the corresponding entry field. Further, it tells the
# user whether the loading of the textfile succeeded and,
# if so, prints its contents as hexadecimal values separated
# by spaces in the text field below.
def ButtonKeyLoadClick():
    ClearFeedbackLabels()
    key = ""
    try:
        with open(PathKey.get(), mode = "br") as KeyFile:
            Key = ToHexStr(KeyFile.read())
    except:
        LabelKeyFeedback["text"] = "An error occurred while reading the file."
    else:
        if Key == "":
            LabelKeyFeedback["text"] = "File empty"
        else:
            TextKey.delete("1.0", "end")
            TextKey.insert("1.0", Key)
            LabelKeyFeedback["text"] = "File loaded successfully."

# This function is invoked when the user clicks the button
# "Save key to file".
# It tries to create or rewrite a binary file with the name
# specified in the corresponding entry field and to write
# the contents of the text field below into the file.
# Further, it tells the user whether the writing to the
# file succeeded.
# It expects the text field to contain a string of
# hexadecimal numbers between 00 and ff separated by spaces.
def ButtonKeySaveClick():
    ClearFeedbackLabels()
    key = TextKey.get("1.0", "end")[:-1]
    if key == "":
        LabelKeyFeedback["text"] = "Nothing to save"
        return
    key = key.split()
    KeyList = [0 for i in range(len(key))]
    try:
        for i in range(len(key)):
            KeyList[i] = int(key[i], 16)
            if KeyList[i] < 0 or KeyList[i] > 255:
                raise Exception
    except:
        LabelKeyFeedback["text"] = "Invalid key"
        return
    try:
        with open(PathKey.get(), mode = "bw") as KeyFile:
            if (KeyFile.write(bytearray(KeyList)) != len(KeyList)):
                raise Exception
    except:
        LabelKeyFeedback["text"] = "An error occurred while saving to file."
    else:
        LabelKeyFeedback["text"] = "Key saved successfully."

# Enables the KeyLength spinbox when needed.
def ChangeKeyGenerationMode():
    SpinboxKeyLength["state"] = "normal" if (KeyGenerationMode.get() == 2) else "disabled"

# This function checks the plain data and, if needed,
# the key data for the right format. If needed, it
# generates a new key randomly.
def ButtonApplyKeyClick():

    def GenerateKey(length):
        KeyList = [format(random.randint(0, 255), "x").zfill(2) for i in range(length)]
        TextKey.delete("1.0", "end")
        TextKey.insert("1.0", " ".join(KeyList))

    ClearFeedbackLabels()
    TextCiph.delete("1.0", "end")
    plain = TextPlain.get("1.0", "end")[:-1]
    if plain == "":
        LabelKeyFeedback["text"] = "No text to encrypt"
        return
    plain = plain.split()
    PlainList = [0 for i in range(len(plain))]
    try:
        for i in range(len(plain)):
            PlainList[i] = int(plain[i], 16)
            if PlainList[i] < 0 or PlainList[i] > 255:
                raise Exception
    except:
        LabelKeyFeedback["text"] = "Invalid plain data"
        return
    if KeyGenerationMode.get() == 1:
        GenerateKey(len(plain))
    elif KeyGenerationMode.get() == 2:
        GenerateKey(int(SpinboxKeyLength.get()))
    key = TextKey.get("1.0", "end")[:-1]
    if key == "":
        LabelKeyFeedback["text"] = "No key entered"
        return
    key = key.split()
    KeyList = [0 for i in range(len(key))]
    try:
        for i in range(len(key)):
            KeyList[i] = int(key[i], 16)
            if KeyList[i] < 0 or KeyList[i] > 255:
                raise Exception
    except:
        LabelKeyFeedback["text"] = "Invalid key"
        return
    if len(key) < len(plain):
        LabelKeyFeedback["text"] = "Warning: Key too short, key reused!"
    CipherList = [0 for i in range(len(plain))]
    for i in range(len(plain)):
        CipherList[i] = format(PlainList[i] ^ KeyList[i % len(KeyList)], "x").zfill(2)
    TextCiph.delete("1.0", "end")
    TextCiph.insert("1.0", " ".join(CipherList))

# The window is divided into three frames.
FramePlain = ttk.Frame(master = root)
FramePlain["borderwidth"] = 5
FramePlain["relief"] = "sunken"
FrameSettings = ttk.Frame(master = root)
FrameSettings["borderwidth"] = 5
FrameSettings["relief"] = "sunken"
FrameCiph = ttk.Frame(master = root)
FrameCiph["borderwidth"] = 5
FrameCiph["relief"] = "sunken"
FramePlain.pack(side = "left", fill = "both", expand = True)
FrameSettings.pack(side = "left", fill = "y")
FrameCiph.pack(side = "left", fill = "both", expand = True)

# The labels, entries, buttons and text fields
# are defined and adjusted.
LabelPlainCaption = ttk.Label(master = FramePlain, text = "Plain data (hex values separated by spaces)")
LabelPlainCaption.pack(side = "top", pady = 5)
FramePlainBtnEntry = ttk.Frame(master = FramePlain)
FramePlainBtnEntry.pack(side = "top", padx = 15, pady = 5, fill = "x")
ButtonPlainLoad = ttk.Button(master = FramePlainBtnEntry,
                             text = "Load plain data from file:",
                             width = 30,
                             command = ButtonPlainLoadClick)
PathPlain = tk.StringVar(value = "./text.txt")
EntryPlain = ttk.Entry(master = FramePlainBtnEntry, text = PathPlain)
ButtonPlainLoad.pack(side = "left", padx = 10)
EntryPlain.pack(side = "left", padx = 10, fill = "x", expand = True)
LabelPlainFeedback = ttk.Label(master = FramePlain, text = "")
LabelPlainFeedback.pack(side = "top", padx = 25, pady = 5, fill = "x")
TextPlain = tk.Text(master = FramePlain, width = 10)
TextPlain.pack(side = "top", fill = "both", expand = True, padx = 25, pady = 10)

LabelSettings = ttk.Label(master = FrameSettings, text = "Settings")
LabelSettings.pack(side = "top", pady = 5)

FrameKeyGeneration = ttk.Frame(master = FrameSettings)
FrameKeyGeneration.pack(side = "top", fill = "both", pady = 5)
FrameKeyGenerationMode = ttk.Frame(master = FrameKeyGeneration)
FrameKeyGenerationMode["relief"] = "groove"
FrameKeyGenerationMode.pack(side = "left", fill = "both", ipady = 5)
KeyGenerationMode = tk.IntVar(value = 1)
RadioButtonCurrentKey = ttk.Radiobutton(master = FrameKeyGenerationMode,
                                        text = "Use current key",
                                        value = 0, variable = KeyGenerationMode,
                                        command = ChangeKeyGenerationMode)
RadioButtonRandom = ttk.Radiobutton(master = FrameKeyGenerationMode,
                                    text = "Generate random key\nwith appropriate length",
                                    value = 1, variable = KeyGenerationMode,
                                    command = ChangeKeyGenerationMode)
RadioButtonRandomLimited = ttk.Radiobutton(master = FrameKeyGenerationMode,
                                           text = "Generate random key\nwith length:",
                                           value = 2, variable = KeyGenerationMode,
                                           command = ChangeKeyGenerationMode)
RadioButtonCurrentKey.pack(side = "top", fill = "x", padx = 22, pady = 5)
RadioButtonRandom.pack(side = "top", fill = "x", padx = 22, pady = 5)
RadioButtonRandomLimited.pack(side = "top", fill = "x", padx = 22, pady = 5)
SpinboxKeyLength = ttk.Spinbox(master = FrameKeyGenerationMode,
                               from_ = 2, to = 150, width = 3,
                               command = KeyLengthChanged)
SpinboxKeyLength.set(50)
SpinboxKeyLength.pack(side = "top")
ButtonApplyKey = ttk.Button(master = FrameKeyGeneration,
                            text = "Apply",
                            command = ButtonApplyKeyClick)
ButtonApplyKey.pack(side = "right", fill = "x", expand = True, padx = 5)

LabelKeyCaption = ttk.Label(master = FrameSettings, text = "Key (hex values separated by spaces)")
LabelKeyCaption.pack(side = "top", pady = 5)
FrameKey = ttk.Frame(master = FrameSettings)
FrameKey["relief"] = "groove"
FrameKey.pack(side = "top", fill = "both", expand = True, pady = 5)
FrameKeyLoadSaveButtons = ttk.Frame(master = FrameKey)
FrameKeyLoadSaveButtons.pack(side = "top", padx = 10, pady = 15, fill = "x")
ButtonKeyLoad = ttk.Button(master = FrameKeyLoadSaveButtons,
                           text = "Load key from file:",
                           width = 20,
                           command = ButtonKeyLoadClick)
ButtonKeySave = ttk.Button(master = FrameKeyLoadSaveButtons,
                           text = "Save key to file:",
                           width = 20,
                           command = ButtonKeySaveClick)
ButtonKeyLoad.pack(side = "left", padx = 10, pady = 3)
ButtonKeySave.pack(side = "left", padx = 10)
PathKey = tk.StringVar(value = "./key.bin")
EntryKeyPath = ttk.Entry(master = FrameKey, text = PathKey)
EntryKeyPath.pack(side = "top", padx = 20, pady = 3, fill = "x")
LabelKeyFeedback = ttk.Label(master = FrameKey, text = "")
LabelKeyFeedback.pack(side = "top", padx = 20, pady = 3, fill = "x")
TextKey = tk.Text(master = FrameKey, width = 10)
TextKey.pack(side = "top", fill = "both", expand = True, padx = 20, pady = 5)

LabelCiphCaption = ttk.Label(master = FrameCiph, text = "Cipher data (hex values separated by spaces)")
LabelCiphCaption.pack(side = "top", pady = 5)
FrameCiphBtnEntry = ttk.Frame(master = FrameCiph)
FrameCiphBtnEntry.pack(side = "top", padx = 15, pady = 5, fill = "x")
ButtonCiphSave = ttk.Button(master = FrameCiphBtnEntry,
                            text = "Save cipher data to file:",
                            width = ButtonPlainLoad.cget("width"),
                            command = ButtonCiphSaveClick)
PathCiph = tk.StringVar(value = "./text.txt")
EntryCiph = ttk.Entry(master = FrameCiphBtnEntry, text = PathCiph)
ButtonCiphSave.pack(side = "left", padx = 10)
EntryCiph.pack(side = "left", padx = 10, fill = "x", expand = True)
LabelCiphFeedback = ttk.Label(master = FrameCiph, text = "")
LabelCiphFeedback.pack(side = "top", padx = 25, pady = 5, fill = "x")
SaveAsText = tk.StringVar(value = 1)
SaveAsText.trace_add("write", CheckSaveAsTextChanged)
CheckSaveAsText = ttk.Checkbutton(master = FrameCiph,
                                  text = "Save hex values as text instead of binary",
                                  variable = SaveAsText)
CheckSaveAsText.pack(side = "top", padx = 25, pady = 5, fill = "x")
InsertNewlines = tk.StringVar(value = 1)
CheckInsertNewlines = ttk.Checkbutton(master = FrameCiph,
                                      text = "",
                                      variable = InsertNewlines)
CheckInsertNewlines.pack(side = "top", padx = 45, pady = 5, fill = "x")
TextCiph = tk.Text(master = FrameCiph, width = 10)
TextCiph.pack(side = "bottom", fill = "both", expand = True, padx = 25, pady = 10)


ChangeKeyGenerationMode()
KeyLengthChanged()
root.mainloop()
