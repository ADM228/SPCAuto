# SPCAuto suite - A bunch of software for people making oscilloscope views

## analyze.py:

### Features

- Analyzes the maximum amplification that can be used per track
- Determines if there are any differences between left and right signals
- Optionally separates echo ((track with echo) - (track without echo) = echo)

### Command-line options:

- `-ed` aka `--echodet`: Detect echo, its amount and stereo/mono, but don't separate it.
- `-es` aka `--echosep`: Detect echo and its above characteristics, and separate it from the un-echo parts.
- `-ne` aka `--no-echo`: Do nothing echo-related.
- `-np` aka `--no-pad`: Don't pad the tracks.
- `-p`  aka `--pad`: Do pad the tracks with emptiness (duration inputted manually).
- `-vo` aka `--verbose-output`: Output the collected data verbosely.
- `-co` aka `--compact-output`: Output the collected data compactly.
- Not having either of the 2 options above will not output anything.
- `-i <filename base>`: The input filename base, without the track number.

### Usage:

- Render .wav files with echo enabled with syntax [base][tracknumber].wav, e.g. "smth_1.wav", "smth_2.wav".
- If you want to separate echo from the music, render .wav files with echo disabled with syntax [base][tracknumber]**e**.wav, e.g. "smth_1e.wav", "smth_2e.wav".
- Put the base directory where you store all oscilloscope view material into the "directory" variable, by default it's set to the root directory but that is not useful outside of Linux.
- Launch main.py and navigate the CLI, or launch it with the aforementioned command-line options to automate it.

### Output:

- Files [base][tracknumber].wav with no echo
- If echo separation was enabled, files [base][tracknumber]**e**.wav which only contain the echo 
- General statistics in the terminal in format [tracknumber]: ['Stereo' if the sound is stereo, or 'Mono  ' if it is mono]; [E if echo is non-zero (aka echo has been enabled at least once in the song), or - if it is not]; ['Stereo' if the echo is stereo, or 'Mono  ' if it is mono]; Amp: [maximum possible amplification for this track], ["EchoAmp: " and maximum possible echo amplification if echo exists]

### Planned Features:

- Specifying the suffixes
- Using config files

## Automatic audio shell scripts

Automatically get audio from SPCPlay (via spccmd.exe), NSFPlay (or specifically nsf2wav), and gbsplay.
SPCPlay then sends the audio to analyze.py.

### Usage:

Either self-execute the scripts (`./autoaudio_XXX.sh`) or use `bash` or `sh` to run them.

### Planned Features:

- Using config files

# The end.

Contact me if you didn't understand something.
