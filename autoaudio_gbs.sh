#!/bin/bash

BASEFOLDER=
DESTFOLDER=
DEFAULT_DURATION=
GBSPLAY=
FFMPEG=

echo -e "Automation of getting GB audio via gbsplay v1.1.0\nBash script made by alexmush, 2022-2023\n\n"

set -o posix

if [[ -z "$BASEFOLDER" ]] || [[ -z "$DESTFOLDER" ]] || [[ -z "$DEFAULT_DURATION" ]] || [[ -z "$GBSPLAY" ]] || [[ -z "$FFMPEG" ]]; then
	OUTSTR=""
	if [[ -z "$BASEFOLDER" ]]; then OUTSTR+="Please specify the base GBS folder with the \"BASEFOLDER\" option in the audioauto_gbs.sh file.\n"; fi
	if [[ -z "$DESTFOLDER" ]]; then OUTSTR+="Please specify the destination folder with the \"DESTFOLDER\" option in the audioauto_gbs.sh file.\n"; fi
	if [[ -z "$DEFAULT_DURATION" ]]; then OUTSTR+="Please specify the default playback duration with the \"DEFAULT_DURATION\" option in the audioauto_gbs.sh file.\n"; fi
	if [[ -z "$GBSPLAY" ]]; then OUTSTR+="Please specify the gbsplay executable path with the \"GBSPLAY\" option in the audioauto_gbs.sh file.\n"; fi
	if [[ -z "$FFMPEG" ]]; then OUTSTR+="Please specify the ffmpeg executable path with the \"FFMPEG\" option in the audioauto_gbs.sh file.\n"; fi
	echo -e "$OUTSTR"
	exit 2
fi

if [ "$#" -eq 0 ]; then
	echo -e "Usage:\nautoaudio_gbs.sh <GBS filename, or directory of GBS files, relative to \"$BASEFOLDER\"> [<Track Number, starting with 1>] [<Audio length, will detect looping if not present>]\nIf no track number is specified, this script will be put into listening mode.\n"
	exit 0
fi

echo -e "You asked for $1, track number $2"

if ! [[ $2 =~ ^[0-9]+$ ]]; then
	echo Invalid track number: $2, putting into listening mode instead
	LISTENING=1
fi


if ! [[ $3 =~ ^[0-9]+$ ]]; then
	echo \"$3\" does not seem to specify the output duration, doing the default ${DEFAULT_DURATION}s...
	DURATION=$DEFAULT_DURATION
else
	echo Duration specified - $3s
	DURATION=$3
fi

IFS=$'\x0A'
files=( $(find ${BASEFOLDER}/${1} -type f -name "*.gbs" ) )
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

	GBSFILE=${files[$(expr $NUM - 1)]}
else
	GBSFILE=${files[0]}
fi

BASE=$(basename -- "$GBSFILE")

echo $GBSFILE

FILEBASE="${DESTFOLDER}/${2}"


if [[ $LISTENING -eq 0 ]]; then
	GBSPLAY+=" -T ${DURATION}"
	GBSPLAY_ARGS="-L -o stdout -E l -r 96000"
	FFMPEG_ARGS="-v 16 -ac 2 -t ${DURATION} -f s16le -ar 96000 -i - -c:a pcm_s16le"

	printf "Starting up recording...\n"
	printf "0/5 [-----] \033[1G"
	${GBSPLAY} ${GBSPLAY_ARGS} "$GBSFILE" $2 $2 | $($FFMPEG ${FFMPEG_ARGS} ${FILEBASE}.wav)
	printf "1/5 [+----] \033[1G" 
	${GBSPLAY} -2 -3 -4 ${GBSPLAY_ARGS} "$GBSFILE" $2 $2 | $($FFMPEG ${FFMPEG_ARGS} ${FILEBASE}_1.wav)
	printf "2/5 [++---] \033[1G"
	${GBSPLAY} -1 -3 -4 ${GBSPLAY_ARGS} "$GBSFILE" $2 $2 | $($FFMPEG ${FFMPEG_ARGS} ${FILEBASE}_2.wav)
	printf "3/5 [+++--] \033[1G"
	${GBSPLAY} -1 -2 -4 ${GBSPLAY_ARGS} "$GBSFILE" $2 $2 | $($FFMPEG ${FFMPEG_ARGS} ${FILEBASE}_3.wav)
	printf "4/5 [++++-] \033[1G"
	${GBSPLAY} -1 -2 -3 ${GBSPLAY_ARGS} "$GBSFILE" $2 $2 | $($FFMPEG ${FFMPEG_ARGS} ${FILEBASE}_4.wav)
	printf "5/5 [+++++] \nDone!\n"
else
	${GBSPLAY} -r 96000 "$GBSFILE"
fi

stty sane
