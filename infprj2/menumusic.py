# Import pygame
import pygame
import config
from pygame import mixer

mixer.init()

def load(file):
    pygame.mixer.music.load(file)

def play():
    pygame.mixer.music.play(-1)

def stop():
    pygame.mixer.music.stop()

def init():
    # Check if menu music should be enabled
    if config.get("snd_enabled") == "1":
        load("assets/sounds/happy.wav")
        play()

#Different sounds
click_snd = pygame.mixer.Sound("assets/sounds/Click.wav")
applause_snd = pygame.mixer.Sound("assets/applause6.wav")
yay_snd = pygame.mixer.Sound("assets/yay.wav")
crowd_snd = pygame.mixer.Sound("assets/sounds/Crowd_Applause.wav")
correct_snd = pygame.mixer.Sound("assets/Correct sound.wav")
wrong_snd = pygame.mixer.Sound("assets/Wrong sound.wav")
timer_snd = pygame.mixer.Sound("assets/sounds/Clock_Timer 23 sec.wav")
rektinator_snd = pygame.mixer.Sound("assets/sounds/rektinator.wav")