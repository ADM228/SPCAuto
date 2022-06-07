<h1>SPCAuto</h1>
<h2>A little program for people making oscilloscope views with SPCPlay</h2>
<h2>How to use:</h2>
<list>
<ul>Render .wav files with SPCPlay with echo enabled with syntax \<base\>\<tracknumber\>.wav, e.g. "sth1.wav", "sth2.wav".</ul>
<ul>Render .wav files with SPCPlay with echo disabled with syntax \<base\>\<tracknumber\><bold>e</bold>.wav, e.g. "sth1e.wav", "sth2e.wav".</ul>
<ul>Put the base directory where you store all oscilloscope view material into the "dir" variable.</ul>
<ul>Launch main.py and navigate the CLI.</ul>
</list>
<h2>The result:</h2>
<list>
<ul>File \<base\>\<tracknumber\>.wav with echo disabled</ul>
<ul>File \<base\>\<tracknumber\><bold>e</bold>.wav which contains only the echo</ul>
<ul>General statistics in the terminal in format \<tracknumber\> \<E if echo is non-zero (aka echo has been enabled at least once in the song), or - if it isn\'t\>\<S if the sound is stereo, or M if it is mono\>
</list>
Contact me if you didn't understand something.