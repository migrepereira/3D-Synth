README

Welcome to 3D Synth! This app was built by Cameron Cook, Michael Pereira, Kevin
Naughton and Brian Burwell in Spring 2018 as a way to showcase possibilities of
3D sounds.

What you'll need to run/use the app:

-A MIDI Input device. Any one should work! However, if you have several input
devices plugged into USBs in your computer (you're getting a device ID out of
range error), you will need to go to lines 157, 162, and 167 of recordNotes.py
and change Input(0) to Input(1), or maybe 2 or 3 depending on how many things
are plugged into your computer.

Don't have a MIDI input device? You can still see the 3d capabilities of the
program! Just put a WAV file in the directory named "recoredSong.wav" (notice,
there's a missing d), and don't click any of the record buttons when adding a
new track and you'll be able to move that track around in space when you go to
localize track.

-Python3. Along with a lot of libraries, all of which can be installed with
"pip3 install <library name>" in terminal. The libraries you will need to have
installed with this method include:
############## LIBRARIES NEEDED TO DOWNLOAD
Another package you will need to have installed is ffmpeg. If you're on a mac
and using homebrew, this can easily be installed with "brew install ffmpeg".
If you aren't, here are instillation instructions:
https://github.com/adaptlearning/adapt_authoring/wiki/Installing-FFmpeg
This is just used when exporting the track out to an MP3. If you don't have it,
the final song will be "mySong.wav" in the directory

-Headphones are encouraged to experience the 3D capabilities of the app

To use the app:
There are 2 ways to start the app:

If you are on a mac, and the main 3D-Synth directory is on your desktop, just
open the application we made! (Note, you may have to go to your system
preferences and change your security preferences because I'm not a "trusted
developer")

If not, navigate to the 3D-Synth directory in the terminal and run "python3
Sliders.py"

############# INSTRUCTIONS ON ALL BUTTONS






Common errors:

Every once in a while, memory allocation errors happen and it crashes. Just
restart the program, your progress will be saved.
If you're getting the "rainbow wheel of death" while recording, that's ok, the
program is doing a lot to render the sound live while it also writes a WAV file.
It should go away when you stop recording.
Missing modules means a library wasn't properly installed.
Most errors should go away if you just restart the program
