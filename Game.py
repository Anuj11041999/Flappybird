import random
import sys
import pygame
from pygame.locals import *

FPS = 32
Screenwidth = 289
Screenheight = 600
Screen = pygame.display.set_mode((Screenwidth, Screenheight))
Ground = Screenheight*0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
player = 'gallery/sprites/bird.png'
background = 'gallery/sprites/background.png'
pipe = 'gallery/sprites/pipe.png'

def welcomescreen():
    plx = int(Screenwidth/5)
    ply = int((Screenheight - GAME_SPRITES['player'].get_height())/2)
    mx = int((Screenwidth - GAME_SPRITES['message'].get_width())/2)
    my = int(Screenheight*0.13)
    base = 0
    while True:
        for event in pygame.event.get():
            if event.type== QUIT or(event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                return
            else:
                Screen.blit(GAME_SPRITES['background'],(0,0))
                Screen.blit(GAME_SPRITES['player'],(plx,ply))
                Screen.blit(GAME_SPRITES['message'],(mx,my))
                Screen.blit(GAME_SPRITES['base'],(base,Ground))
                pygame.display.update()
                FPSCLOCK.tick(FPS)
def maingame():
    score = 0
    plx = int(Screenwidth/5)
    ply = int(Screenwidth/2)
    base = 0
    pipe1 = randompipe()
    pipe2 = randompipe()
    upperpipes = [
        {'x':Screenwidth+200,'y':pipe1[0]['y']},
        {'x':Screenwidth+200+(Screenwidth/2),'y':pipe2[0]['y']}
    ]
    lowerpipes = [
        {'x':Screenwidth+200,'y':pipe1[1]['y']},
        {'x':Screenwidth+200+(Screenwidth/2),'y':pipe2[1]['y']}
    ]
    
    pipevelx = -4
    plvely = -9
    plmaxvel = 10
    plminvel = -8
    plAcc = 1
    plflap = -8
    plflapped = False
    while True:
        for event in pygame.event.get():
            if event.type== QUIT or(event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                if ply>0:
                    plvely = plflap
                    plflapped = True
                    GAME_SOUNDS['wing'].play()
        crash = isCollide(plx,ply,upperpipes,lowerpipes)
        if crash:
            return
        playermid = plx+ GAME_SPRITES['player'].get_width()/2
        for pipe in upperpipes:
            pipemid = pipe['x']+GAME_SPRITES['pipe'][0].get_width()/2
            if pipemid<= playermid <pipemid+4:
                score +=1
                print(f"Your score is {score}") 
                GAME_SOUNDS['point'].play()
        if plvely<plmaxvel and not plflapped:
            plvely += plAcc
        if plflapped:
            plflapped= False
        playerheight = GAME_SPRITES['player'].get_height()
        ply = ply +min(plvely,Ground-ply-playerheight)
        
        for upperpipe,lowerpipe in zip(upperpipes,lowerpipes):
            upperpipe['x'] += pipevelx
            lowerpipe['x'] += pipevelx
        if 0<upperpipes[0]['x']<5:
            newpipe = randompipe()
            upperpipes.append(newpipe[0])
            lowerpipes.append(newpipe[1])
        if upperpipes[0]['x']< - GAME_SPRITES['pipe'][0].get_width():
            upperpipes.pop(0)
            lowerpipes.pop(0)
        
        Screen.blit(GAME_SPRITES['background'],(0,0))
        for upperpipe,lowerpipe in zip(upperpipes,lowerpipes):
            Screen.blit(GAME_SPRITES['pipe'][0],(upperpipe['x'],upperpipe['y']))
            Screen.blit(GAME_SPRITES['pipe'][1],(lowerpipe['x'],lowerpipe['y']))
        
        Screen.blit(GAME_SPRITES['base'],(base,Ground))
        Screen.blit(GAME_SPRITES['player'],(plx,ply))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (Screenwidth - width)/2

        for digit in myDigits:
            Screen.blit(GAME_SPRITES['numbers'][digit], (Xoffset, Screenheight*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(plx,ply,upperpipes,lowerpipes):
    if ply> Ground - 25  or ply<0:
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperpipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(ply < pipeHeight + pipe['y'] and abs(plx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerpipes:
        if (ply + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(plx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False


def randompipe():
    pipeheight= GAME_SPRITES['pipe'][0].get_height()
    offset = int(Screenheight/4)
    y2 = offset + random.randrange(0, int(Screenheight-GAME_SPRITES['base'].get_height() - 1.2*offset))
    pipex = Screenwidth+10
    y1 = pipeheight - y2+offset
    pipe=[
        {'x':pipex,'y':-y1},
        {'x':pipex,'y':y2}
    ]
    return pipe


if __name__ == "__main__":
    pygame.init() 
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird')
    GAME_SPRITES['numbers'] = (
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
    )
    GAME_SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(pipe).convert_alpha(),180),
        pygame.image.load(pipe).convert_alpha()
    )
    GAME_SPRITES['background'] = pygame.image.load(background).convert()
    GAME_SPRITES['player'] = pygame.image.load(player).convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['message'] = pygame.image.load('gallery/sprites/message.png').convert_alpha()
    
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    while True:
        welcomescreen() 
        maingame()
    
