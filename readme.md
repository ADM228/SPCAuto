<h1>SPCAuto suite</h1>
<h2>A little suite for people making oscilloscope views</h2>
<h3>How to use SPCAuto:</h3>
<list>
<ul>Render .wav files with echo enabled with syntax [base][tracknumber].wav, e.g. "sth1.wav", "sth2.wav".</ul>
<ul>If you want to separate echo from the music, render .wav files with echo disabled with syntax [base][tracknumber]<bold>e</bold>.wav, e.g. "sth1e.wav", "sth2e.wav".</ul>
<ul>Put the base directory where you store all oscilloscope view material into the "dir" variable.</ul>
<ul>Launch main.py and navigate the CLI.</ul>
</list>
<h3>The result:</h3>
<list>
<ul>File [base][tracknumber].wav with echo disabled</ul>
<ul>File [base][tracknumber]<bold>e</bold>.wav which contains only the echo if you choose to do so</ul>
<ul>General statistics in the terminal in format [tracknumber]: [E if echo is non-zero (aka echo has been enabled at least once in the song), or - if it is not][S if the sound is stereo, or M if it is mono]</ul>
</list>
<h3>How to use wvcenter:</h3>
<list>
<ul>Render the .wav file (which has the wave off-center, for example gbsplay's output of the wave channel)</ul>
<ul>Launch wvcenter.py and navigate the CLI.</ul>
</list>
<h3>The result:</h3>
<list>
<ul>The .wav file that replaced the original but with the wave (mostly) centered</ul>
</list>
Contact me if you didn't understand something.
