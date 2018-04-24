#Cameron Cook

import pygame
import time

def playWAV():
    pygame.init()
    pygame.mixer.init()
    sounda= pygame.mixer.Sound("recoredSong.wav")
    sounda.play()

def playSpace():
    pygame.init()
    pygame.mixer.init()
    sounda= pygame.mixer.Sound("spatializedTrack.wav")
    sounda.play()
