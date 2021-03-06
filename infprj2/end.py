# End-screen python file
import pygame
import button
import translate
import menumusic

def update(game):
    pass

def init(game):
    menumusic.yay_snd.play()
    menumusic.applause_snd.play()
    menumusic.crowd_snd.play()
 
def rot_center(image, rect, angle):
        #rotate an image while keeping its center
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image,rot_rect

def draw(game):
    # Termination screen colour
    game.screen.fill((160, 187, 194))
    font = pygame.font.Font(None, 72)
    if game.has_started == True:
        game.players = []
        game.playercount = 0
        game.current_player = 0
        game.has_started = False
        game.question = 0
        game.chosen = []

    # Termination screen text + colour
    label_1 = font.render(game.winner + " " + translate.translate("PLAYER_WON"), 1, (212,175,55))
    size = font.size(game.winner + " " + translate.translate("PLAYER_WON"))

    # Placement text in screen
    game.screen.blit(label_1,(int(game.width/2 - (size[0]/2)), game.height*0.1 - (size[1]/2)))
    
    bg = pygame.image.load("assets/img/Lego_met_vlag4.png")
    game.screen.blit(bg,(game.width/2.4 ,game.height*0.2 ))
    party1 = pygame.image.load("assets/img/party1.png")
    # rotate image clockwise
    game.angle += 1
    if game.angle >= 360:
        game.angle = 0
    rot_party1 = rot_center(party1,party1.get_rect(), game.angle)[0]
    game.screen.blit(rot_party1,(game.width/1.4 ,game.height*0.2))
    party3 = pygame.image.load("assets/img/party3.png")
    #rotate image anticlockwise
    game.angle1 -= 1
    if game.angle1 >= 360:
        game.angle1 = 0
    rot_party3 = rot_center(party3, party3.get_rect(), game.angle1)[0]
    game.screen.blit(rot_party3,(game.width/15.0 ,game.height*0.2))
   
    
    # button variables
    btn_width = game.width / 5;
    btn_height = game.height / 10;
    btn_x_off = (game.width / 2) - (btn_width / 2)
    btn_y_off = lambda idx: (game.height / 10) * (idx + 1) + (idx * 10)

    button.draw(game, btn_x_off, btn_y_off(6), int(btn_width), int(btn_height), translate.translate("BACK"), 20, (25,25,25), (255,255,255), lambda x: game.set_state(0))