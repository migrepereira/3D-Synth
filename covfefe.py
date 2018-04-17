import numpy as np
import scipy as sp
import scipy.io as spio
import scipy.io.wavfile as radio
import os
import math

def callCovfefe(x,y,z):

    print("Localizing track at:")
    print("x:")
    print(x)
    print("y:")
    print(y)
    print("z:")
    print(z)
    print("---------------------------")

    print('Calculating distance from source...')
    d = math.sqrt(x**2 + y**2 + z**2) #distance

    print('Calclating azimuth angle...')
    if y == 0:
        if x > 0:
            a = 90
        elif x < 0:
            a = -90
        else:
            a = 0
    else:
        a = np.degrees(np.arctan(x / y)) #azimuth

    print('Calculating elevation...')
    if d == 0:
        e = 0
    else:
        e = np.degrees(np.arcsin(y / d)) #elevation

    '''
    DEFINING THE AZIMUTHS AND ELEVATIONS USED IN THE CIPIC DATABASE
    '''

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


    '''
    FINDING THE CLOSEST AZIMUTH AND ELEVATION FROM THE CIPIC DATABASE TO MATCH THE USER'S SELECTED LOCATION
    '''
    print('Comparing...')
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

    print('Azimuth index found.')


    e_index = 0

    while e_index < 50:
        if  Ce[e_index] < e and e < Ce[e_index + 1]:
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

    print('Elevation index found.')


    '''
    USES A_INDEX AND E_INDEX TO FIND RELEVANT INFORMATION FROM THE CIPIC DATABASE
    '''
    print('Finding CIPIC profile...')

    C58 = spio.loadmat('CIPIC_58.mat', squeeze_me=True)

    ITD = C58['ITD']
    hrir_l = C58['hrir_l']
    hrir_r = C58['hrir_r']

    delay = ITD[a_index][e_index] #measured in microseconds (10^-6)
    lft = hrir_l[a_index][e_index] #gives you a bunch of float64
    rgt = hrir_r[a_index][e_index]

    print(lft)
    print('Calculating Interaural Time Delay (ITD)...')


    '''
    RADIO
    '''
    sound = radio.read('recoredSong.wav')

    fs = sound[0] #fs means sample rate is an int
    audio_in = sound[1] #a 2D integer array

    print(audio_in)

    lft_list = [] #a list of values in the left and right channels
    rgt_list = [] #lists are easier to edit and add values to, which will become useful when adding the delay

    print('Appending data to list...')

    for i in range(0,200):
        lft_list.append(lft[i])
        rgt_list.append(rgt[i])
        i += 1

    if a_index < 13: #sound is coming from the left
        for i in range(0, 15): #15 is a sample delay?
            lft_list.append(0)
            rgt_list.insert(0, 0)
            i += 1
        #add zeros to beginning of right and end of left
    else:
        for i in range(0, 15):
            lft_list.insert(0, 0)
            rgt_list.append(0)
            #add zeros to end of right and beginning of left


    left_array = np.asarray(lft_list)
    right_array = np.asarray(rgt_list)

    wav_left = np.convolve(left_array, audio_in[0])
    wav_right = np.convolve(right_array, audio_in[0])

    track = np.asarray([wav_left, wav_right])

    wav_left = np.asarray(wav_left)

    print('Writing track to file...')

    print('★░░░░░░░░░░░████░░░░░░░░░░░░░░░░░░░░★')
    print('★░░░░░░░░░███░██░░░░░░░░░░░░░░░░░░░░★')
    print('★░░░░░░░░░██░░░█░░░░░░░░░░░░░░░░░░░░★')
    print('★░░░░░░░░░██░░░██░░░░░░░░░░░░░░░░░░░★')
    print('★░░░░░░░░░░██░░░███░░░░░░░░░░░░░░░░░★')
    print('★░░░░░░░░░░░██░░░░██░░░░░░░░░░░░░░░░★')
    print('★░░░░░░░░░░░██░░░░░███░░░░░░░░░░░░░░★')
    print('★░░░░░░░░░░░░██░░░░░░██░░░░░░░░░░░░░★')
    print('★░░░░░░░███████░░░░░░░██░░░░░░░░░░░░★')
    print('★░░░░█████░░░░░░░░░░░░░░███░██░░░░░░★')
    print('★░░░██░░░░░████░░░░░░░░░░██████░░░░░★        S U C C E S S')
    print('★░░░██░░████░░███░░░░░░░░░░░░░██░░░░★')
    print('★░░░██░░░░░░░░███░░░░░░░░░░░░░██░░░░★')
    print('★░░░░██████████░███░░░░░░░░░░░██░░░░★')
    print('★░░░░██░░░░░░░░████░░░░░░░░░░░██░░░░★')
    print('★░░░░███████████░░██░░░░░░░░░░██░░░░★')
    print('★░░░░░░██░░░░░░░████░░░░░██████░░░░░★')
    print('★░░░░░░██████████░██░░░░███░██░░░░░░★')
    print('★░░░░░░░░░██░░░░░████░███░░░░░░░░░░░★')
    print('★░░░░░░░░░█████████████░░░░░░░░░░░░░★')
    print('★░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░★')

    filename = 'spatializedTrack.wav'


    radio.write(filename, fs, audio_in)

    print('Your track ' + filename + ' is done!')

    os.system('start ' + filename)
