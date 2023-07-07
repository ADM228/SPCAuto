<h1>SPCAuto suite</h1>
<h2>A little suite for people making oscilloscope views</h2>
<h3>How to use SPCAuto:</h3>
<list>
<ul>Render .wav files with echo enabled with syntax [base]\_[tracknumber].wav, e.g. "smth\_1.wav", "smth\_2.wav".</ul>
<ul>If you want to separate echo from the music, render .wav files with echo disabled with syntax [base]\_[tracknumber]<bold>e</bold>.wav, e.g. "smth\_1e.wav", "smth\_2e.wav".</ul>
<ul>Put the base directory where you store all oscilloscope view material into the "dir" variable.</ul>
<ul>Launch main.py and navigate the CLI.</ul>
</list>
<h3>The result:</h3>
<list>
<ul>File [base]\_[tracknumber].wav with echo disabled</ul>
<ul>File [base]\_[tracknumber]<bold>e</bold>.wav which contains only the echo if you choose to do so</ul>
<ul>General statistics in the terminal in format [tracknumber]: ['Stereo' if the sound is stereo, or 'Mono  ' if it is mono]; [E if echo is non-zero (aka echo has been enabled at least once in the song), or - if it is not]; ['Stereo' if the echo is stereo, or 'Mono  ' if it is mono]; Amp: [maximum possible amplification for this track], ["EchoAmp: " and maximum possible echo amplification if echo exists]</ul>
</list>
<h3>GetAudioAuto shell script</h3>
<p>Uses spccmd.exe to get to SPCPlay to automatically fetch audio from it.</p>
<p>Before using make sure to set BASEFOLDER to the base directory where the spc action is happening, SPCCMD_EXE to the location of spccmd.exe that comes along with SPCPlay, and SPCAUTO to the location of main.py of this suite</p>
<p>Usage: bash getaudioauto.sh [path to SPC file without .spc relative to BASEFOLDER]</p>
<p>It will automatically get audio from channels, you only need to enable and disable echo manually through the SPCPlay GUI.</p>
<h3>How to use wvcenter:</h3>
<s><list>
<ul>Render the .wav file (which has the wave off-center, for example gbsplay's output of the wave channel)</ul>
<ul>Launch wvcenter.py and navigate the CLI.</ul>
</list>
<h3>The result:</h3>
<list>
<ul>The .wav file that replaced the original but with the wave (mostly) centered</ul></s>
<h3>Don\'t, find some Audacity DC offset tools, they are way faster </h3> 
</list>
Contact me if you didn't understand something.
