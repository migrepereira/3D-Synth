import pygame.midi
import pygame.mixer
import time
import numpy as np
from scipy.io.wavfile import write
from scipy import signal

##Need to change so this like loops on a short interval. Also add Kev's different WAVs
def playNote(note, velocity, mode):
    #Old method
    #frequency = 440 * (2 ** ((note - 69)/12))
    #fs = 8000
    #T = 1
    #t = np.arange(0,T,1/fs)
    #x = 0.5 * np.sin(2*np.pi*frequency*t)
    #x  = (x*32768).astype(np.int16)
    #pygame.mixer.pre_init(fs, size=-16, channels=1)
    #pygame.mixer.init()
    #sound = pygame.sndarray.make_sound(x)
    #sound.play()

    frequency = 440 * (2 ** ((note - 69)/12))
    fs = 44100
    duration = 1
    vol = 1000*(velocity/127)

    t = np.linspace(0, duration, duration * fs)
    if mode is "SIN":
        data = np.sin(2 * np.pi * frequency * t) * vol
    elif mode is "SQUARE":
        data = signal.square(2 * np.pi * frequency * t) * vol
    elif mode is "SAW":
        data = signal.sawtooth(2 * np.pi * frequency * t) * vol
    x = data.astype(np.int16)

    pygame.mixer.pre_init(fs, size=-16, channels=1)
    pygame.mixer.init()
    sound = pygame.sndarray.make_sound(x)
    sound.play()

def readInput(input_device, mode):

    timeStamps = []
    currentNotes = []
    notesAtThatTime = []
    timeStamps.append(0)
    notesAtThatTime.append([])

    currentVelocities = []
    velocitiesAtThatTime = []
    velocitiesAtThatTime.append([])

    loop = True
    while loop:
        if input_device.poll():
            event = input_device.read(1)
            midiData = event[0][0]
            note = midiData[1]

            #######THIS NEEDS TO CHANGE RIGHT NOW CANT RECORD MORE THAN ONE THING
            #Start time needs to be recorded and it needs to subtract the difference
            #Because right now the next recording wouldn't start at zero, it would start after the first one ends
            timestamp = event[0][1]

            ##KEVIN: Change the 0 in both of these input statements to what your MIDI
            ##Keyboard returns when you release a note to play yours
            if(midiData[2] is not 0 and note is not 120):

                ##Needs work obvs, probably loop to sustain or something
                playNote(note, midiData[2], mode)

                timeStamps.append(timestamp)
                currentNotes.append(note)
                notesAtThatTime.append([])
                for y in currentNotes:
                    notesAtThatTime[len(notesAtThatTime)-1].append(y)
                currentVelocities.append(midiData[2])
                velocitiesAtThatTime.append([])
                for y in currentVelocities:
                    velocitiesAtThatTime[len(velocitiesAtThatTime)-1].append(y)
                print(timestamp)
                print(notesAtThatTime[(len(notesAtThatTime)-1)])
                print(velocitiesAtThatTime[(len(velocitiesAtThatTime)-1)])
            if(midiData[2] is 0 and note is not 120):
                index = currentNotes.index(note)
                currentVelocities.remove(currentVelocities[index])
                velocitiesAtThatTime.append([])
                for y in currentVelocities:
                    velocitiesAtThatTime[len(velocitiesAtThatTime)-1].append(y)
                currentNotes.remove(note)
                timeStamps.append(timestamp)
                notesAtThatTime.append([])
                for y in currentNotes:
                    notesAtThatTime[len(notesAtThatTime)-1].append(y)
                print(timestamp)
                print(notesAtThatTime[(len(notesAtThatTime)-1)])
                print(velocitiesAtThatTime[(len(velocitiesAtThatTime)-1)])

            if (note is 120 and midiData[2] is 0):
                writeWAVFile(timeStamps, notesAtThatTime, velocitiesAtThatTime, mode)
                loop = False
                input_device.close()


def noteAdd(freq, duration, amp, rate, mode):
    t = np.linspace(0, duration, duration * rate)
    if mode is "SIN":
        data = np.sin(2 * np.pi * freq * t) * amp
    elif mode is "SQUARE":
        data = signal.square(2 * np.pi * freq * t) * amp
    elif mode is "SAW":
        data = signal.sawtooth(2 * np.pi * freq * t) * amp
    return data.astype(np.int16)

def writeWAVFile(timeStamps, notesAtThatTime, velocitiesAtThatTime, mode):

    amp = 1E4
    rate = 44100
    song = noteAdd(0, 0, amp, rate, mode)

    for x in range(0, len(timeStamps)-1):
        duration = timeStamps[x+1] - timeStamps[x]
        duration = duration/1000
        silence = noteAdd(0, duration, amp, rate, mode)
        for i in notesAtThatTime[x]:
            index = notesAtThatTime[x].index(i)
            vel = velocitiesAtThatTime[x][index]
            vel = 1000*(vel/127)
            freq = 440 * (2 ** ((i - 69)/12))
            addition = noteAdd(freq, duration, vel, rate, mode)
            silence = silence + addition;
        song = np.concatenate((song, silence), axis = 0)

        print("------\nnotes")
        print(notesAtThatTime[x])
        print("added for")
        print(duration)
        print("------")

    write('recoredSong.wav', 44100, song)
    print("recoredSong.wav was built succesfully")

##If it can't find MIDI device change 0 to a 1 in input

def recordSIN():
    pygame.midi.init()
    my_input = pygame.midi.Input(0)
    readInput(my_input, "SIN")

def recordSAW():
    pygame.midi.init()
    my_input = pygame.midi.Input(0)
    readInput(my_input, "SAW")

def recordSQUARE():
    pygame.midi.init()
    my_input = pygame.midi.Input(0)
    readInput(my_input, "SQUARE")

if __name__ == '__main__':
    pygame.midi.init()
    my_input = pygame.midi.Input(0, "SIN")
    readInput(my_input)
