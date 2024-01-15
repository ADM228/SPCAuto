# SPCAuto suite - A bunch of software for people making oscilloscope views


## Automatic audio bash scripts

These scripts are to be either self-run (`./autoaudio_XXX.sh`) or run with `bash` or `sh`. You need to configure paths beforehand.

### SPC

autoaudio_spc.sh gets audio from SPCPlay via spc_cmd.exe, an official CLI for SPCPlay bundled with it. It has the ability to get audio with and without the echo, albeit that requires human interaction. It automatically exports audio into the format analyze.py accepts and sends the audio to it afterwards.

#### Usage

`autoaudio_spc.sh <SPC File, relative to $BASEFOLDER> [--echosep]`  
The `--echosep` is optional, it enables echo separation (requires human interaction to turn on/off the echo).

### NSF

autoaudio_nsf.sh gets audio from the NSFPlay emulation core via nsf2wav. A specific version of nsf2wav is needed, specifically in [my fork](https://github.com/ADM228/nsfplay) (it's in the contrib folder). It automatically exports trigger waves for NES Triangle, FDS (untested) and N163 (untested). It also features a directory explorer to find NSF files easily.

#### Usage

`autoaudio_nsf.sh <NSF filename, or directory of NSF files, relative to $BASEFOLDER> <Track Number, starting with 1> [<Audio length, will detect looping if not present>] [Expansion args]`  
Possible expansion arguments: `--fds`, `--mmc5` ,`--s5b`, `--vrc6`, `--vrc7`, `--n163`, `--opll`.

### GBS

autoaudio_gbs.sh gets audio from gbsplay and converts it to wav files using ffmpeg. It just uses the standard version of gbsplay. It features a listening mode that straight up launches gbsplay with the specified GBS file. It also features a directory explorer to find GBS files easily.

#### Usage

`autoaudio_gbs.sh <GBS filename, or directory of GBS files, relative to $BASEFOLDER> [<Track Number, starting with 1>] [<Audio length, will detect looping if not present>]`  
If no track number is specified, this script will be put into listening mode.

### Planned Features

- Using config files
  
## analyze.py

### Features

- Analyzes the maximum amplification that can be used per track
- Determines if there are any differences between left and right signals
- Optionally separates echo ((track with echo) - (track without echo) = echo)

### Command-line options

- `-ed` aka `--echodet`: Detect echo, its amount and stereo/mono, but don't separate it.
- `-es` aka `--echosep`: Detect echo and its above characteristics, and separate it from the un-echo parts.
- `-ne` aka `--no-echo`: Do nothing echo-related.
- `-np` aka `--no-pad`: Don't pad the tracks.
- `-p`  aka `--pad`: Do pad the tracks with emptiness (duration inputted manually).
- `-vo` aka `--verbose-output`: Output the collected data verbosely.
- `-co` aka `--compact-output`: Output the collected data compactly.
- Not having either of the 2 options above will not output anything.
- `-i <filename base>`: The input filename base, without the track number.

### Usage

- Render .wav files with echo enabled with syntax [base][tracknumber].wav, e.g. "smth_1.wav", "smth_2.wav".
- If you want to separate echo from the music, render .wav files with echo disabled with syntax [base][tracknumber]**e**.wav, e.g. "smth_1e.wav", "smth_2e.wav".
- Put the base directory where you store all oscilloscope view material into the "directory" variable, by default it's set to the root directory but that is not useful outside of Linux.
- Launch main.py and navigate the CLI, or launch it with the aforementioned command-line options to automate it.

### Output

- Files [base][tracknumber].wav with no echo
- If echo separation was enabled, files [base][tracknumber]**e**.wav which only contain the echo 
- General statistics in the terminal in format [tracknumber]: ['Stereo' if the sound is stereo, or 'Mono  ' if it is mono]; [E if echo is non-zero (aka echo has been enabled at least once in the song), or - if it is not]; ['Stereo' if the echo is stereo, or 'Mono  ' if it is mono]; Amp: [maximum possible amplification for this track], ["EchoAmp: " and maximum possible echo amplification if echo exists]

### Planned Features

- Specifying the suffixes
- Using config files

# The end

Contact me if you didn't understand something.
