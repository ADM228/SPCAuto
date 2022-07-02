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

directory = "/home/alexmush/Soundtracks/"
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

w_intermediate = np.empty(0,w1l.dtype) 

w1fl = np.empty(w1l.shape,w1l.dtype)

for i in range(0, int(w1l.shape[0]/offset)):
    first_index = i*offset-int(unit/2)
    first_index = first_index if first_index >= 0 else 0
    w_intermediate = w1l[first_index:i*offset+int(unit/2)]
    if algorithm == 0:
        w_im_avg = np.cast[w1l.dtype](np.average(w_intermediate))
    else: 
        ma = max(w_intermediate)
        mi = min(w_intermediate)
        w_im_avg = np.cast[w1l.dtype]((ma+mi)/2)

    #print(w_intermediate[0], end=" ")
    w_intermediate = w1l[first_index:i*offset+int(unit/2)] - w_im_avg
    w1fl[i*offset:(i+1)*offset] = w_intermediate[0:offset]
    #print(w_im_avg, w_intermediate[0])
    print ("\033[F"+str(i+1)+"/"+str(w1l.shape[0]/offset))

w1r = (w1[:,1])

w1fr = np.empty(w1r.shape,w1r.dtype)

for i in range(0, int(w1r.shape[0]/offset)):
    first_index = i*offset-int(unit/2)
    first_index = first_index if first_index >= 0 else 0
    w_intermediate = w1r[first_index:i*offset+int(unit/2)]
    if algorithm == 0:
        w_im_avg = np.cast[w1r.dtype](np.average(w_intermediate))
    else: 
        ma = max(w_intermediate)
        mi = min(w_intermediate)
        w_im_avg = np.cast[w1r.dtype]((ma+mi)/2)

    #print(w_intermediate[0], end=" ")
    w_intermediate = w1r[first_index:i*offset+int(unit/2)] - w_im_avg
    w1fr[i*offset:(i+1)*offset] = w_intermediate[0:offset]
    #print(w_im_avg, w_intermediate[0])
    print ("\033[F"+str(i+1)+"/"+str(w1r.shape[0]/offset))

w1f = np.empty(w1.shape,w1.dtype)

w1f[:,0] = w1fl
w1f[:,1] = w1fr
wav.write(directory, sr1, w1f)

