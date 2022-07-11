import numpy as np
import scipy.io.wavfile as wav
import os, sys
import curses

def getUnit():
    a = int(input("Input the unit of space where averaging happens (0 to cancel):\n(1) Samples (relative to input sample rate)\n(2) Lowest frequency in the input file\n(3) Lowest note in the input file\nNumber (0-3): "))
    if a == 0:
        sys.exit("Cancelled")
    elif a == 1:
        return (int(input("Input the amount in samples: ")), 0)
    elif a == 2:
        return (int(input("Input the frequency: ")), 1)
    elif a == 3:
        b = int(input("Input the octave of the note (-2 to cancel, 4 being the Middle C): "))*12
        if b == -24:
            sys.exit("Cancelled")
        c = int(input("Input the number of the note (0 to cancel, 1 - C, 12 - B/H): "))-1
        if c == -1:
            sys.exit("Cancelled")
        b += c
        c = b - 57
        return (440*(2**(c/12)),1)

def output (number, total, totalSize):
    columns = os.get_terminal_size().columns
    spacing = (totalSize-len(str(number+1+(total*instance))))*" "
    mainString = (spacing+str(number+1+(total*instance))+"/"+str(total*(totalInstances+1))+" ")
    pbLength = (number+total*instance)*((columns-len(mainString))/(total*(totalInstances+1)))
    mainString += int(pbLength)*"█"
    pbFloat = (pbLength - int(pbLength)) * 8
    mainString += nonFullSymbols[int(pbFloat)]
    mainString += "\033[F"
    mainString += (columns-len(mainString))*" "
    print (mainString)


def centerAvg (wave):
    w_intermediate = np.empty(0,wave.dtype) 
    wf = np.empty(wave.shape,wave.dtype)
    total = int(wave.shape[0]/offset)
    totalSize = len (str(total*(totalInstances+1))) #here for optimization
    for i in range(0, total):
        first_index = i*offset-int(unit/2)
        first_index = first_index if first_index >= 0 else 0
        w_intermediate = wave[first_index:i*offset+int(unit/2)]
        w_im_avg = np.cast[wave.dtype](np.average(w_intermediate))

        #print(w_intermediate[0], end=" ")
        w_intermediate = wave[first_index:i*offset+int(unit/2)] - w_im_avg
        wf[i*offset:(i+1)*offset] = w_intermediate[0:offset]
        #print(w_im_avg, w_intermediate[0])
        if i % 50:
            output(i, total, totalSize)
    return wf

def centerMinMax (wave):
    w_intermediate = np.empty(0,wave.dtype) 
    wf = np.empty(wave.shape,wave.dtype)
    total = int(wave.shape[0]/offset)
    totalSize = len (str(total*(totalInstances+1))) #here for optimization
    for i in range(0, total):
        first_index = i*offset-int(unit/2)
        first_index = first_index if first_index >= 0 else 0
        w_intermediate = wave[first_index:i*offset+int(unit/2)]
        ma = max(w_intermediate)
        mi = min(w_intermediate)
        w_im_avg = np.cast[wave.dtype]((ma+mi)/2)
        #print(w_intermediate[0], end=" ")
        w_intermediate = wave[first_index:i*offset+int(unit/2)] - w_im_avg
        wf[i*offset:(i+1)*offset] = w_intermediate[0:offset]
        #print(w_im_avg, w_intermediate[0])
        output(i, total, totalSize)
        if i % 50:
            output(i, total, totalSize)
    return wf

def center (wave):
    if algorithm == 0:
        wf = centerAvg(wave)
    else:
        wf = centerMinMax(wave)
    return wf


nonFullSymbols = [" ", "▏", "▎", "▍", "▌", "▋", "▊", "▉"]
directory = ""
dirlevel = 2


unit, f = getUnit()
offset = 4 #samples per try
algorithm = int( input ("Select the centering algorithm (0 to cancel):\n(1) Averaging\n(2) Min-max\nThe number (0-2): "))
if algorithm == 0:
    sys.exit("Cancelled")
algorithm-=1

for i in range (dirlevel):
    i = 0
    dirs = []
    for entry in os.scandir(directory):
        if entry.is_dir():
            i+=1
            dirs.append(entry.name)
    if len(dirs) == 1:
        directory += dirs[0] + "/"
        print("Found only one directory, progressing automatically")
        continue
    print("Input the number to select the directory (0 to cancel):")
    for i in range(len(dirs)):
        print("("+str(i+1)+") "+dirs[i])
    dirnum = int(input ("The number (0-"+str(i)+"): "))
    if dirnum == 0:
        sys.exit("Cancelled")
    else:
        directory += dirs[dirnum-1] + "/"
directory += input("Input the file name: ")
print("\n")

sr1, w1 = wav.read(directory)

if f == 1:
    unit = sr1 / unit
unit *= 1.2

w1l = (w1[:,0])
w1r = (w1[:,1])

instance = 0
totalInstances = 0

stereo = (w1l - w1r).any()

if not stereo:
    w1fl = center(w1l)
    w1fr = w1fl
else:
    totalInstances = 1
    w1fl = center(w1l)
    instance = 1
    w1fr = center(w1r)

print ("\n \n")
w1f = np.empty(w1.shape,w1.dtype)

w1f[:,0] = w1fl
w1f[:,1] = w1fr
wav.write(directory, sr1, w1f)

