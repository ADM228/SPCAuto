#!/bin/bash

BASEFOLDER=
DESTFOLDER=
SPCCMD_EXE=
ANALYZE_PY=

echo -e "Automation of getting SNES audio via spccmd.exe, v1.1.0\nBash script made by alexmush, 2023\n"

set -o posix

if [[ -z "$BASEFOLDER" ]] || [[ -z "$DESTFOLDER" ]] || [[ -z "$SPCCMD_EXE" ]] || [[ -z "$ANALYZE_PY" ]]; then
	OUTSTR=""
	if [[ -z "$BASEFOLDER" ]]; then OUTSTR+="Please specify the base SPC folder with the \"BASEFOLDER\" option in the audioauto_spc.sh file.\n"; fi
	if [[ -z "$DESTFOLDER" ]]; then OUTSTR+="Please specify the destination folder with the \"DESTFOLDER\" option in the audioauto_spc.sh file.\n"; fi
	if [[ -z "$SPCCMD_EXE" ]]; then OUTSTR+="Please specify the spccmd.exe path with the \"SPCCMD_EXE\" option in the audioauto_spc.sh file.\n"; fi
	if [[ -z "$ANALYZE_PY" ]]; then OUTSTR+="Please specify the analyzer.py path with the \"ANALYZE_PY\" option in the audioauto_spc.sh file.\n"; fi
	echo -e "$OUTSTR"
	exit 2
fi

if [ "$#" -eq 0 ]; then
	echo -e "Usage:\nautoaudio_spc.sh <SPC File, relative to \"$BASEFOLDER\"> [--echosep]\nThe --echosep is optional, it enables echo separation.\n"
	exit 0
fi

echo -e "You asked for $1\n"

OutFileBase="${DESTFOLDER}"
OutFileBase+=$(basename -- "${1}")
WineOutFileBase="Z:${OutFileBase}"
SPCFile="Z:${BASEFOLDER}$1.spc"

if ! [ -f "${BASEFOLDER}$1.spc" ]; then
    echo The file \"${BASEFOLDER}$1.spc\" does not exist, exiting
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
OUT_CMDB=$(wine "$SPCCMD_EXE" -cw "$SPCFile" "$WineOutFileBase.wav")
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

ECHO_SEP=0

for i in "$@" ; do [[ $i == "--echosep" ]] && ECHO_SEP=1 && break ; done

if [ $ECHO_SEP -eq 1 ]; then
	echo -n -e "Exporting separate audio with echo... "
else
	echo -n -e "Exporting separate audio..."
fi


for i in {1..8}
do
    OUT_CMDA=$(wine "$SPCCMD_EXE" -sm $i --rev); ERR_CMDA=$?
    OUT_CMDB=$(wine "$SPCCMD_EXE" -cw "$SPCFile" "${WineOutFileBase}_${i}.wav"); ERR_CMDB=$?
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

ARGS="-i ${OutFileBase}_ -np -co "

if  [ $ECHO_SEP -eq 1 ] ; then
    read -s -N 1 -p "Disable the echo and press any key" 
    echo -n -e "\nExporting separate audio without echo... "
    for i in {1..8}
    do
        OUT_CMDA=$(wine "$SPCCMD_EXE" -sm $i --rev); ERR_CMDA=$?
        OUT_CMDB=$(wine "$SPCCMD_EXE" -cw "$SPCFile" "${WineOutFileBase}_${i}e.wav"); ERR_CMDB=$?
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
    ARGS+="-es "
else
    ARGS+="-ne "
fi

echo -e "Done!\nLaunching analyze.py..."
python3 $ANALYZE_PY $ARGS 
