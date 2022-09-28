file = open("Laborübung-1/mini.bmp","rb")
data = file.read()
file.close()

print(list(data))

bf_OffBits = 0
bm_width = 0
bm_height = 0
biBitCount = 0

def bytesToInt(amount, pos, val, root):
    if(amount>0):
        #BitMap uses"Little Endian" => first byte is lowest, lat byte is highest
        #00000001 00000001 0..0 0..0 => 1 256 0 0
        #So root has to start at 0 and get higher by every bit for a specific information
        val+=list(data)[pos]*(256**(root))
        pos+=1
        amount-=1
        root+=1
        bytesToInt(amount, pos, val, root)
    return val

def checkIfCorrect():
    global bf_OffBits, bm_width, bm_height, biBitCount
    #Check if the first two bytes are 'B' and 'M' in ASCII for BitMap
    if(chr(list(data)[0]) == 'B' and chr(list(data)[1]) == 'M'):
        print("ok")
    else:
        print("Failure")
        return

    #Skip to next two Infos (= 8 Bytes)
    #Check the bfOffBits (4 Bytes)
    bf_OffBits = bytesToInt(4, 10, 0, 0)
    if(bf_OffBits == 54):
        print("OffBits: " + str(bf_OffBits))
    else:
        print("Failure")
        return
    
    #Ignore biSize (=4 Bytes)
    #Read width and height (=8 Bytes)
    bm_width = bytesToInt(4, 18, 0, 0)
    bm_height = bytesToInt(4, 22, 0, 0)
    print("Width: " + str(bm_width) + ", Height: " + str(bm_height))
    
    #Ignore biPlanes (=2 Bytes)
    #Read biBitCound (=Farbtiefe)
    biBitCount = bytesToInt(2, 28, 0, 0)
    if(biBitCount == 24):
        print("Farbtiefe: " + str(biBitCount))
    else:
        print("Failure")
        return
    
    #Check biCompression
    if(bytesToInt(4, 30, 0, 0) == 0):
        print("ok")
    else:
        print("Failure")
        return
    
    #Skip next 3 infos (=12 Bytes)
    #Check biClrUsed
    if(bytesToInt(4, 46, 0, 0) == 0):
        print("ok")
    else:
        print("Failure")
        return

    #Skip next info (=4 Bytes)
    
def checkIfMessageFits(text):
    #each char is equal to 8 bytes
    bytesNeeded = len(text)*8
    #the first 54 bytes are used for other infos
    bytesAvailable = len(list(data))-54
    if(bytesAvailable >= bytesNeeded):
        print("Message fits!")
    else:
        print("Message is too big!")
        
def addHiddenText(text):
    byte_arr = [char for char in text]
    for c in byte_arr:
        print(c)
                
    return

def getSecretText():
    return

checkIfCorrect()
checkIfMessageFits("asd")
checkIfMessageFits("ajshd")
addHiddenText("asd")