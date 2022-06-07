import numpy as np
import scipy.io.wavfile as wav
import os, sys

directory = ""
dirlevel = 2
unit = 100 #ms

for i in range (dirlevel):
    i = 0
    dirs = []
    print("Input the number to select the directory (0 to cancel):")
    for entry in os.scandir(directory):
        if entry.is_dir():
            i+=1
            print("(" + str(i) + ") " + entry.name)
            dirs.append(entry.name)
    dirnum = int(input ("The number (0-"+str(i)+"): "))
    if dirnum == 0:
        sys.exit("Cancelled")
    else:
        directory += dirs[dirnum-1] + "/"
directory += input("Input the beginning of file names: ") + "_"
paramstr = ""
for i in range (7,int(input("Input the amount of tracks: "))+1):
    sr1, w1 = wav.read(directory + str(i) + ".wav")
    print ("Track", str(i)+":1 loaded successfully!")
    sr2, w2 = wav.read(directory + str(i) + "e.wav")
    print ("Track", str(i)+":2 loaded successfully!")
    zeramount = int(input("Input the padding in units ("+str(unit)+"ms): "))
    if zeramount != 0:
        zer = np.zeros((int(sr1*unit*zeramount*0.001),2),np.float32)
        w1 = np.vstack((zer,w1))
        w2 = np.vstack((zer,w2))
    print ("Track "+str(i)+" padded successfully!")
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
    wav.write(directory + str(i) + ".wav", sr1, w2)
    if echo:
        wav.write(directory + str(i) + "e.wav", sr1, w3)
    else:
        os.remove(directory + str(i) + "e.wav")
    print("Files #"+str(i), "written sucessfully!")
    paramstr +=(str(i)+": "+("E" if echo else "-")+("S" if stereo else "M")+"\n")
print(paramstr)