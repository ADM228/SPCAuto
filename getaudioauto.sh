#!/bin/bash

BASEFOLDER=
SPCCMD_EXE=
SPCAUTO=

echo -e "Automation of getting SNES audio via spccmd.exe\nVersion 1.0\nScript made by alexmush, 2023\n\n"
echo -e "You asked for $1"

FileBase="Z:$BASEFOLDER$1"
SPCFile="$FileBase.spc"

if ! [ -f "$BASEFOLDER$1.spc" ]; then
    echo The file \"$BASEFOLDER$1.spc\" does not exist, exiting
    exit 1
fi

wine "$SPCCMD_EXE" -s >/dev/null
if [ $? -eq 101 ]; then
    echo SPCPlay is currently not running
    exit 101
fi

read -s -N 1 -p "Ensure that echo is enabled right now, and press any key" 

echo -n -e "\nExporting master audio... "

OUT_CMDA=$(wine "$SPCCMD_EXE" -sm 0)
ERR_CMDA=$?
OUT_CMDB=$(wine "$SPCCMD_EXE" -cw "$SPCFile" "$FileBase.wav")
ERR_CMDB=$?

if ! [ $ERR_CMDB -eq 0 ] || ! [ $ERR_CMDA -eq 0 ]; then
    echo "Couldn't for whatever reason; logs:"
    echo $OUT_CMDA
    echo $OUT_CMDB
    if ! [ $ERR_CMDA -eq 0 ]; then
        exit $ERR_CMDA
    else
        exit $ERR_CMDB
    fi
else
    echo "Done! "
fi

echo -n -e "Exporting separate audio with echo... "

for i in {1..8}
do
    OUT_CMDA=$(wine "$SPCCMD_EXE" -sm $i --rev); ERR_CMDA=$?
    OUT_CMDB=$(wine "$SPCCMD_EXE" -cw "$SPCFile" "${FileBase}_${i}.wav"); ERR_CMDB=$?
    if ! [ $ERR_CMDB -eq 0 ] || ! [ $ERR_CMDA -eq 0 ]; then
        echo -e "\nFailed on track ${i}, logs:"
        echo $OUT_CMDA
        echo $OUT_CMDB
        if ! [ $ERR_CMDA -eq 0 ]; then
            exit $ERR_CMDA
        else
            exit $ERR_CMDB
        fi
    else
        echo -n "${i} "
    fi
done
echo -e "Done!\n"



read -s -N 1 -p "Disable the echo and press any key" 
echo -n -e "\nExporting separate audio without echo... "
for i in {1..8}
do
    OUT_CMDA=$(wine "$SPCCMD_EXE" -sm $i --rev); ERR_CMDA=$?
    OUT_CMDB=$(wine "$SPCCMD_EXE" -cw "$SPCFile" "${FileBase}_${i}e.wav"); ERR_CMDB=$?
    if ! [ $ERR_CMDB -eq 0 ] || ! [ $ERR_CMDA -eq 0 ]; then
        echo -e "\nFailed on track ${i}, logs:"
        echo $OUT_CMDA
        echo $OUT_CMDB
        if ! [ $ERR_CMDA -eq 0 ]; then
            exit $ERR_CMDA
        else
            exit $ERR_CMDB
        fi
    else
        echo -n "${i} "
    fi
done
echo -e "Done!\nLaunching SPCAuto..."
python3 $SPCAUTO <(echo -e -n "y\ny\nn\n") 
