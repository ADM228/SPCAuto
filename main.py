import numpy as np
import scipy.io.wavfile as wav
import os, sys

directory = ""
dirlevel = 2
unit = 100 #ms

echodet = input ("Detect echo? [Y/N]: ")
echodet = True if echodet == "y" or echodet == "Y" else False

pad = input ("Pad the tracks? [Y/N]: ")
pad = True if pad == "y" or pad == "Y" else False

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
directory += input("Input the beginning of file names: ") + "_"
paramstr = ""
for i in range (1,int(input("Input the amount of tracks: "))+1):
    sr1, w1 = wav.read(directory + str(i) + ".wav")
    print ("Track", str(i)+":1 loaded successfully!")
    if echodet:
        sr2, w2 = wav.read(directory + str(i) + "e.wav")
        print ("Track", str(i)+":2 loaded successfully!")
    if pad:
        zeramount = int(input("Input the padding in units ("+str(unit)+"ms): "))
        if zeramount != 0:
            zer = np.zeros((int(sr1*unit*zeramount*0.001),2),np.float32)
            w1 = np.vstack((zer,w1))
            if echodet:
                w2 = np.vstack((zer,w2))
        print ("Track "+str(i)+" padded successfully!")
    if echodet:
        shape = w1.shape[0] - w2.shape[0]
        if shape > 0:
            zer = np.zeros((shape,2))
            w2 = np.vstack((zer,w2))
        elif shape < 0:
            zer = np.zeros((abs(shape),2))
            w1 = np.vstack((zer,w1))
        w3 = w1 - w2
        echo = w3.any()
        print ("Echo of", i, "calculated successfully, it "+("has" if echo else "doesn't have")+" echo!")
    stereo = ((w1[:,1]) - (w1[:,0])).any()
    print("Track "+str(i)+" is "+("stereo!" if stereo else "mono!"))
    if echodet:
        wav.write(directory + str(i) + ".wav", sr1, w2)
        if echo:
            wav.write(directory + str(i) + "e.wav", sr1, w3)
        else:
            os.remove(directory + str(i) + "e.wav")
    else:
        wav.write(directory + str(i) + ".wav", sr1, w1)
    print("Files #"+str(i), "written sucessfully!")
    paramstr +=(str(i)+": "+("" if not echodet else "E" if echo else "-")+("S" if stereo else "M")+"\n")
print(paramstr)