# Game python file
import pygame
import button
import random
import time
import translate
import questions

def update(game):
    pass

# Deze class zorgt ervoor dat het dice systeem werkt
class Dice:
    def __init__(self):
        # zet de begin image van de die naar een lege
        self.image ="assets\img\die0.png"
    def onclick(self,game):
        if not game.ourturn:
            return

        # TODO: niet display.flip gebruiken
        for x in range(20):
            self.newimg = "assets\img\die{}.png".format(random.randrange(1,7))
            while self.newimg == self.image:
                self.newimg = "assets\img\die{}.png".format(random.randrange(1,7))
            self.image = self.newimg
            self.draw(game)
            pygame.display.flip()
            time.sleep(0.05)
        # dit pakt een random nummer van 1 t/m 6 en slaat het op in game.dice_roll
        game.dice_roll = random.randrange(1, 7)
        # dit zet het plaatje van de die naar hetgeen wat gegooid is
        self.image = "assets\img\die{}.png".format(game.dice_roll)
    def draw(self,game):
        # dit tekent de die
        if game.dice_roll == 0:
            game.screen.blit((pygame.font.Font(None, 20)).render("Roll the die!", 1, (0,0,0)),(665, 515))
        button.draw_img(game, game.width - 130, game.height - 70, 64, 64, "", 0, self.image, (0,0,0), self.onclick)

dice = Dice()

def question_chosen(game, idx):
    game.ourturn = False

def callback_question1(game):
    question_chosen(game, 1)
    

def callback_question2(game):
    question_chosen(game, 2)

def callback_question3(game):
    question_chosen(game, 3)


def draw(game):
	#Achtergrond kleur
    pygame.draw.rect(game.screen,(204,204,204),(600,0,game.width * 0.9,game.height * 1))

	#Teken dice
    dice.draw(game)

	#Teken categorie kleur
    pygame.draw.rect(game.screen,(255,0,0),(32,32,110,game.height * 0.8))
    pygame.draw.rect(game.screen,(255,239,0),(162,32,110,game.height * 0.8))
    pygame.draw.rect(game.screen,(52,163,253),(292,32,110,game.height * 0.8))
    pygame.draw.rect(game.screen,(24,208,27),(422,32,110,game.height * 0.8))

	#Start onder categorie
    font = pygame.font.Font(None, 48)
    font2 = pygame.font.Font(None, 20)
    label_1 = font.render("Start", 1, (255,255,255))
    size = font.size("Start")
    game.screen.blit(label_1,(45, game.height * 0.9))
    game.screen.blit(label_1,(175, game.height * 0.9))
    game.screen.blit(label_1,(305, game.height * 0.9))
    game.screen.blit(label_1,(435, game.height * 0.9))
    if game.ourturn == False:
        game.screen.blit(font2.render("Correct!", 1, (255,255,255)), (32,17))

    # Teken popup venster
    if game.ourturn:
        if not game.didgeneratequestions:
            game.didgeneratequestions = True

            # remove existing answers
            game.answers.clear()

            # add new answers   
            question = random.randrange(1,41)
            game.answers.append("QUESTION{}_ANSWER1".format(question))
            game.answers.append("QUESTION{}_ANSWER2".format(question))
            game.answers.append("QUESTION{}_ANSWER3".format(question))
            game.answers.append("QUESTION{}".format(question))
            print(question)
            pass

        if game.dice_roll != 0:
            pygame.draw.rect(game.screen,(255,255,255),(24,9,game.width*0.8 + 2,game.height * 0.9 + 2))
            pygame.draw.rect(game.screen,(153,146,245),(25,10,game.width*0.8,game.height * 0.9))
            game.screen.blit(font2.render(translate.translate(game.answers[3]), 1, (255,255,255)), (32,17))
            button.draw(game, game.width * 0.25,162,300,60, translate.translate(game.answers[0]), 20, (0,0,0), (255,255,255), callback_question1)
            button.draw(game, game.width * 0.25,252,300,60, translate.translate(game.answers[1]), 20, (0,0,0), (255,255,255), callback_question2)
            button.draw(game, game.width * 0.25,342,300,60, translate.translate(game.answers[2]), 20, (0,0,0), (255,255,255), callback_question3)
            pass

def init(game):
    pass