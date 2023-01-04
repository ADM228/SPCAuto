<h1>SPCAuto suite</h1>
<h2>A little suite for people making oscilloscope views</h2>
<h3>How to use SPCAuto:</h3>
<list>
<ul>Render .wav files with echo enabled with syntax [base]_[tracknumber].wav, e.g. "smth_1.wav", "smth_2.wav".</ul>
<ul>If you want to separate echo from the music, render .wav files with echo disabled with syntax [base]_[tracknumber]<bold>e</bold>.wav, e.g. "smth_1e.wav", "smth_2e.wav".</ul>
<ul>Put the base directory where you store all oscilloscope view material into the "dir" variable.</ul>
<ul>Launch main.py and navigate the CLI.</ul>
</list>
<h3>The result:</h3>
<list>
<ul>File [base]_[tracknumber].wav with echo disabled</ul>
<ul>File [base]_[tracknumber]<bold>e</bold>.wav which contains only the echo if you choose to do so</ul>
<ul>General statistics in the terminal in format [tracknumber]: ['Stereo' if the sound is stereo, or 'Mono  ' if it is mono]; [E if echo is non-zero (aka echo has been enabled at least once in the song), or - if it is not]; ['Stereo' if the echo is stereo, or 'Mono  ' if it is mono]; Amp: [maximum possible amplification for this track], ["EchoAmp: " and maximum possible echo amplification if echo exists]</ul>
</list>
<h3>How to use wvcenter:</h3>
<s><list>
<ul>Render the .wav file (which has the wave off-center, for example gbsplay's output of the wave channel)</ul>
<ul>Launch wvcenter.py and navigate the CLI.</ul>
</list>
<h3>The result:</h3>
<list>
<ul>The .wav file that replaced the original but with the wave (mostly) centered</ul></s>
<h3>Don't, find some Audacity DC offset tools, they are way faster </h3> 
</list>
Contact me if you didn't understand something.
