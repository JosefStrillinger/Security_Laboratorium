# tkinter provides GUI objects and commands
# math provides floor, ceil and sqrt
# matplotlib provides the commands to print
# the statistical analysis of the letter
# frequencies
import tkinter as tk
import tkinter.ttk as ttk
import math
import matplotlib.pyplot as plt

# An object (root) is created which represents the window.
# Its title and full screen property are set.
root = tk.Tk()
root.title("Vigenère Crack")
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
    LabelFreqAnFeedback["text"] = ""
    LabelExamFeedback["text"] = ""
    LabelCiphFeedback["text"] = ""

# This function is invoked when the user clicks the button
# "Save plaintext to file".
# It tries to create or rewrite a textfile with the name
# specified in the corresponding entry field and to write
# the contents of the text field below into the file.
# Further, it tells the user whether the writing to the
# textfile succeeded.
def ButtonPlainSaveClick():
    ClearFeedbackLabels()
    plain = TextPlain.get("1.0", "end")[:-1]
    if len(plain) < 1:
        LabelPlainFeedback["text"] = "Nothing to save"
        return
    try:
        with open(PathPlain.get(), mode = "wt", encoding = "utf-8") as PlainFile:
            if (PathPlain.write(plain) != len(plain)):
                raise Exception
    except:
        LabelPlainFeedback["text"] = "An error occurred while saving to file."
    else:
        LabelPlainFeedback["text"] = "Plaintext saved successfully."

# This function is invoked when the user clicks the button
# "Load ciphertext from file".
# It tries to open a textfile with the name specified in the
# corresponding entry field. Further, it tells the user
# whether the loading of the textfile succeeded and, if so,
# prints its contents in the text field below.
def ButtonCiphLoadClick():
    ClearFeedbackLabels()
    try:
        with open(PathCiph.get(), mode = "rt", encoding = "utf-8") as CiphFile:
            ciph = CiphFile.read()
    except:
        LabelCiphFeedback["text"] = "An error occurred while reading the file."
    else:
        if ciph == "":
            LabelCiphFeedback["text"] = "File empty"
        else:
            ciph = NormalizeText(ciph)
            TextCiph.delete("1.0", "end")
            TextCiph.insert("1.0", ciph)
            LabelCiphFeedback["text"] = "File loaded successfully."

# This function is invoked when the user clicks the button
# "Load sample text from file".
# It tries to open a textfile with the name specified in the
# corresponding entry field. Further, it tells the user
# whether the loading of the textfile succeeded and, if so,
# prints its contents in the text field below.
def ButtonFreqAnLoadClick():
    ClearFeedbackLabels()
    try:
        with open(PathFreqAn.get(), mode = "rt", encoding = "utf-8") as SampleFile:
            FreqAnText = SampleFile.read()
    except:
        LabelFreqAnFeedback["text"] = "An error occurred while reading the file."
    else:
        if FreqAnText == "":
            LabelFreqAnFeedback["text"] = "File empty"
        else:
            TextFreqAn.delete("1.0", "end")
            TextFreqAn.insert("1.0", FreqAnText)
            LabelFreqAnFeedback["text"] = "File loaded successfully."       

# This function is invoked when the users clicks the button
# "Carry out Kasiski examination."
# 
def ButtonKasiskiClick():
    ClearFeedbackLabels()
    plt.close("all")
    StringLength = int(SpinboxKasiskiLength.get())
    RepeatedStrings = {}
    DivisorsOfDistances = {}

    def FindDivisorsOfDistances(coinc):
        def AddDivisor(d):
            if d > MaxDivisor:
                return
            if d in DivisorsOfDistances:
                DivisorsOfDistances[d] += 1
            else:
                DivisorsOfDistances.update({d: 1})
            
        for i in range(len(coinc) - 1):
            for j in range(i + 1, len(coinc)):
                dist = coinc[j] - coinc[i]
                for d in range(2, min(math.floor(math.sqrt(dist) + 1), MaxDivisor)):
                    if (dist % d == 0):
                        AddDivisor(d)
                        m = dist //d
                        if m != d:
                            AddDivisor(m)
                AddDivisor(dist)                            
    
    ciph = TextCiph.get("1.0", "end")[:-1]
    ciph = NormalizeText(ciph)
    TextCiph.delete("1.0", "end")
    TextCiph.insert("1.0", ciph)
    ciph = NormalizeText(ciph, strict = True)
    MaxDivisor = int(SpinboxKasiskiMaxDivisor.get())
    for pos in range(len(ciph) - StringLength - 1):
        s = ciph[pos : pos + StringLength]
        if s in RepeatedStrings:
            continue
        coinc = []
        for pos2 in range(pos + 2, len(ciph) - StringLength + 1):
            if s == ciph[pos2 : pos2 + StringLength]:
                coinc.append(pos2)
        if coinc != []:
            coinc.insert(0, pos)
            FindDivisorsOfDistances(coinc)
            RepeatedStrings.update({s: len(coinc)})
    try:
        MaxDivisor = max(DivisorsOfDistances.keys())
    except:
        LabelExamFeedback["text"] = "No string found repeatedly"
        return
    CoincidenceOfDivisors = [0 for i in range(2, MaxDivisor + 1)]
    for i in DivisorsOfDistances.keys():
        CoincidenceOfDivisors[i - 2] = DivisorsOfDistances[i]
    plt.figure("Possible key lengths")
    plt.bar([i for i in range(MaxDivisor - 1)],
            [CoincidenceOfDivisors[i] for i in range(MaxDivisor - 1)],
            tick_label = [i for i in range(2, MaxDivisor + 1)])
    plt.show()

def ButtonFriedmanClick():
    freq = CalculateFrequencies(UseWholeCipherText = True)
    if freq == 0:
        LabelExamFeedback["text"] = "No ciphertext to analyze"
        return
    if freq == 1:
        LabelExamFeedback["text"] = "No sample text to compare with"
        return
    CiphIndexOfCoincidence = 0
    SampleIndexOfCoincidence = 0
    RandomIndexOfCoincidence = 1/26
    CiphLength = sum(freq[0])
    SampleLength = sum(freq[1])
    for i in range(26):
        CiphIndexOfCoincidence += (freq[0][i] * (freq[0][i] - 1) /
                                   (CiphLength * (CiphLength - 1)))
        SampleIndexOfCoincidence += (freq[1][i] * (freq[1][i] - 1) /
                                     (SampleLength * (SampleLength - 1)))
    EstimatedKeyLength = ((SampleIndexOfCoincidence - RandomIndexOfCoincidence) * CiphLength /
                          ((CiphLength - 1) * CiphIndexOfCoincidence + SampleIndexOfCoincidence - RandomIndexOfCoincidence * CiphLength))
    LabelExamFeedback["text"] = "Estimated keylength: %.2f" % EstimatedKeyLength

def KeyLengthChanged():
    ClearFeedbackLabels()
    LabelKey["text"] = "A" * int(SpinboxKeyLength.get())
    SpinboxLetterSelection.set(1)
    SpinboxLetterSelection["to"] = int(SpinboxKeyLength.get())
    SpinboxLetterShift.set(0)
    ButtonShowFrequenciesClick(ShowFigure = (len(plt.get_fignums()) != 0))

def LetterSelectionChanged():
    ClearFeedbackLabels()
    key = LabelKey.cget("text")
    letter = int(SpinboxLetterSelection.get())
    SpinboxLetterShift.set(ord(key[letter - 1]) - ord("A"))

def LetterShiftChanged():
    key = LabelKey.cget("text")
    letter = int(SpinboxLetterSelection.get())
    shift = int(SpinboxLetterShift.get())
    key = key[:letter - 1] + chr(ord("A") + shift) + key[letter:]
    LabelKey["text"] = key
    ButtonShowFrequenciesClick(ShowFigure = (len(plt.get_fignums()) != 0))

def CalculateFrequencies(UseWholeCipherText = False):
    def CalcPlainText():
        for i in range(len(ciph)):
            n = ord(ciph[i]) - ord(key[i % KeyLength]) + ord("A")
            if n < ord("A"):
                n += 26
            PlainGrid[i // KeyLength][i % KeyLength] = chr(n)                
    
    ClearFeedbackLabels()
    key = LabelKey.cget("text")
    KeyLength = (len(key))
    letter = int(SpinboxLetterSelection.get())
    ciph = TextCiph.get("1.0", "end")[:-1]
    ciph = NormalizeText(ciph, strict = True)
    sample = TextFreqAn.get("1.0", "end")[:-1]
    sample = NormalizeText(sample, strict = True)
    if ciph == "":
        return 0
    PlainGrid = [[0 for j in range(KeyLength)] for i in range(math.ceil(len(ciph)/KeyLength))]
    if len(ciph) % KeyLength != 0:
        PlainGrid[-1] = [0 for j in range(len(ciph) % KeyLength)]
    CalcPlainText()
    TextPlain.delete("1.0", "end")
    TextPlain.insert("1.0", "\n".join(["".join(PlainGrid[i]) for i in range(len(PlainGrid))]))
    if sample == "":
        return 1
    SampleFrequencies = [0 for i in range(26)]
    CiphFrequencies = [0 for i in range(26)]
    for c in sample:
        SampleFrequencies[ord(c) - ord("A")] += 1
    if UseWholeCipherText:
        for c in ciph:
            CiphFrequencies[ord(c) - ord("A")] += 1
    else:
        for i in range(len(PlainGrid) - 1):
            CiphFrequencies[ord(PlainGrid[i][letter - 1]) - ord("A")] += 1
        if len(PlainGrid[-1]) >= letter:
            CiphFrequencies[ord(PlainGrid[-1][letter - 1]) - ord("A")] += 1
    return [CiphFrequencies, SampleFrequencies]

def ButtonShowFrequenciesClick(ShowFigure = True):
    freq = CalculateFrequencies()
    if freq == 0:
        LabelExamFeedback["text"] = "No ciphertext to analyze"
        return
    if freq == 1:
        if ShowFigure:
            LabelExamFeedback["text"] = "No sample text to compare with"
        return
    if not ShowFigure:
        return
    alphabet = [chr(ord("A") + i) for i in range(26)]
    fig = plt.figure("Letter frequencies")
    plt.subplot(211)
    plt.cla()
    plt.bar([i for i in range(52)],
            [freq[1][i % 26] for i in range(52)],
            tick_label = [alphabet[i % 26] for i in range(52)])
    plt.subplot(212)
    plt.cla()
    plt.bar([i for i in range(52)],
            [freq[0][i % 26] for i in range(52)],
            tick_label = [alphabet[i % 26] for i in range(52)])
    plt.show()

def ButtonEstimateShiftClick():
    LabelExamFeedback["text"] = "Function disabled"

def ButtonFormatPlaintextClick():
    def IsLetter(c):
        return ((ord(c) <= ord("Z")) and (ord(c) >= ord("A"))) or ((ord(c) <= ord("z")) and (ord(c) >= ord("a")))

    if CalculateFrequencies() == 0:
        LabelExamFeedback["text"] = "No ciphertext entered"
        return
    ciph = TextCiph.get("1.0", "end")[:-1]
    ciph = NormalizeText(ciph)
    TextCiph.delete("1.0", "end")
    TextCiph.insert("1.0", ciph)
    plain_old = TextPlain.get("1.0", "end")[:-1]
    i = 0
    plain = ""
    for c in ciph:
        if IsLetter(c):
            while not IsLetter(plain_old[i]):
                i += 1
            plain += plain_old[i]
            i += 1
        else:
            plain += c
    TextPlain.delete("1.0", "end")
    TextPlain.insert("1.0", plain)

# The window is divided into three frames.
FramePlain = ttk.Frame(master = root)
FramePlain["borderwidth"] = 5
FramePlain["relief"] = "sunken"
FrameExam = ttk.Frame(master = root)
FrameExam["borderwidth"] = 5
FrameExam["relief"] = "sunken"
FrameCiph = ttk.Frame(master = root)
FrameCiph["borderwidth"] = 5
FrameCiph["relief"] = "sunken"
FrameCiph.pack(side = "left", fill = "both", expand = True)
FrameExam.pack(side = "left", fill = "y")
FramePlain.pack(side = "left", fill = "both", expand = True)

# The labels, entries, buttons and text fields
# are defined and adjusted.
LabelCiphCaption = ttk.Label(master = FrameCiph, text = "Ciphertext")
LabelCiphCaption.pack(side = "top", pady = 5)
FrameCiphBtnEntry = ttk.Frame(master = FrameCiph)
FrameCiphBtnEntry.pack(side = "top", padx = 15, pady = 5, fill = "x")
ButtonCiphLoad = ttk.Button(master = FrameCiphBtnEntry,
                            text = "Load ciphertext from file:",
                            width = 30,
                            command = ButtonCiphLoadClick)
PathCiph = tk.StringVar(value = "./text.txt")
EntryCiph = ttk.Entry(master = FrameCiphBtnEntry, text = PathCiph)
ButtonCiphLoad.pack(side = "left", padx = 10)
EntryCiph.pack(side = "left", padx = 10, fill = "x", expand = True)
LabelCiphFeedback = ttk.Label(master = FrameCiph, text = "")
LabelCiphFeedback.pack(side = "top", padx = 25, pady = 5, fill = "x")
TextCiph = tk.Text(master = FrameCiph, width = 10)
TextCiph.pack(side = "top", fill = "both", expand = True, padx = 25, pady = 10)

LabelExamCaption = ttk.Label(master = FrameExam, text = "Settings")
LabelExamCaption.pack(side = "top", pady = 5)
KeepBlanks = tk.StringVar(value = 1)
KeepNonalpha = tk.StringVar(value = 1)
CheckboxKeepBlanks = ttk.Checkbutton(master = FrameExam,
                                     text = "Keep blanks",
                                     variable = KeepBlanks)
CheckboxKeepSpecials = ttk.Checkbutton(master = FrameExam,
                                       text = "Keep non-alphabetic chars",
                                       variable = KeepNonalpha)
CheckboxKeepBlanks.pack(side = "top", padx = 25, pady = 5, fill = "x")
CheckboxKeepSpecials.pack(side = "top", padx = 25, pady = 5, fill = "x")
LabelExamFeedback = ttk.Label(master = FrameExam, text = "")
LabelExamFeedback.pack(side = "top", padx = 25, pady = 5, fill = "x")
FrameKasiski = ttk.Frame(master = FrameExam)
FrameKasiski["relief"] = "groove"
FrameKasiski.pack(side = "top", fill = "both", padx = 10)
LabelKasiskiCaption = ttk.Label(master = FrameKasiski,
                                text = "Kasiski examination")
LabelKasiskiCaption.pack(side = "top", padx = 25, pady = 5, expand = True)
FrameKasiskiLength = ttk.Frame(master = FrameKasiski)
FrameKasiskiLength.pack(side = "top", fill = "x", expand = True,
                        padx = 15, pady = 5)
LabelKasiskiLength = ttk.Label(master = FrameKasiskiLength,
                               text = "Length of repeated strings  ")
LabelKasiskiLength.pack(side = "left", fill = "x", expand = True)
SpinboxKasiskiLength = ttk.Spinbox(master = FrameKasiskiLength,
                                   from_ = 2, to = 5, width = 3)
SpinboxKasiskiLength.set(3)
SpinboxKasiskiLength.pack(side = "left", padx = 2)
FrameKasiskiMaxDivisor = ttk.Frame(master = FrameKasiski)
FrameKasiskiMaxDivisor.pack(side = "top", fill = "x", expand = True,
                            padx = 15, pady = 5)
LabelKasiskiMaxDivisor = ttk.Label(master = FrameKasiskiMaxDivisor,
                               text = "Show max n bars")
LabelKasiskiMaxDivisor.pack(side = "left", fill = "x", expand = True)
SpinboxKasiskiMaxDivisor = ttk.Spinbox(master = FrameKasiskiMaxDivisor,
                                       from_ = 10, to = 50, width = 3)
SpinboxKasiskiMaxDivisor.pack(side = "left", padx = 2)
SpinboxKasiskiMaxDivisor.set(20)
ButtonKasiski = ttk.Button(master = FrameKasiski,
                           text = "Carry out Kasiski examination",
                           command = ButtonKasiskiClick)
ButtonKasiski.pack(side = "top", padx = 25, pady = 15, fill = "x")
ButtonFriedman = ttk.Button(master = FrameExam,
                            text = "Friedman estimation",
                            command = ButtonFriedmanClick)
ButtonFriedman.pack(side = "top", padx = 15, pady = 15)
FrameKey = ttk.Frame(master = FrameExam)
FrameKey["relief"] = "groove"
FrameKey.pack(side = "top", fill = "both", padx = 10)
LabelKeyCaption = ttk.Label(master = FrameKey,
                            text = "Find keyword")
LabelKeyCaption.pack(side = "top", padx = 25, pady = 5, expand = True)
FrameKeyLengthAssumption = ttk.Frame(master = FrameKey)
FrameKeyLengthAssumption.pack(side = "top", fill = "x", expand = True,
                              padx = 15, pady = 5)
LabelKeyLength = ttk.Label(master = FrameKeyLengthAssumption,
                           text = "Assumed key length")
LabelKeyLength.pack(side = "left", fill = "x", expand = True)
SpinboxKeyLength = ttk.Spinbox(master = FrameKeyLengthAssumption,
                               from_ = 1, to = 25,
                               width = 3, command = KeyLengthChanged)
SpinboxKeyLength.pack(side = "left", padx = 2)
SpinboxKeyLength.set(3)
FrameKeyAssumption = ttk.Frame(master = FrameKey)
FrameKeyAssumption.pack(side = "top", fill = "x", expand = True,
                        padx = 15, pady = 5)
LabelKeyExplanation = ttk.Label(master = FrameKeyAssumption,
                                text = "Assumed key")
LabelKeyExplanation.pack(side = "left", fill = "x", expand = True)
LabelKey = ttk.Label(master = FrameKeyAssumption, text = "AAA")
LabelKey.pack(side = "right", padx = 2)
FrameLetterSelection = ttk.Frame(master = FrameKey)
FrameLetterSelection.pack(side = "top", fill = "x", expand = True,
                          padx = 15, pady = 5)
LabelLetterSelection = ttk.Label(master = FrameLetterSelection,
                                 text = "Find n-th letter")
LabelLetterSelection.pack(side = "left", fill = "x", expand = True)
SpinboxLetterSelection = ttk.Spinbox(master = FrameLetterSelection,
                                     from_ = 1, to = SpinboxKeyLength.get(),
                                     width = 3, command = LetterSelectionChanged)
SpinboxLetterSelection.pack(side = "left", padx = 2)
SpinboxLetterSelection.set(1)
FrameLetterShift = ttk.Frame(master = FrameKey)
FrameLetterShift.pack(side = "top", fill = "x", expand = True,
                      padx = 15, pady = 5)
LabelLetterShift = ttk.Label(master = FrameLetterShift,
                             text = "Shift of the n-th letter")
LabelLetterShift.pack(side = "left", fill = "x", expand = True)
SpinboxLetterShift = ttk.Spinbox(master = FrameLetterShift,
                                 from_ = 0, to = 25, wrap = True,
                                 width = 3, command = LetterShiftChanged)
SpinboxLetterShift.pack(side = "left", padx = 2)
SpinboxLetterShift.set(0)
FrameEstimateShift = ttk.Frame(master = FrameKey)
FrameEstimateShift.pack(side = "top", fill = "x", expand = True,
                        padx = 15, pady = 5)
LabelEstimateShift = ttk.Label(master = FrameEstimateShift,
                               text = "Estimate shift")
LabelEstimateShift.pack(side = "left", fill = "x", expand = True)
ButtonEstimateShift = ttk.Button(master = FrameEstimateShift,
                          text = "auto",
                          command = ButtonEstimateShiftClick)
ButtonEstimateShift.pack(side = "left", fill = "x")
ButtonShowFrequencies = ttk.Button(master = FrameKey,
                                   text = "Show frequencies",
                                   command = ButtonShowFrequenciesClick)
ButtonShowFrequencies.pack(side = "top", padx = 15, pady = 15)
ButtonFormatPlaintext = ttk.Button(master = FrameExam,
                                   text = "Format plaintext",
                                   command = ButtonFormatPlaintextClick)
ButtonFormatPlaintext.pack(side = "top", padx = 15, pady = 15)

LabelPlainCaption = ttk.Label(master = FramePlain, text = "Plaintext")
LabelPlainCaption.pack(side = "top", pady = 5)
FramePlainBtnEntry = ttk.Frame(master = FramePlain)
FramePlainBtnEntry.pack(side = "top", padx = 15, pady = 5, fill = "x")
ButtonPlainSave = ttk.Button(master = FramePlainBtnEntry,
                             text = "Save plaintext to file:",
                             width = ButtonCiphLoad.cget("width"),
                             command = ButtonPlainSaveClick)
PathPlain = tk.StringVar(value = "./text.txt")
EntryPlain = ttk.Entry(master = FramePlainBtnEntry, text = PathPlain)
ButtonPlainSave.pack(side = "left", padx = 10)
EntryPlain.pack(side = "left", padx = 10, fill = "x", expand = True)
LabelPlainFeedback = ttk.Label(master = FramePlain, text = "")
LabelPlainFeedback.pack(side = "top", padx = 25, pady = 5, fill = "x")
TextPlain = tk.Text(master = FramePlain, width = 10)
TextPlain.pack(side = "bottom", fill = "both", expand = True, padx = 25, pady = 10)

FrameFreqAn = ttk.Frame(master = FrameCiph)
FrameFreqAn["relief"] = "groove"
FrameFreqAn.pack(side = "bottom", fill = "both")
LabelFreqAnCaption = ttk.Label(master = FrameFreqAn,
                               text = "Sample text in target language to estimate letter frequencies")
LabelFreqAnCaption.pack(side = "top", pady = 5)
FrameFreqAnBtnEntry = ttk.Frame(master = FrameFreqAn)
FrameFreqAnBtnEntry.pack(side = "top", padx = 10, pady = 5, fill = "x")
ButtonFreqAnLoad = ttk.Button(master = FrameFreqAnBtnEntry,
                            text = "Load sample text from file:",
                            width = ButtonCiphLoad.cget("width"),
                            command = ButtonFreqAnLoadClick)
PathFreqAn = tk.StringVar(value = "./sample.txt")
EntryFreqAn = ttk.Entry(master = FrameFreqAnBtnEntry, text = PathFreqAn)
ButtonFreqAnLoad.pack(side = "left", padx = 10)
EntryFreqAn.pack(side = "left", padx = 10, fill = "x", expand = True)
LabelFreqAnFeedback = ttk.Label(master = FrameFreqAn, text = "")
LabelFreqAnFeedback.pack(side = "top", padx = 20, pady = 5, fill = "x")
TextFreqAn = tk.Text(master = FrameFreqAn, width = 10, height = 5)
TextFreqAn.pack(side = "bottom", fill = "both", expand = True,
                padx = 20, pady = 10)

root.mainloop()
