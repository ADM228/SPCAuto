import numpy as np
import scipy.io.wavfile as wav
import os, sys, time

directory = ""
dirlevel = 2
unit = 100 #ms

echodet = input ("Detect echo? [Y/N]: ")
echodet = True if echodet == "y" or echodet == "Y" else False

echosep = False
if echodet:
    echosep = input ("Separate the echo? [Y/N]: ")
    echosep = True if echosep == "y" or echosep == "Y" else False


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

index = input ("Select a specific track? [Y/N]: ")
index = True if index == "y" or index == "Y" else False

if index == True:
    nrange = ""
    while not nrange.isnumeric():
        nrange = input ("Select a specific track (0 to cancel): \n (0-"+str(i-1)+"): ")
    nrange = [int(nrange)]
else:
    nrange = range (1, i)

for i in nrange:
    zeramount = ""
    sr1, w1 = wav.read(directory + str(i) + ".wav")
    d1 = w1.dtype
    if "int" in str(d1):
        max1 = np.iinfo(d1).max
        min1 = np.iinfo(d1).min
    elif "float" in str(d1):
        max1 = np.finfo(d1).max
        min1 = np.finfo(d1).min
    else:
        print ("I don't know what a '"+str(d1)+"' is, please report to alexmush#7063 on Discord")
    
    print ("Track", str(i)+":1 loaded successfully!")
    if echodet:
        sr2, w2 = wav.read(directory + str(i) + "e.wav")
        d2 = w2.dtype
        if d2 != d1:
            print ("Why is your echo exported in a different format than the main file? Using the main file's type properties anyway")
        print ("Track", str(i)+":2 loaded successfully!")
    if pad:
        while not zeramount.isdigit():
            zeramount = input("Input the padding in units ("+str(unit)+"ms): ")
        zeramount = int(zeramount)
        if zeramount != 0:
            zer = np.zeros((int(sr1*unit*zeramount*0.001),2),d1)
            w1 = np.vstack((zer,w1))
            if echodet:
                w2 = np.vstack((zer,w2))
        print ("Track "+str(i)+" padded successfully!")
    if echodet:
        shape = w1.shape[0] - w2.shape[0]
        if shape > 0:
            zer = np.zeros((shape,2))
            w2 = np.vstack((w2,zer))
        elif shape < 0:
            zer = np.zeros((abs(shape),2))
            w1 = np.vstack((w1,zer))
        w3 = w1 - w2
        echo = w3.any()
        print ("Echo of track ", i, "calculated successfully, it "+("has" if echo else "doesn't have")+" echo!")
    else:
        echo = False
    if echo:
        stereo = ((w2[:,1]) - (w2[:,0])).any()
        print("Track "+str(i)+" is "+("stereo!" if stereo else "mono!"))
        estereo = ((w3[:,1]) - (w3[:,0])).any()
        print("Track "+str(i)+"'s echo is "+("stereo!" if estereo else "mono!"))
    else:
        stereo = ((w1[:,1]) - (w1[:,0])).any()
        print("Track "+str(i)+" is "+("stereo!" if stereo else "mono!"))
    if echosep:
        wav.write(directory + str(i) + ".wav", sr2, w2.astype(d1))
        if echo:
            wav.write(directory + str(i) + "e.wav", sr2, w3.astype(d1))
        else:
            os.remove(directory + str(i) + "e.wav")
    else:
        wav.write(directory + str(i) + ".wav", sr1, w1.astype(d1))
    print("Files #"+str(i), "written sucessfully!")
    if echodet:
        paramstr +=(str(i)+": "+("Stereo; " if stereo else "Mono;   ")+("" if not echodet else "E" if echo else "-")+(" " if not echo else "Stereo; " if estereo else "Mono;   "))
    else:
        paramstr +=(str(i)+": "+("Stereo; " if stereo else "Mono;   "))
    if echosep:
        paramstr +="Main Amp: "+(str(min(max1/np.amax(w2), min1/np.amin(w2))))+"; Echo Amp: "+(str(min(max1/np.amax(w3), min1/np.amin(w3)) if echo else "")+" ")
    else:
        paramstr +="Amp: " + (str(min(max1/np.amax(w1), min1/np.amin(w1))))
#    if stereo:
#        paramstr +=(str(np.amax((w2[:,1])-(w2[:,0]
# Stereo difference, pointless
    paramstr += "\n"
print(paramstr)
