# 3D-Synth
This is a Python application where you can record sound through a MIDI keyboard, localize those sounds in 3D space, and then export them as a 3D song in the form of a .wav file.

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
image
numpy
pandas
pydub
pygame
scipy
tkinter

Another package you will need to have installed is ffmpeg. If you're on a mac
and using homebrew, this can easily be installed with "brew install ffmpeg".
If you aren't, here are installation instructions:
https://github.com/adaptlearning/adapt_authoring/wiki/Installing-FFmpeg.
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

Once you have the app running:

Currently, there are no tracks in your song. The first thing to do is to add a new track (Click on "Add track to current song").

On the new track menu, select which waveform you want to use (SIN, SQUARE, or SAW) and begin playing your track on the input hardware. Once you're done recording, end the recording by pressing the highest note on the keyboard. (Note, this currently has to manually be adjusted at several points in recordNotes.py for different keyboards, pretty much every 120 (the highest note) needs to be changed to whatever the MIDI input of the highest key of that input is) You can click "Playback track" to hear what you recorded. Now that the track is recorded, it's time to put it in 3D space. From the menu, click "Localize Track", which will bring you to a new menu.

On this menu, you can click and drag on each of the three sliders to indicate where in space you want the track to appear (+X will appear on your right, +Y will appear above you, +Z will appear in front of you). You can test how it sounds before you commit this location by clicking "Play". Once you're satisfied with the sound of the track, click "Done" to add it to your song.

To confirm your changes, click "Add track to song". Once you commit these changes, the track cannot be removed.

From the main menu you can now "Start a new song" (which clears all of your recorded tracks), "Play current song" (which is all of your recorded tracks layered on top of each other), add another track ("Add track to current song"), or finish your song and export it as 'mySong.mp3'. Your track will save in the same directory as '3D-Synth' (So the desktop if that folder is in the desktop).


Common errors:

Every once in a while, memory allocation errors happen and it crashes. Just
restart the program, your progress will be saved.

If you're getting the "rainbow wheel of death" while recording, that's ok, the
program is doing a lot to render the sound live while it also writes a WAV file.
It should go away when you stop recording.

Missing modules means a library wasn't properly installed.

Most errors should go away if you just restart the program

If it says value not in list during recording just restart program
