import numpy as np
import scipy.io.wavfile as wav
import os, sys, time

directory = "/"
unit = 100 #ms
 
def is_valid_argument(arg):
    return ((arg in sys.argv) and (sys.argv.index(arg) < len(sys.argv)-1) and (sys.argv[sys.argv.index(arg)+1][0] != "-"))

def get_argument(arg):
    return sys.argv[sys.argv.index(arg)+1]

if not (("--echodet" in sys.argv) or ("--echosep" in sys.argv) or ("-ed" in sys.argv) or ("-es" in sys.argv) or ("--no-echo" in sys.argv) or ("-ne" in sys.argv)): 
    echodet = input ("Detect echo? [Y/N]: ")
    echodet = True if echodet == "y" or echodet == "Y" else False

    echosep = False
    if echodet:
        echosep = input ("Separate the echo? [Y/N]: ")
        echosep = True if echosep == "y" or echosep == "Y" else False
elif (("--echodet" in sys.argv) or ("--echosep" in sys.argv) or ("-ed" in sys.argv) or ("-es" in sys.argv)) and (("--no-echo" in sys.argv) or ("-ne" in sys.argv)):
    pro_echo = [i for i in sys.argv if ((i == "--echodet") or (i == "--echosep") or (i == "-ed") or (i == "-es"))]
    anti_echo = [i for i in sys.argv if ((i == "--no-echo") or (i == "-ne"))]
    sys.exit(f"Invalid arguments: " + (", ".join(pro_echo))+ " " + ("are" if len(pro_echo) > 1 else "is") + " incompatible with " + ", ".join(anti_echo))
else:
    echodet = (("--echodet" in sys.argv) or ("--echosep" in sys.argv) or ("-ed" in sys.argv) or ("-es" in sys.argv)) # echodet is implied when echosep
    echosep = (("--echosep" in sys.argv) or ("-es" in sys.argv))

if not (("--no-pad" in sys.argv) or ("-np" in sys.argv) or ("--pad" in sys.argv) or ("-p" in sys.argv)):
    pad = input ("Pad the tracks? [Y/N]: ")
    pad = True if pad == "y" or pad == "Y" else False
else:
    pad = ("--pad" in sys.argv) or ("-p" in sys.argv)

if not (("--compact-output" in sys.argv) or ("-co" in sys.argv) or ("--verbose-output" in sys.argv) or ("-vo" in sys.argv)):
    outlevel = 0
elif (("--compact-output" in sys.argv) or ("-co" in sys.argv)) and (("--verbose-output" in sys.argv) or ("-vo" in sys.argv)):
    compact = [i for i in sys.argv if i in ["--compact-output", "-co"]]
    verbose = [i for i in sys.argv if i in ["--verbose-output", "-vo"]]    
    sys.exit(f"Invalid arguments: " + (", ".join(compact))+ " " + ("are" if len(compact) > 1 else "is") + " incompatible with " + ", ".join(verbose))
else:
    outlevel = 1 if (("--compact-output" in sys.argv) or ("-co" in sys.argv)) else 2


if not is_valid_argument("-i"):
    while True:
        i = 0
        dirs = ["..", "."]
        for entry in os.scandir(directory):
            if entry.is_dir():
                i+=1
                dirs.append(entry.name)
        print("Input the number to select the directory (0 to cancel, 1 to go back, 2 to pick this directory):")
        for i in range(len(dirs)):
            print("("+str(i+1)+") "+dirs[i])

        dirnum = -1
        while (dirnum < 0 or dirnum > len(dirs)):
            dirnum = int(input ("The number (0-"+str(len(dirs))+"): "))

        if dirnum == 0:
            sys.exit("Cancelled")
        elif dirnum == 1:
            directory = "/"+"/".join(directory.split("/")[:-2])
        elif dirnum == 2:
            break
        else:
            directory += dirs[dirnum-1] + "/"
    directory += input("Input the prefix of file names (before track number): ")
else:
    directory = get_argument("-i")
paramstr = ""

i = 1
while os.path.isfile(directory+str(i)+".wav"):
    i+=1
if (i == 1):
    sys.exit("Detected 0 tracks, exiting")
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
    print("Track "+str(i) + "'s files written sucessfully!")
    if outlevel == 2:
        if echodet:
            paramstr +=(str(i)+": "+("Stereo; " if stereo else "Mono;   ")+("" if not echodet else "E" if echo else "-")+(" " if not echo else "Stereo; " if estereo else "Mono;   "))
        else:
            paramstr +=(str(i)+": "+("Stereo; " if stereo else "Mono;   "))
        if echosep:
            paramstr +="Main Amp: "+(str(min(max1/np.amax(w2), min1/np.amin(w2))))+"; Echo Amp: "+(str(min(max1/np.amax(w3), min1/np.amin(w3)) if echo else "")+" ")
        else:
            paramstr +="Amp: " + (str(min(max1/np.amax(w1), min1/np.amin(w1))))
    elif outlevel == 1:
        if echodet:
            paramstr +=(str(i)+": "+("S; " if stereo else "M; ")+("" if not echodet else "E" if echo else "-")+(" " if not echo else "S; " if estereo else "M; "))
        else:
            paramstr +=(str(i)+": "+("S; " if stereo else "M; "))
        if echosep:
            paramstr +=(str(min(max1/np.amax(w2), min1/np.amin(w2))))+"; "+(str(min(max1/np.amax(w3), min1/np.amin(w3)) if echo else "")+" ")
        else:
            paramstr +=(str(min(max1/np.amax(w1), min1/np.amin(w1))))
#    if stereo:
#        paramstr +=(str(np.amax((w2[:,1])-(w2[:,0]
# Stereo difference, pointless
    paramstr += "\n"
if outlevel >= 0:
    print(paramstr)


