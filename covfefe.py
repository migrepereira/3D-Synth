import numpy as np
import scipy as sp
import scipy.io as spio
import scipy.io.wavfile as radio
import os
import math

#def callCovfefe():

x = int(input("x value: "))

y = int(input("y value: "))

z = int(input("z value: "))

print()

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

print()
print('Azimuth: ' + str(math.ceil(a)) + ' degrees')
print('Elevation: ' + str(math.ceil(e)) + ' degrees')


'''
DEFINING THE AZIMUTHS AND ELEVATIONS USED IN THE CIPIC DATABASE
'''

print()
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
print()
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
print(a_index)
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
print(e_index)

'''
USES A_INDEX AND E_INDEX TO FIND RELEVANT INFORMATION FROM THE CIPIC DATABASE
'''
print()
print('Loading CIPIC profile...')

C58 = spio.loadmat('CIPIC_58.mat', squeeze_me=True)

ITD = C58['ITD']
hrir_l = C58['hrir_l']
hrir_r = C58['hrir_r']

delay = ITD[a_index][e_index] #measured in microseconds (10^-6)
lft = hrir_l[a_index][e_index] #gives you a bunch of float64
rgt = hrir_r[a_index][e_index]

'''
RADIO
'''
sound = radio.read('A.wav')

fs = sound[0] #fs means sample rate is an int
audio_in = sound[1] #a 2D integer array

hold = int(fs * 0.2)

print()
print('Appending data to list...')

lft_list = list(lft) #a list of values in the left and right channels
rgt_list = list(rgt) #lists are easier to edit and add values to, which will become useful when adding the delay

print('Creating delay...')
if a_index < 13: #sound is coming from the left 
    for i in range(0, 15): #15 is a sample delay?
        lft_list.append(0)
        rgt_list.insert(0, 0)
    #add zeros to beginning of right and end of left
else:
    for i in range(0, 15):
        lft_list.insert(0, 0)
        rgt_list.append(0)
        #add zeros to end of right and beginning of left


left_array = np.asarray(lft_list)
right_array = np.asarray(rgt_list)

wav_left = np.convolve(left_array, audio_in)
wav_right = np.convolve(right_array, audio_in)

print(wav_left)
print()
for i in range(0 , len(wav_left)):
    wav_left[i] = math.ceil(wav_left[i] * 100000)
    wav_right[i] = math.ceil(wav_right[i] * 100000)

print(wav_left)


#for i in range(0 , len(wav_left))
#wav_left = [np.convolve(left_array, audio_in), np.zeros((1, hold))]
#wav_right = [np.convolve(right_array, audio_in), np.zeros((1, hold))]

track = np.column_stack((wav_left, wav_right))

print('Writing track to file...')
print()
'''
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
'''
print('★░░░██░░░░░████░░░░░░░░░░██████░░░░░★        S U C C E S S')
'''
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
'''
print()
filename = input("Name your track: ")
filename = filename + '.wav'

radio.write(filename, fs, track)

print()
print('Your track ' + filename + ' is done!')


print('TRACK')
print(track)
print()
print('audio_in')
print(audio_in)

os.system('start ' + filename)
