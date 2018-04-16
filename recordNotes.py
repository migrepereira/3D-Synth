import pygame.midi
import pygame.mixer
import time
import numpy as np
from scipy.io.wavfile import write


#To import into new one that controls lights and sounds
#start_time = time.time()

def playNote(note):
    frequency = 440 * (2 ** ((note - 69)/12))
    fs = 8000
    T = 1
    t = np.arange(0,T,1/fs)
    x = 0.5 * np.sin(2*np.pi*frequency*t)
    x  = (x*32768).astype(np.int16)
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
                playNote(note)
            if (note is 120 and midiData[2] is 0):
                writeWAVFile(timeStamps, notesAtThatTime)
                loop = False
                input_device.close()

def noteAdd(freq, duration, amp, rate):
    t = np.linspace(0, duration, duration * rate)
    data = np.sin(2*np.pi*freq*t)*amp
    return data.astype(np.int16) # two byte integers

def writeWAVFile(timeStamps, notesAtThatTime):
    amp = 1E4
    rate = 44100
    song = noteAdd(0, 0, amp, rate)
    for x in range(0, len(timeStamps)-1):
        duration = timeStamps[x+1] - timeStamps[x]
        duration = duration/1000
        silence = noteAdd(0, duration, amp, rate) #silence
        for i in notesAtThatTime[x]:
            freq = 440 * (2 ** ((i - 69)/12))
            addition = noteAdd(freq, duration, amp, rate)
            silence = silence + addition;
        song = np.concatenate((song, silence), axis = 0)
        print("------\nnotes")
        print(notesAtThatTime[x])
        print("added for")
        print(duration)
        print("------")
    write('recoredSong.wav', 44100, song)


if __name__ == '__main__':
    pygame.midi.init()
    my_input = pygame.midi.Input(0)
    readInput(my_input)
