import numpy as np
import scipy.io.wavfile as wav
import os, sys

directory = ""
dirlevel = 2
unit = 100 #ms

echodet = input ("Detect echo? [Y/N]: ")
echodet = True if echodet == "y" or echodet == "Y" else False

echosep = False
# if echodet:
#     echosep = input ("Separate the echo? [Y/N]: ")
#     echosep = True if echosep == "y" or echosep == "Y" else False
# Automatic echo separation is disabled because it is bullshit for some reason

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
    dirnum = int(input ("The number (0-"+str(len(dirs))+"): "))
    if dirnum == 0:
        sys.exit("Cancelled")
    else:
        directory += dirs[dirnum-1] + "/"
directory += input("Input the beginning of file names: ") + "_"
paramstr = ""

i = 1
while os.path.isfile(directory+str(i)+".wav"):
    i+=1
print ("Detected", str(i-1), "tracks")
for i in range (i):
    zeramount = ""
    sr1, w1 = wav.read(directory + str(i) + ".wav")
    print ("Track", str(i)+":1 loaded successfully!")
    if echodet:
        sr2, w2 = wav.read(directory + str(i) + "e.wav")
        print ("Track", str(i)+":2 loaded successfully!")
    if pad:
        while not zeramount.isdigit():
            zeramount = input("Input the padding in units ("+str(unit)+"ms): ")
        zeramount = int(zeramount)
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
    if echosep:
        w10 = w1[:,0]
        w11 = w1[:,1]
        w20 = w2[:,0]
        w21 = w2[:,1]
        w30 = np.subtract(w20, w10)
        w31 = np.subtract(w21, w11)
        w3[:,0] = w30
        w3[:,1] = w31
    if echodet:
        stereo = ((w2[:,1]) - (w2[:,0])).any()
        print("Track "+str(i)+" is "+("stereo!" if stereo else "mono!"))
        estereo = ((w3[:,1]) - (w3[:,0])).any()
        print("Track "+str(i)+"'s echo is "+("stereo!" if estereo else "mono!"))
    else:
        stereo = ((w1[:,1]) - (w1[:,0])).any()
        print("Track "+str(i)+" is "+("stereo!" if stereo else "mono!"))
    if echosep:
        wav.write(directory + str(i) + ".wav", sr1, w2)
        if echo:
            wav.write(directory + str(i) + "e.wav", sr1, w3)
        else:
            os.remove(directory + str(i) + "e.wav")
    else:
        wav.write(directory + str(i) + ".wav", sr1, w1)
    print("Files #"+str(i), "written sucessfully!")
    if echodet:
        paramstr +=(str(i)+": "+("S" if stereo else "M")+("" if not echodet else "E" if echo else "-")+("S" if estereo else "M")+"\n")
    else:
        paramstr +=(str(i)+": "+("" if not echodet else "E" if echo else "-")+"\n")
print(paramstr)