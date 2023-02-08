# tkinter provides GUI objects and commands
import tkinter as tk
import tkinter.ttk as ttk

# An object (root) is created which represents the window.
# Its title and full screen property are set.
root = tk.Tk()
root.title("Transpositional encryptions")
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
    LabelMethodFeedback["text"] = ""
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
# It enables the spin boxes and entries for the selected
# cipher mode and disables all others.
# Eventually, it executes the encryption.
def ChangeMethod():
    SpinboxSkytaleDiameter["state"] = "normal" if (Method.get() == 1) else "disabled"
    SpinboxRailLines["state"] = "normal" if (Method.get() == 2) else "disabled"
    EntryRedefenceKey["state"] = "normal" if (Method.get() == 3) else "disabled"
    SpinboxRotationLength["state"] = "normal" if (Method.get() == 4) else "disabled"
    SpinboxRotationAngle["state"] = "normal" if (Method.get() == 4) else "disabled"
    EntryColTrans1["state"] = "normal" if (Method.get() == 5) else "disabled"
    EntryColTrans2["state"] = "normal" if (Method.get() == 5 and
                                           DoubleColTrans.get() == "1") else "disabled"
    CheckDoubleColTrans["state"] = "normal" if (Method.get() == 5) else "disabled"
    CheckMyszkowski["state"] = "normal" if (Method.get() == 5) else "disabled"
    if (Method.get() != 5):
        Myszkowski.set("0")
    EntryDisrColTrans["state"] = "normal" if (Method.get() == 6) else "disabled"
    EntryDisrColTrans2["state"] = "normal" if (Method.get() == 7) else "disabled"
    EntryDisrColTrans2Num["state"] = "normal" if (Method.get() == 7) else "disabled"
    EntryADFGVX["state"] = "normal" if (Method.get() == 8) else "disabled"
    if Method.get() == 0:
        DoReverseCipher()
    elif Method.get() == 1:
        SkytaleDiameterChanged()
    elif Method.get() == 2:
        RailLinesChanged()
    elif Method.get() == 3:
        RedefenceKey.set(RedefenceKey.get())
    elif Method.get() == 4:
        RotationChanged()
    elif Method.get() == 5:
        ColTransKey1.set(ColTransKey1.get())
    elif Method.get() == 6:
        DisrColTransKey.set(DisrColTransKey.get())
    elif Method.get() == 7:
        DisrColTransKey2.set(DisrColTransKey2.get())
    elif Method.get() == 8:
        ADFGVXKey.set(ADFGVXKey.get())

# This function collects all necessary preparations for the
# ensuing encryption like clearing of text fields.
def PrepareForEncryption():
    ClearFeedbackLabels()
    TextCiph.delete("1.0", "end")
    TextExplanation.delete("1.0", "end")
    plain = NormalizeText(TextPlain.get("1.0", "end")[:-1])
    TextPlain.delete("1.0", "end")
    TextPlain.insert("1.0", plain)
    return plain

# This function encrypts the text contained in the left
# text field, by use of the reverse cipher.
def DoReverseCipher():
    plain = PrepareForEncryption()
    pass
    cipher = plain[::-1]
    #erase this line, its only purpose is to
    #avoid an error when running the script for the first time
    TextCiph.insert("1.0", cipher)

# This function encrypts the text contained in the left
# text field, imitating the skytale.
# The user has selected its diameter, i.e. the number
# of letters for one wrapping.
# In the explanation text field, the letters are printed
# diagonally to explain how the ciphertext is obtained.
def SkytaleDiameterChanged():
    plain = PrepareForEncryption()
    pass
    cipher = ""#erase this line, its only purpose is to
    #avoid an error when running the script for the first time
    explanation = ""#erase this line, its only purpose is to
    #avoid an error when running the script for the first time
    TextCiph.insert("1.0", cipher)
    TextExplanation.insert("1.0", explanation)

# This function encrypts the text contained in the left
# text field, by use of the rail fence.
# It is invoked, when the cipher mode is selected or when
# the number of lines of the zig-zag pattern is changed.
# In the explanation text field, the letters are printed
# in zig-zag to explain how the ciphertext is obtained.
def RailLinesChanged():
    plain = PrepareForEncryption()
    pass
    cipher = ""#erase this line, its only purpose is to
    #avoid an error when running the script for the first time
    explanation = ""#erase this line, its only purpose is to
    #avoid an error when running the script for the first time
    TextCiph.insert("1.0", cipher)
    TextExplanation.insert("1.0", explanation)

# This function encrypts the text contained in the left
# text field, by use of the redefence cipher.
# It is invoked, when the cipher mode is selected or when
# the keyword is changed.
# In the explanation text field, the letters are printed
# in zig-zag with preceding keyword letters to explain
# how the ciphertext is obtained.
def RedefenceKeyChanged(var, index, mode):
    plain = PrepareForEncryption()
    Key = NormalizeText(RedefenceKey.get(), strict = True)
    if Key != RedefenceKey.get():
        RedefenceKey.set(Key)
    pass
    cipher = ""#erase this line, its only purpose is to
    #avoid an error when running the script for the first time
    explanation = ""#erase this line, its only purpose is to
    #avoid an error when running the script for the first time
    TextCiph.insert("1.0", cipher)
    TextExplanation.insert("1.0", explanation)

# This function encrypts the text contained in the left
# text field, by use of the rotation cipher.
# It is invoked, when the cipher mode is selected or when
# the block size or the angle of rotation are changed.
def RotationChanged():
    plain = PrepareForEncryption()
    pass
    cipher = ""#erase this line, its only purpose is to
    #avoid an error when running the script for the first time
    explanation = ""#erase this line, its only purpose is to
    #avoid an error when running the script for the first time
    TextCiph.insert("1.0", cipher)
    TextExplanation.insert("1.0", explanation.strip())

# This function is invoked when the Myszkowski check
# box is altered. It simulates a change of the key.
def MyszkowskiChanged(var, index, mode):
    ColTransKeyChanged(0, 0, 0)

# This function is invoked when the double columnar
# transposition check box is altered.
# It simulates a change of the key.
def DoubleColTransChanged(var, index, mode):
    EntryColTrans2["state"] = "normal" if DoubleColTrans.get() == "1" else "disabled"
    ColTransKeyChanged(0, 0, 0)

# This function encrypts the text contained in the left
# text field, by use of the columnar transposition cipher.
# It is invoked, when the cipher mode is selected or the
# keyword is changed or the state of one of the check boxes.
def ColTransKeyChanged(var, index, mode):
    plain = PrepareForEncryption()
    Key1 = NormalizeText(ColTransKey1.get(), strict = True)
    if Key1 != ColTransKey1.get():
        ColTransKey1.set(Key1)
    Key2 = NormalizeText(ColTransKey2.get(), strict = True)
    if Key2 != ColTransKey2.get():
        ColTransKey2.set(Key2)
    pass
    cipher = ""#erase this line, its only purpose is to
    #avoid an error when running the script for the first time
    explanation = ""#erase this line, its only purpose is to
    #avoid an error when running the script for the first time
    TextCiph.insert("1.0", cipher)
    TextExplanation.insert("1.0", explanation)

# This function encrypts the text contained in the left
# text field, by use of the disrupted columnar
# transposition cipher with the comb approach.
# The first line is only filled until the first letter
# of the key, the next line only until the second and
# so on. All other entries are blanks (except in the
# last line).
# It is invoked, when the cipher mode is selected or the
# keyword is changed.
def DisrColTransKeyChanged(var, index, mode):
    plain = PrepareForEncryption()
    Key = NormalizeText(DisrColTransKey.get(), strict = True)
    if Key != DisrColTransKey.get():
        DisrColTransKey.set(Key)
    pass
    cipher = ""#erase this line, its only purpose is to
    #avoid an error when running the script for the first time
    explanation = ""#erase this line, its only purpose is to
    #avoid an error when running the script for the first time
    TextCiph.insert("1.0", cipher)
    TextExplanation.insert("1.0", explanation)

# This function encrypts the text contained in the left
# text field, by use of the disrupted columnar
# transposition cipher with numerical sequence approach.
# The position of the first letter of the disruption key
# yields after how many letters a blank space is inserted
# in the plain text and so on.
# It is invoked, when the cipher mode is selected or one
# of the keywords is changed.
def DisrColTransKey2Changed(var, index, mode):
    plain = PrepareForEncryption()
    Key1 = NormalizeText(DisrColTransKey2.get(), strict = True)
    if Key1 != DisrColTransKey2.get():
        DisrColTransKey2.set(Key1)
        #Normal Key
    Key2 = NormalizeText(DisrColTransKey2Num.get(), strict = True)
    if Key2 != DisrColTransKey2Num.get():
        DisrColTransKey2Num.set(Key2)
        #Disruption Key
    
    valuesOfNormalKeys = {}
    valuesOfDisruptionKeys = {}
    normalKeys = []
    disruptionKeys = []
    for l in range(len(DisrColTransKey2.get())):
        normalKeys.append([*DisrColTransKey2.get()][l]) if [*DisrColTransKey2.get()][l] not in normalKeys else normalKeys.append([*DisrColTransKey2.get()][l]+str(l))
    for l in range(len(DisrColTransKey2Num.get())):
        disruptionKeys.append([*DisrColTransKey2Num.get()][l]) if [*DisrColTransKey2Num.get()][l] not in disruptionKeys else disruptionKeys.append([*DisrColTransKey2Num.get()][l]+str(l))
    sortedNormalKeys = sorted(normalKeys)
    sortedDisruptionKeys = sorted(disruptionKeys)
    for c in normalKeys:
        valuesOfNormalKeys[c] = sortedNormalKeys.index(c)
        
    for c in disruptionKeys:
        valuesOfDisruptionKeys[c] = sortedDisruptionKeys.index(c)
    cypheredRows = []
    explanationRows = []
    for i in range(len(DisrColTransKey2.get())):
        cypheredRows.append([])
        
    for i in range(len(DisrColTransKey2.get())):
        explanationRows.append([])
    
    indexNormalKey = 0
    indexExplanationKey = 0
    indexDisruptionKey = 0
    while not plain == "":
        if len(DisrColTransKey2Num.get()) > 1:
            for c in range(valuesOfDisruptionKeys[disruptionKeys[indexDisruptionKey]]):
                if plain == "":
                    break
                cypheredRows[indexNormalKey].append(plain[0])
                explanationRows[indexExplanationKey].append(plain[0])
                plain = plain[1:]
                indexNormalKey = indexNormalKey + 1 if indexNormalKey < len(cypheredRows)-1 else 0
                indexExplanationKey = indexExplanationKey + 1 if indexExplanationKey < len(explanationRows)-1 else 0
            cypheredRows[indexNormalKey].append(" ")
            indexNormalKey = indexNormalKey + 1 if indexNormalKey < len(cypheredRows)-1 else 0
            explanationRows[indexExplanationKey].append(" ")
            indexExplanationKey = indexExplanationKey + 1 if indexExplanationKey < len(explanationRows)-1 else 0
            indexDisruptionKey = indexDisruptionKey + 1 if indexDisruptionKey < len(sortedDisruptionKeys)-1 else 0
        else:
            break
        
    cipher = ""
    print(cypheredRows)
    for i in range(len(cypheredRows)):
        for c in cypheredRows[normalKeys.index(sortedNormalKeys[i])]:
            cipher += c
    
    explanation = "Keyword: " + DisrColTransKey2.get() + "\nDisruption Key: " + DisrColTransKey2Num.get() + "\n______________________________\n"
    for i in range(max([len(i) for i in explanationRows])):
        for j in range(len(explanationRows)):
            explanation += str(explanationRows[j][0]) + "\t" if not explanationRows[j] == [] else "  "
            explanationRows[j].pop(0) if not explanationRows[j] == [] else None
        explanation += "\n"
    TextCiph.insert("1.0", cipher)
    TextExplanation.insert("1.0", explanation)

# This function encrypts the text contained in the left
# text field, by use of the ADFGVX cipher.
# First, the letters of the plain text are substituted
# by use of a fixed substitution table. Afterwards, a
# straight columnar transposition is applied.
# It is invoked, when the cipher mode is selected or
# the keyword is changed.
def ADFGVXKeyChanged(var, index, mode):
    plain = NormalizeText(PrepareForEncryption())
    Key = NormalizeText(ADFGVXKey.get(), strict = True)
    if Key != ADFGVXKey.get():
        ADFGVXKey.set(Key)
    pass
    cipher = ""#erase this line, its only purpose is to
    #avoid an error when running the script for the first time
    explanation = ""#erase this line, its only purpose is to
    #avoid an error when running the script for the first time
    TextCiph.insert("1.0", cipher)
    TextExplanation.insert("1.0", explanation)

# The window is divided into three frames.
FramePlain = ttk.Frame(master = root)
FramePlain["borderwidth"] = 5
FramePlain["relief"] = "sunken"
FrameMethod = ttk.Frame(master = root)
FrameMethod["borderwidth"] = 5
FrameMethod["relief"] = "sunken"
FrameCiph = ttk.Frame(master = root)
FrameCiph["borderwidth"] = 5
FrameCiph["relief"] = "sunken"
FramePlain.pack(side = "left", fill = "both", expand = True)
FrameMethod.pack(side = "left", fill = "y")
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
TextPlain.pack(side = "top", fill = "both", expand = True, padx = 25, pady = 10)

FrameExplanation = ttk.Frame(master = FramePlain)
FrameExplanation["relief"] = "groove"
FrameExplanation.pack(side = "bottom", fill = "both")
LabelExplanation = ttk.Label(master = FrameExplanation,
                             text = "Intermediate step for clarity")
LabelExplanation.pack(side = "top", pady = 5)
TextExplanation = tk.Text(master = FrameExplanation, width = 10, height = 25,
                          wrap = "none")
TextExplanation.pack(side = "bottom", fill = "both", expand = True, padx = 20, pady = 10)

LabelMethodSettings = ttk.Label(master = FrameMethod, text = "Settings")
LabelMethodSettings.pack(side = "top", pady = 5)
KeepBlanks = tk.StringVar(value = 0)
KeepNonalpha = tk.StringVar(value = 0)
CheckKeyKeepBlanks = ttk.Checkbutton(master = FrameMethod, text = "Keep blanks",
                                     variable = KeepBlanks)
CheckKeyKeepSpecials = ttk.Checkbutton(master = FrameMethod, text = "Keep non-alphabetic chars",
                                       variable = KeepNonalpha)
CheckKeyKeepBlanks.pack(side = "top", padx = 25, pady = 5, fill = "x")
CheckKeyKeepSpecials.pack(side = "top", padx = 25, pady = 5, fill = "x")
LabelMethodCaption = ttk.Label(master = FrameMethod, text = "Select cipher")
LabelMethodCaption.pack(side = "top", pady = 5)
Method = tk.IntVar(value = 0)

LabelMethodFeedback = ttk.Label(master = FrameMethod, text = "")
LabelMethodFeedback.pack(side = "top", pady = 5)

FrameMethodL = ttk.Frame(master = FrameMethod)
FrameMethodR = ttk.Frame(master = FrameMethod)
FrameMethodL.pack(side = "left", fill = "y")
FrameMethodR.pack(side = "right", fill = "y")
FrameReverse = ttk.Frame(master = FrameMethodL)
FrameReverse["relief"] = "groove"
FrameReverse.pack(side = "top", fill = "both")
RadioButtonReverse = ttk.Radiobutton(master = FrameReverse, text = "Reverse",
                                     value = 0, variable = Method,
                                     command = ChangeMethod)
RadioButtonReverse.pack(side = "top", pady = 5)

FrameSkytale = ttk.Frame(master = FrameMethodL)
FrameSkytale["relief"] = "groove"
FrameSkytale.pack(side = "top", fill = "both")
RadioButtonSkytale = ttk.Radiobutton(master = FrameSkytale, text = "Skytale",
                                     value = 1, variable = Method,
                                     command = ChangeMethod)
RadioButtonSkytale.pack(side = "top", pady = 5)
FrameSkytaleDiameter = ttk.Frame(master = FrameSkytale)
FrameSkytaleDiameter.pack(side = "top", fill = "both", padx = 10, pady = 8)
LabelSkytaleDiameter = ttk.Label(master = FrameSkytaleDiameter, text = "Diameter")
LabelSkytaleDiameter.pack(side = "left")
SpinboxSkytaleDiameter = ttk.Spinbox(master = FrameSkytaleDiameter,
                                     from_ = 2, to = 15, width = 3,
                                     command = SkytaleDiameterChanged)
SpinboxSkytaleDiameter.set(5)
SpinboxSkytaleDiameter.pack(side = "right", padx = 2)

FrameRail = ttk.Frame(master = FrameMethodL)
FrameRail["relief"] = "groove"
FrameRail.pack(side = "top", fill = "both")
RadioButtonSkytale = ttk.Radiobutton(master = FrameRail, text = "Rail fence",
                                     value = 2, variable = Method,
                                     command = ChangeMethod)
RadioButtonSkytale.pack(side = "top", pady = 5)
FrameRailLines = ttk.Frame(master = FrameRail)
FrameRailLines.pack(side = "top", fill = "both", padx = 10, pady = 8)
LabelRailLines = ttk.Label(master = FrameRailLines, text = "No. of lines")
LabelRailLines.pack(side = "left")
SpinboxRailLines = ttk.Spinbox(master = FrameRailLines,
                               from_ = 2, to = 15, width = 3,
                               command = RailLinesChanged)
SpinboxRailLines.set(5)
SpinboxRailLines.pack(side = "right", padx = 2)

FrameRedefence = ttk.Frame(master = FrameMethodL)
FrameRedefence["relief"] = "groove"
FrameRedefence.pack(side = "top", fill = "both")
RadioButtonRedefence = ttk.Radiobutton(master = FrameRedefence, text = "Redefence",
                                     value = 3, variable = Method,
                                     command = ChangeMethod)
RadioButtonRedefence.pack(side = "top", pady = 5)
FrameRedefenceKey = ttk.Frame(master = FrameRedefence)
FrameRedefenceKey.pack(side = "top", fill = "both", padx = 10, pady = 8)
LabelRedefenceKey = ttk.Label(master = FrameRedefenceKey, text = "Key")
LabelRedefenceKey.pack(side = "left")
RedefenceKey = tk.StringVar(value = "KEY")
RedefenceKey.trace_add("write", RedefenceKeyChanged)
EntryRedefenceKey = ttk.Entry(master = FrameRedefenceKey, text = RedefenceKey,
                              width = 11)
EntryRedefenceKey.pack(side = "right", padx = 2)

FrameRotation = ttk.Frame(master = FrameMethodL)
FrameRotation["relief"] = "groove"
FrameRotation.pack(side = "top", fill = "both")
RadioButtonRotation = ttk.Radiobutton(master = FrameRotation, text = "Rotation",
                                      value = 4, variable = Method,
                                      command = ChangeMethod)
RadioButtonRotation.pack(side = "top", pady = 5)
FrameRotationLength = ttk.Frame(master = FrameRotation)
FrameRotationLength.pack(side = "top", fill = "both", padx = 10, pady = 8)
LabelRotationLength = ttk.Label(master = FrameRotationLength, text = "Block size")
LabelRotationLength.pack(side = "left")
SpinboxRotationLength = ttk.Spinbox(master = FrameRotationLength,
                                    from_ = 2, to = 15, width = 3,
                                    command = RotationChanged)
SpinboxRotationLength.set(5)
SpinboxRotationLength.pack(side = "right", padx = 2)
FrameRotationAngle = ttk.Frame(master = FrameRotation)
FrameRotationAngle.pack(side = "top", fill = "both", padx = 10, pady = 8)
LabelRotationAngle = ttk.Label(master = FrameRotationAngle, text = "Angle of rotation")
LabelRotationAngle.pack(side = "left")
SpinboxRotationAngle = ttk.Spinbox(master = FrameRotationAngle,
                                   values = ["90°", "270°"], width = 5,
                                   wrap = True, command = RotationChanged)
SpinboxRotationAngle.set("90°")
SpinboxRotationAngle.pack(side = "right", padx = 2)

FrameColTrans = ttk.Frame(master = FrameMethodR)
FrameColTrans["relief"] = "groove"
FrameColTrans.pack(side = "top", fill = "both")
RadioButtonColTrans = ttk.Radiobutton(master = FrameColTrans, text = "Columnar transposition",
                                      value = 5, variable = Method,
                                      command = ChangeMethod)
RadioButtonColTrans.pack(side = "top", pady = 5)
FrameColTrans1 = ttk.Frame(master = FrameColTrans)
FrameColTrans1.pack(side = "top", fill = "both", padx = 10, pady = 8)
LabelColTrans1 = ttk.Label(master = FrameColTrans1, text = "Key 1")
LabelColTrans1.pack(side = "left")
ColTransKey1 = tk.StringVar(value = "KEY")
ColTransKey1.trace_add("write", ColTransKeyChanged)
EntryColTrans1 = ttk.Entry(master = FrameColTrans1, text = ColTransKey1,
                           width = 11)
EntryColTrans1.pack(side = "right", padx = 2)
Myszkowski = tk.StringVar(value = 0)
Myszkowski.trace_add("write", MyszkowskiChanged)
DoubleColTrans = tk.StringVar(value = 0)
DoubleColTrans.trace_add("write", DoubleColTransChanged)
CheckMyszkowski = ttk.Checkbutton(master = FrameColTrans,
                                  text = "Use Myszkowski",
                                  variable = Myszkowski)
CheckDoubleColTrans = ttk.Checkbutton(master = FrameColTrans,
                                      text = "Use double columnar\ntransposition",
                                      variable = DoubleColTrans)
CheckMyszkowski.pack(side = "top", padx = 10, fill = "x")
CheckDoubleColTrans.pack(side = "top", padx = 10, fill = "x")
FrameColTrans2 = ttk.Frame(master = FrameColTrans)
FrameColTrans2.pack(side = "top", fill = "both", padx = 10, pady = 8)
LabelColTrans2 = ttk.Label(master = FrameColTrans2, text = "Key 2")
LabelColTrans2.pack(side = "left")
ColTransKey2 = tk.StringVar(value = "KEY")
ColTransKey2.trace_add("write", ColTransKeyChanged)
EntryColTrans2 = ttk.Entry(master = FrameColTrans2, text = ColTransKey2,
                           width = 11)
EntryColTrans2.pack(side = "right", padx = 2)

FrameDisrColTrans = ttk.Frame(master = FrameMethodR)
FrameDisrColTrans["relief"] = "groove"
FrameDisrColTrans.pack(side = "top", fill = "both")
RadioButtonDisrColTrans = ttk.Radiobutton(master = FrameDisrColTrans,
                                          text = "Disr. col. transp. (comb)",
                                          value = 6, variable = Method,
                                          command = ChangeMethod)
RadioButtonDisrColTrans.pack(side = "top", pady = 5)
FrameDisrColTransKey = ttk.Frame(master = FrameDisrColTrans)
FrameDisrColTransKey.pack(side = "top", fill = "both", padx = 10, pady = 8)
LabelDisrColTransKey = ttk.Label(master = FrameDisrColTransKey, text = "Key")
LabelDisrColTransKey.pack(side = "left")
DisrColTransKey = tk.StringVar(value = "KEY")
DisrColTransKey.trace_add("write", DisrColTransKeyChanged)
EntryDisrColTrans = ttk.Entry(master = FrameDisrColTransKey,
                              text = DisrColTransKey,
                              width = 11)
EntryDisrColTrans.pack(side = "right", padx = 2)

FrameDisrColTrans2 = ttk.Frame(master = FrameMethodR)
FrameDisrColTrans2["relief"] = "groove"
FrameDisrColTrans2.pack(side = "top", fill = "both")
RadioButtonDisrColTrans2 = ttk.Radiobutton(master = FrameDisrColTrans2,
                                           text = "Disr. col. transp. (num.)",
                                           value = 7, variable = Method,
                                           command = ChangeMethod)
RadioButtonDisrColTrans2.pack(side = "top", pady = 5)
FrameDisrColTransKey2 = ttk.Frame(master = FrameDisrColTrans2)
FrameDisrColTransKey2.pack(side = "top", fill = "both", padx = 10, pady = 8)
LabelDisrColTransKey2 = ttk.Label(master = FrameDisrColTransKey2, text = "Key")
LabelDisrColTransKey2.pack(side = "left")
DisrColTransKey2 = tk.StringVar(value = "KEY")
DisrColTransKey2.trace_add("write", DisrColTransKey2Changed)
EntryDisrColTrans2 = ttk.Entry(master = FrameDisrColTransKey2,
                                  text = DisrColTransKey2,
                                  width = 11)
EntryDisrColTrans2.pack(side = "right", padx = 2)
FrameDisrColTransKey2Num = ttk.Frame(master = FrameDisrColTrans2)
FrameDisrColTransKey2Num.pack(side = "top", fill = "both", padx = 10, pady = 8)
LabelDisrColTransKey2Num = ttk.Label(master = FrameDisrColTransKey2Num, text = "Disruption key")
LabelDisrColTransKey2Num.pack(side = "left")
DisrColTransKey2Num = tk.StringVar(value = "FILL")
DisrColTransKey2Num.trace_add("write", DisrColTransKey2Changed)
EntryDisrColTrans2Num = ttk.Entry(master = FrameDisrColTransKey2Num,
                                     text = DisrColTransKey2Num,
                                     width = 11)
EntryDisrColTrans2Num.pack(side = "right", padx = 2)

FrameADFGVX = ttk.Frame(master = FrameMethodR)
FrameADFGVX["relief"] = "groove"
FrameADFGVX.pack(side = "top", fill = "both")
RadioButtonADFGVX = ttk.Radiobutton(master = FrameADFGVX,
                                    text = "ADFGVX",
                                    value = 8, variable = Method,
                                    command = ChangeMethod)
RadioButtonADFGVX.pack(side = "top", pady = 5)
FrameADFGVXKey = ttk.Frame(master = FrameADFGVX)
FrameADFGVXKey.pack(side = "top", fill = "both", padx = 10, pady = 8)
LabelADFGVXKey = ttk.Label(master = FrameADFGVXKey, text = "Key")
LabelADFGVXKey.pack(side = "left")
ADFGVXKey = tk.StringVar(value = "KEY")
ADFGVXKey.trace_add("write", ADFGVXKeyChanged)
EntryADFGVX = ttk.Entry(master = FrameADFGVXKey,
                        text = ADFGVXKey,
                        width = 11)
EntryADFGVX.pack(side = "right", padx = 2)

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

    
ChangeMethod()
root.mainloop()
