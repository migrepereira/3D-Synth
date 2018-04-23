import numpy as np
import scipy as sp
import scipy.io as spio
import scipy.io.wavfile as radio
from scipy.signal import lfilter
import os
import math
from pydub import AudioSegment

def callCovfefe(x,y,z):

    print("Localizing track at:")
    print("x:")
    print(x)
    print("y:")
    print(y)
    print("z:")
    print(z)
    print("---------------------------")

    negZ = False
    if (z < 0):
        negZ = True
        z *= -1

    print('Calculating distance from source...')
    d = math.sqrt(x**2 + y**2 + z**2) #distance
    print('Calclating azimuth angle...')
    if z == 0: #####Changed to Z
        if x > 0:
            a = 90
        elif x < 0:
            a = -90
        else:
            a = 0
    else:
        a = np.degrees(np.arctan(x / z)) #azimuth #######Changed to Z

    print('Calculating elevation...')
    if d == 0:
        e = 0
    else:
        e = np.degrees(np.arcsin(y / d)) #elevation

    #initialize a list with all of the azimuths used in the CIPIC database (Ca = CIPIC azimuths)
    print('Constructing database...')
    Ca = [-80 , -65, -55, -45]

    i = -40
    while i <= 45:
        Ca.append(i)
        i += 5

    Ca.append(55)
    Ca.append(65)
    Ca.append(80)

    #initialize a list with all of the elevations used in the CIPIC database (Ce = CIPIC elevations)
    Ce =[]

    i = 0
    while i <= 49:
        Ce.append(-45 + 5.625 * i)
        i += 1
    a_index = 0


    while a_index < 25:
        if a < Ca[0]:
            a_index = 0
            break
        elif a > Ca[24]:
            a_index = 24
            break
        elif  Ca[a_index] < a and a < Ca[a_index + 1]:
            break
        elif a == Ca[a_index]:
            break
        elif a > Ca[a_index]:
            a_index += 1
            continue
        elif a < Ca[a_index]:
            a_index -= 1
            continue
        else:
            a_index = 24


    if abs(Ca[a_index - 1] - a) < abs(Ca[a_index] - a):
        a_index -= 1

    if (negZ):
        e = 180-e

    e_index = 0
    while e_index < 50:
        if e < Ce[0]:
            e_index = 0
            break
        elif e > Ce[49]:
            e_index = 50
            break
        elif  Ce[e_index] < e and e < Ce[e_index + 1]:
            break
        elif e == Ce[e_index]:
            break
        elif e > Ce[e_index]:
            e_index += 1
            continue
        elif e < Ce[e_index]:
            e_index -= 1
            continue
        else:
            e_index = 49

    if abs(Ce[e_index - 1] - e) < abs(Ce[e_index] - e):
        e_index -= 1

    print('Finding CIPIC profile...')

    C58 = spio.loadmat('CIPIC_58.mat', squeeze_me=True)

    ITD = C58['ITD']
    hrir_l = C58['hrir_l']
    hrir_r = C58['hrir_r']

    delay = ITD[a_index][e_index] #measured in microseconds (10^-6)
    lft = hrir_l[a_index][e_index] #gives you a bunch of float64
    rgt = hrir_r[a_index][e_index]

    print('Calculating Interaural Time Delay (ITD)...')

    sound = radio.read('recoredSong.wav')

    fs = sound[0] #fs means sample rate is an int
    audio_in = sound[1] #a 2D integer array

    print('Appending data to list...')

    lft_list = list(audio_in)
    rgt_list = list(audio_in)


    print('Creating delay...')
    delay = int(round(ITD[a_index][e_index]))

    if a_index < 13: #sound is coming from the left
        for i in range(0, delay):
            lft_list.append(0)
            rgt_list.insert(0, 0)
            #add zeros to beginning of right and end of left
    else:
        for i in range(0, delay):
            lft_list.insert(0, 0)
            rgt_list.append(0)
            #add zeros to end of right and beginning of left

    wav_left = lfilter(lft, 1.0, audio_in)
    wav_right = lfilter(rgt, 1.0, audio_in)

    track = np.array([wav_left, wav_right]).T.astype(np.int16)

    filename = 'spatializedTrack.wav'
    radio.write(filename, fs, track)

    print('Adding distance...')
    sound = AudioSegment.from_file("spatializedTrack.wav")
    if (d>0):
        sound = sound - math.log(d, 2)*6
    print('Writing track to file...')
    sound.export('spatializedTrack.wav', format='wav')
    print('Localization succesfull!')
