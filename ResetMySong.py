#Cameron Cook

import pygame.midi
import pygame.mixer
import time
import numpy as np
from scipy.io.wavfile import write
from scipy import signal
from pydub import AudioSegment
import wave
import contextlib

def noteAdd(freq, duration, amp, rate):
    t = np.linspace(0, duration, duration * rate)
    data = np.sin(2 * np.pi * freq * t) * amp
    return data.astype(np.int16)

def resetSong():
    silence = noteAdd(0, 1, 1000, 44100)
    write('mySong.wav', 44100, silence)
    print("mySong was reset")

def exportSong():
    AudioSegment.from_wav("mySong.wav").export("../mySong.mp3", format="mp3")
    print("Export succesful! mySong.mp3 is now ready to listen to in the same directory as 3D-Synth")
