# SPCAuto suite - A bunch of software for people making oscilloscope views
## analyze.py:
### Features
- Analyzes the maximum amplification that can be used per track
- Determines if there are any differences between left and right signals
- Optionally separates echo ((track with echo) - (track without echo) = echo)
### Usage:
- Render .wav files with echo enabled with syntax [base][tracknumber].wav, e.g. "smth_1.wav", "smth_2.wav".
- If you want to separate echo from the music, render .wav files with echo disabled with syntax [base][tracknumber]**e**.wav, e.g. "smth_1e.wav", "smth_2e.wav".
- Put the base directory where you store all oscilloscope view material into the "dir" variable.
- Launch main.py and navigate the CLI.
### Output:
- Files [base][tracknumber].wav with no echo
- If echo separation was enabled, files [base][tracknumber]**e**.wav which only contain the echo 
- General statistics in the terminal in format [tracknumber]: ['Stereo' if the sound is stereo, or 'Mono  ' if it is mono]; [E if echo is non-zero (aka echo has been enabled at least once in the song), or - if it is not]; ['Stereo' if the echo is stereo, or 'Mono  ' if it is mono]; Amp: [maximum possible amplification for this track], ["EchoAmp: " and maximum possible echo amplification if echo exists]
### Planned Features:
- Specifying the suffixes/prefixes
- Using command line arguments
- Using config files
## GetAudioAuto shell script
Uses spccmd.exe to get to SPCPlay to automatically fetch audio from it.
### Usage:
Before using make sure to set BASEFOLDER to the base directory where the spc action is happening, SPCCMD_EXE to the location of spccmd.exe that comes along with SPCPlay, and ANALYZER to the location of main.py of this suite
Run ```bash getaudioauto.sh``` [path to SPC file without .spc relative to BASEFOLDER]
It will automatically get audio from channels, you only need to enable and disable echo manually through the SPCPlay GUI, and then it will automatically launch analyze.py.
### Planned Features:
- Using config files
# End.
Contact me if you didn't understand something.
