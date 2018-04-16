import pygame
import time

def playSong():
    pygame.init()
    pygame.mixer.init()
    sounda= pygame.mixer.Sound("mySong.wav")
    sounda.play()
