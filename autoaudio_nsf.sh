#!/bin/bash

BASEFOLDER=
DESTFOLDER=
NSF2WAV=

echo -e "Automation of getting NES audio via modified nsf2wav, v1.1.0\nBash script made by alexmush, 2023\n"

set -o posix

if [[ -z "$BASEFOLDER" ]] || [[ -z "$DESTFOLDER" ]] || [[ -z "$NSF2WAV" ]]; then
	OUTSTR=""
	if [[ -z "$BASEFOLDER" ]]; then OUTSTR+="Please specify the base NSF folder with the \"BASEFOLDER\" option in the audioauto_nsf.sh file.\n"; fi
	if [[ -z "$DESTFOLDER" ]]; then OUTSTR+="Please specify the destination folder with the \"DESTFOLDER\" option in the audioauto_nsf.sh file.\n"; fi
	if [[ -z "$NSF2WAV" ]]; then OUTSTR+="Please specify the nsf2wav executable path with the \"NSF2WAV\" option in the audioauto_nsf.sh file.\n"; fi
	echo -e "$OUTSTR"
	exit 2
fi

if [ "$#" -eq 0 ]; then
	echo -e "Usage:\nautoaudio_nsf.sh <NSF filename, or directory of NSF files, relative to \"$BASEFOLDER\"> <Track Number, starting with 1> [<Audio length, will detect looping if not present>] [Expansion args]\nPossible expansion arguments:\n --fds\n --mmc5\n --s5b\n --vrc6 \n --vrc7\n --n163\n --opll\n"
	exit 0
fi

echo -e "You asked for $1, track number $2"

if ! [[ $2 =~ ^[0-9]+$ ]]; then
	echo Invalid track number: $2
	exit 2
fi

if ! [[ $3 =~ ^[0-9]+$ ]]; then
	echo \"$3\" does not seem to specify the output duration, doing the default...
	DURATION=""
else
	echo Duration specified - $3ms
	DURATION="--length_ms=$3 --length_force"
fi

IFS=$'\x0A'
files=( $(find ${BASEFOLDER}/${1} -type f -name "*.nsf" ) $(find${BASEFOLDER} -type f -name "${1}/*.nsfe" ) )
unset IFS

if [ ${#files[@]} -eq 0 ]; then
	echo No files found, exiting
	exit 1
fi

if ! [ ${#files[@]} -eq 1 ]; then

	echo "(0) Cancel"

	for i in $(seq 0 ${#files[@]}); do
		if ! [ "${files[${i}]}" == "" ]; then
			echo "($(expr ${i} + 1)) ${files[${i}]}"
		else 
			unset files[${i}]
		fi
	done

	NUM=-1

	while ! [ \( $NUM -eq $NUM 2>/dev/null \) -a \( "${NUM}" -ge 0 \) -a \( "${NUM}" -le ${#files[@]} \) ]; do
		read -p "Choose the file: " NUM
	done 

	NSFFILE=${files[$(expr $NUM - 1)]}

else
	NSFFILE=${files[0]}
fi

BASE=$(basename -- "$NSFFILE")
NSFE=0
if [ "${filename##*.}" == "nsfe" ]; then
	NSFE=1
fi

echo $NSFFILE

FILEBASE="${DESTFOLDER}/${2}"

ARGS="--c=1 --track=$2 --s=96000 --quiet ${DURATION}"
MASK_ARGS="--mask_reverse --mute"

echo -n -e "\nExporting master audio... "

OUT_CMD=$($NSF2WAV ${ARGS} "${NSFFILE}" $FILEBASE.wav)
ERR_CMD=$?

if ! [ $ERR_CMD -eq 0 ]; then
    echo "Couldn't for whatever reason; logs:"
    echo $OUT_CMD
	exit $ERR_CMD
else
    echo "Done! "
fi

echo -n -e "Exporting NES APU audio... "

for i in {0..4}
do
    OUT_CMD=$($NSF2WAV ${ARGS} --mask=${i} ${MASK_ARGS} "${NSFFILE}" ${FILEBASE}_${i}.wav)
	ERR_CMD=$?
    if ! [ $ERR_CMD -eq 0 ]; then
        echo -e "\nFailed on track ${i}, logs:"
        echo $OUT_CMD
		exit $ERR_CMD
    else
        echo -n "${i} "
    fi
done
OUT_CMD=$($NSF2WAV --trigger ${ARGS} --mask=2 ${MASK_ARGS} "${NSFFILE}" ${FILEBASE}_2T.wav)
ERR_CMD=$?
if ! [ $ERR_CMD -eq 0 ]; then
    echo -e "\nFailed on track 2T, logs:"
    echo $OUT_CMD
	exit $ERR_CMD
else
    echo -n "2T "
fi

echo -e "Done!"

FDS=0
MMC5=0
S5B=0
VRC6=0
VRC7=0
N163=0
OPLL=0

for i in "$@" ; do [[ $i == "--fds" ]] && FDS=1 && break ; done
for i in "$@" ; do [[ $i == "--mmc5" ]] && MMC5=1 && break ; done
for i in "$@" ; do [[ $i == "--s5b" ]] && S5B=1 && break ; done
for i in "$@" ; do [[ $i == "--vrc6" ]] && VRC6=1 && break ; done
for i in "$@" ; do [[ $i == "--vrc7" ]] && VRC7=1 && break ; done
for i in "$@" ; do [[ $i == "--n163" ]] && N163=1 && break ; done
for i in "$@" ; do [[ $i == "--opll" ]] && VRC7=1 && OPLL=1 && break ; done

if  [ $FDS -eq 1 ] ; then
	echo -n -e "Exporting FDS audio... "
	OUT_CMD=$($NSF2WAV ${ARGS} --mask=5 ${MASK_ARGS} "${NSFFILE}" ${FILEBASE}_5.wav)
	ERR_CMD=$?
    if ! [ $ERR_CMD -eq 0 ]; then
		echo -e "\nFailed on track 5, logs:"
		echo $OUT_CMD
		exit $ERR_CMD
	else
		echo -n "5 "
	fi

	OUT_CMD=$($NSF2WAV --trigger ${ARGS} --mask=5 ${MASK_ARGS} "${NSFFILE}" ${FILEBASE}_5T.wav)
	ERR_CMD=$?
    if ! [ $ERR_CMD -eq 0 ]; then
		echo -e "\nFailed on track 5, logs:"
		echo $OUT_CMD
		exit $ERR_CMD
	else
		echo -n "5T "
	fi

	echo -e "Done!"
fi

if [ $MMC5 -eq 1 ] ; then
	echo -n -e "Exporting MMC5 audio... "
	for i in {6..8}
	do
		OUT_CMD=$($NSF2WAV ${ARGS} --mask=${i} ${MASK_ARGS} "${NSFFILE}" ${FILEBASE}_${i}.wav)
		ERR_CMD=$?
    	if ! [ $ERR_CMD -eq 0 ]; then
		    echo -e "\nFailed on track ${i}, logs:"
		    echo $OUT_CMD
			exit $ERR_CMD
		else
		    echo -n "${i} "
		fi
	done
	echo -e "Done!"
fi


if [ $S5B -eq 1 ] ; then
	echo -n -e "Exporting S5B audio... "
	for i in {9..11}
	do
		OUT_CMD=$($NSF2WAV ${ARGS} --mask=${i} ${MASK_ARGS} "${NSFFILE}" ${FILEBASE}_${i}.wav)
		ERR_CMD=$?
    	if ! [ $ERR_CMD -eq 0 ]; then
		    echo -e "\nFailed on track ${i}, logs:"
		    echo $OUT_CMD
			exit $ERR_CMD
		else
		    echo -n "${i} "
		fi
	done
	echo -e "Done!"
fi

if [ $VRC6 -eq 1 ] ; then
	echo -n -e "Exporting VRC6 audio... "
	for i in {12..14}
	do
		OUT_CMD=$($NSF2WAV ${ARGS} --mask=${i} ${MASK_ARGS} "${NSFFILE}" ${FILEBASE}_${i}.wav)
		ERR_CMD=$?
    	if ! [ $ERR_CMD -eq 0 ]; then
		    echo -e "\nFailed on track ${i}, logs:"
		    echo $OUT_CMD
			exit $ERR_CMD
		else
		    echo -n "${i} "
		fi
	done
	echo -e "Done!"
fi

if [ $VRC7 -eq 1 ] ; then
	echo -n -e "Exporting VRC7 audio... "
	for i in {15..20}
	do
		OUT_CMD=$($NSF2WAV ${ARGS} --mask=${i} ${MASK_ARGS} "${NSFFILE}" ${FILEBASE}_${i}.wav)
		ERR_CMD=$?
    	if ! [ $ERR_CMD -eq 0 ]; then
		    echo -e "\nFailed on track ${i}, logs:"
		    echo $OUT_CMD
			exit $ERR_CMD
		else
		    echo -n "${i} "
		fi
	done
	echo -e "Done!"
fi


if [ $N163 -eq 1 ] ; then
	echo -n -e "Exporting N163 audio... "
	for i in {21..28}
	do
		OUT_CMD=$($NSF2WAV ${ARGS} --mask=${i} ${MASK_ARGS} "${NSFFILE}" ${FILEBASE}_${i}.wav)
		ERR_CMD=$?
    	if ! [ $ERR_CMD -eq 0 ]; then
		    echo -e "\nFailed on track ${i}, logs:"
		    echo $OUT_CMD
			exit $ERR_CMD
		else
		    echo -n "${i} "
		fi

		OUT_CMD=$($NSF2WAV --trigger ${ARGS} --mask=${i} ${MASK_ARGS} "${NSFFILE}" ${FILEBASE}_${i}T.wav)
		ERR_CMD=$?
    	if ! [ $ERR_CMD -eq 0 ]; then
		    echo -e "\nFailed on track ${i}, logs:"
		    echo $OUT_CMD
			exit $ERR_CMD
		else
		    echo -n "${i}T "
		fi
	done
	echo -e "Done!"
fi

if [ $VRC6 -eq 1 ] ; then
	echo -n -e "Exporting YM2413 audio... "
	for i in {29..31}
	do
		echo $NSF2WAV ${ARGS} --mask=${i} ${MASK_ARGS} "${NSFFILE}" ${FILEBASE}_${i}.wav
		OUT_CMD=$($NSF2WAV ${ARGS} --mask=${i} ${MASK_ARGS} "${NSFFILE}" ${FILEBASE}_${i}.wav)
		ERR_CMD=$?
    	if ! [ $ERR_CMD -eq 0 ]; then
		    echo -e "\nFailed on track ${i}, logs:"
		    echo $OUT_CMD
			exit $ERR_CMD
		else
		    echo -n "${i} "
		fi
	done
	echo -e "Done!"
fi

cd ${DESTFOLDER}
