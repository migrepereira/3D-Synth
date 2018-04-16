import pygame.midi
import pygame.mixer
import time
import numpy as np
from scipy.io.wavfile import write
from scipy import signal

#To import into new one that controls lights and sounds
#start_time = time.time()


def playNote(note, velocity, waveType):
    frequency = 440 * (2 ** ((note - 69)/12))
    fs = 44100
    duration = 1

    vol = 1000
    
    #OLD way of making it work***************
    #t = np.arange(0,T,1/fs)
    #if waveType is "sin":
    #    x = vol * np.sin(2*np.pi*frequency*t)
    #elif waveType is "square":
    #    #x = vol * signal.square(2*np.pi*frequency*t)
    #    t = np.linspace(0, T, T * fs)
    #    x = np.square(2 * np.pi * frequency * t) * vol / 32768
    #    print(frequency)
    #elif waveType is "saw":
    #    x = vol * signal.sawtooth(2*np.pi*frequency*t)
    #x  = (x*32768).astype(np.int16)

    #New Working way.
    t = np.linspace(0, duration, duration * fs)
    if waveType is "sin":
        data = np.sin(2 * np.pi * frequency * t) * vol
    elif waveType is "square":
        data = signal.square(2 * np.pi * frequency * t) * vol
    elif waveType is "saw":
        data = signal.sawtooth(2 * np.pi * frequency * t) * vol
    x = data.astype(np.int16)

    pygame.mixer.pre_init(fs, size=-16, channels=1)
    pygame.mixer.init()
    sound = pygame.sndarray.make_sound(x)
    sound.play()
    #To import into new that controls lights and sounds
    #timeDif = time.time() - start_time
    #print (timeDif)

def readInput(input_device):

    timeStamps = []
    currentNotes = []
    notesAtThatTime = []
    timeStamps.append(0)
    notesAtThatTime.append([])

    loop = True
    while loop:
        if input_device.poll():
            event = input_device.read(1)
            midiData = event[0][0]
            note = midiData[1]
            timestamp = event[0][1]

            if(midiData[2] is 127 and note is not 120):
                currentNotes.append(note)
                timeStamps.append(timestamp)
                #notesAtThatTime.append(currentNotes)
                notesAtThatTime.append([])
                for y in currentNotes:
                    notesAtThatTime[len(notesAtThatTime)-1].append(y)
                print(notesAtThatTime[(len(notesAtThatTime)-1)])
            if(midiData[2] is 0 and note is not 120):
                currentNotes.remove(note)
                timeStamps.append(timestamp)
                #notesAtThatTime.append(currentNotes)
                notesAtThatTime.append([])
                for y in currentNotes:
                    notesAtThatTime[len(notesAtThatTime)-1].append(y)
                print(notesAtThatTime[(len(notesAtThatTime)-1)])


            #print (event)
            if(midiData[2] is 127 and note is not 120):
                playNote(note, 127, "square") #Don't change to square. change to waveType later.
            if (note is 120 and midiData[2] is 0):
                writeWAVFile(timeStamps, notesAtThatTime)
                loop = False
                input_device.close()

def noteAdd(freq, duration, vol, rate, waveType): #change to waveType later ********************************
    t = np.linspace(0, duration, duration * rate)
    if waveType is "sin":
        data = np.sin(2 * np.pi * freq * t) * vol
    elif waveType is "square":
        data = signal.square(2 * np.pi * freq * t) * vol
    elif waveType is "saw":
        data = signal.sawtooth(2 * np.pi * freq * t) * vol
    return data.astype(np.int16) # two byte integers

def writeWAVFile(timeStamps, notesAtThatTime):
    vol = 1E4
    rate = 44100
    song = noteAdd(0, 0, vol, rate, "square") #change to waveType later *****************************************
    for x in range(0, len(timeStamps)-1):
        duration = timeStamps[x+1] - timeStamps[x]
        duration = duration/1000
        silence = noteAdd(0, duration, vol, rate, "square") #silence #change to waveType later ***********************
        for i in notesAtThatTime[x]:
            freq = 440 * (2 ** ((i - 69)/12))
            addition = noteAdd(freq, duration, vol, rate, "square") #change to waveType later ***************************
            silence = silence + addition
        song = np.concatenate((song, silence), axis = 0)
        print("------\nnotes")
        print(notesAtThatTime[x])
        print("added for")
        print(duration)
        print("------")
    write('recoredSong.wav', 44100, song)


if __name__ == '__main__':
    pygame.midi.init()
    my_input = pygame.midi.Input(1)
readInput(my_input)