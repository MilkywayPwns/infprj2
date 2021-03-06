# Game python file
import pygame
import button
import random
import time
import translate
import questions
import textbox
import player
import checkbox
import math
import menumusic
import score

def update(game):
    pass

# Deze class zorgt ervoor dat het dice systeem werkt
class Dice:
    def __init__(self):
        # zet de begin image van de die naar een lege
        self.image = "assets\img\die0.png"
    def onclick(self,game):
        if game.get_current_player().did_roll:
            return

        # TODO: niet display.flip gebruiken
        for x in range(15):
            self.newimg = "assets\img\die{}.png".format(random.randrange(1,7))
            while self.newimg == self.image:
                self.newimg = "assets\img\die{}.png".format(random.randrange(1,7))
            self.image = self.newimg
            self.draw(game)
            pygame.display.flip()
            time.sleep(0.05)

        # dit pakt een random nummer van 1 t/m 6 en slaat het op in game.dice_roll
        game.get_current_player().dice_roll = random.randrange(1, 7)
        game.get_current_player().did_roll = True

        # dit zet het plaatje van de die naar hetgeen wat gegooid is
        self.image = "assets\img\die{}.png".format(game.get_current_player().dice_roll)

        	#Entertainment questions
        if game.get_current_player().pos.get_col() == 1:
             game.question = random.randrange(1,31)
				#History questions
        elif game.get_current_player().pos.get_col() == 2:
             game.question = random.randrange(31,44)
				#Sport questions
        elif game.get_current_player().pos.get_col() == 3:
             game.question = random.randrange(44,59)
				#Geography questions
        elif game.get_current_player().pos.get_col() == 4:
             game.question = random.randrange(59,70)
        game.get_current_player().turn_start = time.clock()
        
    def draw(self,game):
        # dit tekent de die
        label = (pygame.font.Font(None, 20)).render(translate.translate("ROLL"),1,(0,0,0))
        self.size = (pygame.font.Font(None, 20)).size(translate.translate("ROLL"))
        if game.get_current_player().did_roll == False and not game.get_current_player().direction == None:
            game.screen.blit(label, (702 - self.size[0]/2, 515))
        button.draw_img(game, game.width - 130, game.height - 70, 64, 64, "", 0, self.image, (0,0,0), self.onclick)

def correct_answer(game):
    for x in range(1,4):
        if translate.translate(game.get_current_player().answers[x-1]) == translate.translate("QUESTIONANSWER{}".format(game.question)):
            return x
            break

    print("Question {} is incorrect!".format(game.question))
    return 1

class GameLogic:
    def __init__(self):
        self.dice = Dice()
    def draw(self, game):
        # draw players in rows
        for plr in game.players:
            plr.draw()

        # draw questions etc
        if game.get_current_player().did_roll and not game.get_current_player().did_answer and not game.get_current_player().moves_left:
            if not game.get_current_player().did_generate_question:

                # remove existing answers
                game.get_current_player().answers.clear()

                # add new answers
                game.get_current_player().answers.append("QUESTION{}_ANSWER1".format(game.question))
                game.get_current_player().answers.append("QUESTION{}_ANSWER2".format(game.question))
                game.get_current_player().answers.append("QUESTION{}_ANSWER3".format(game.question))
                game.get_current_player().answers.append("QUESTION{}".format(game.question))

                # do not re-generate question
                game.get_current_player().did_generate_question = True

            # draw question popup
            if not game.get_current_player().isAI:
                font = pygame.font.Font(None, 20)
                pygame.draw.rect(game.screen,(255,255,255),(24,9,game.width*0.8 + 2,game.height * 0.9 + 2))

				# change popup according to category
                # entertainment question popup
                if game.get_current_player().pos.get_col() == 1: 
                     pygame.draw.rect(game.screen,(255,0,0),(25,10,game.width*0.8,game.height * 0.9))
				# history question popup 
                elif game.get_current_player().pos.get_col() == 2:
                     pygame.draw.rect(game.screen,(200,200,0),(25,10,game.width*0.8,game.height * 0.9))
				# sport question popup
                elif game.get_current_player().pos.get_col() == 3:
                     pygame.draw.rect(game.screen,(52,163,253),(25,10,game.width*0.8,game.height * 0.9))
				# geography question popup
                elif game.get_current_player().pos.get_col() == 4:
                     pygame.draw.rect(game.screen,(24,208,27),(25,10,game.width*0.8,game.height * 0.9))

                game.screen.blit(font.render(translate.translate(game.get_current_player().answers[3]), 1, (255,255,255)), (32,17))
                button.draw(game, game.width * 0.25,162,300,60, translate.translate(game.get_current_player().answers[0]), 20, (0,0,0), (255,255,255), lambda game: question_chosen(game, 1))
                button.draw(game, game.width * 0.25,252,300,60, translate.translate(game.get_current_player().answers[1]), 20, (0,0,0), (255,255,255), lambda game: question_chosen(game, 2))
                button.draw(game, game.width * 0.25,342,300,60, translate.translate(game.get_current_player().answers[2]), 20, (0,0,0), (255,255,255), lambda game: question_chosen(game, 3))
                if math.floor((time.clock() - game.get_current_player().turn_start) / 2) < 12:
                    menumusic.timer_snd.play(1)
                    game.screen.blit(pygame.image.load("assets\img\hourglass{}.png".format(math.floor((time.clock() - game.get_current_player().turn_start) / 2))), (600, 40))
                else:
                    question_chosen(game, 5)
            else:
                if random.randrange(1,4) == 2:
                    question_chosen(game, correct_answer(game))
                else:
                    question_chosen(game, random.randrange(1, 4))
        elif not game.get_current_player().did_roll and not game.get_current_player().did_choose_row:
            # draw start buttons
            if not game.get_current_player().isAI:
                if 1 not in game.chosen:
                    button.draw(game, 45, game.height * 0.9, 100, 32, "Start", 20, (0,0,0), (255,255,255), lambda game: start_chosen(game, 1))
                if 2 not in game.chosen:
                    button.draw(game, 175, game.height * 0.9, 100, 32, "Start", 20, (0,0,0), (255,255,255), lambda game: start_chosen(game, 2))
                if 3 not in game.chosen:
                    button.draw(game, 305, game.height * 0.9, 100, 32, "Start", 20, (0,0,0), (255,255,255), lambda game: start_chosen(game, 3))
                if 4 not in game.chosen:
                    button.draw(game, 435, game.height * 0.9, 100, 32, "Start", 20, (0,0,0), (255,255,255), lambda game: start_chosen(game, 4))
            else:
                time.sleep(0.4)
                chosen = False
                while not chosen:
                    number = random.randrange(1,5)
                    if not number in game.chosen:
                        start_chosen(game,number)
                        chosen = True
        elif game.get_current_player().direction == None: 
            if not game.get_current_player().isAI:
                # draw movement buttons
                button.draw_img(game, game.width - 145, game.height - 264, 80, 80, "", 0, "assets/img/pijlomhoog.png", (0,0,0), lambda game: game.get_current_player().set_direction("up"))
                button.draw_img(game, game.width - (145 + 40), game.height - 200, 80, 80, "", 0, "assets/img/pijllinks.png", (0,0,0), lambda game: game.get_current_player().set_direction("left"))
                button.draw_img(game, game.width - (145 - 40), game.height - 200, 80, 80, "", 0, "assets/img/pijlrechts.png", (0,0,0), lambda game: game.get_current_player().set_direction("right"))
                # button.draw(game, 435, game.height * 0.9, 100, 32, "Start", 20, (0,0,0), (255,255,255), lambda game: start_chosen(game, 4))
            else:
                time.sleep(0.3)
                if game.get_current_player().pos.get_y() > 2 and game.get_current_player().pos.get_y() < 13:
                    for plr in game.players:
                        if game.get_current_player().pos.get_col() == plr.pos.get_col() + 1 and game.get_current_player().pos.get_y() == plr.pos.get_y() and plr != game.get_current_player():
                            game.get_current_player().set_direction("left")
                        if game.get_current_player().pos.get_col() == plr.pos.get_col() - 1 and game.get_current_player().pos.get_y() == plr.pos.get_y() and plr != game.get_current_player():
                            game.get_current_player().set_direction("right")
                        if game.get_current_player().pos.get_col() == plr.pos.get_col() + 2 and plr.pos.get_x() == 1 and game.get_current_player().pos.get_y() == plr.pos.get_y() and plr != game.get_current_player():
                            game.get_current_player().set_direction("left")
                        if game.get_current_player().pos.get_col() == plr.pos.get_col() - 2 and plr.pos.get_x() == 0 and game.get_current_player().pos.get_y() == plr.pos.get_y() and plr != game.get_current_player():
                            game.get_current_player().set_direction("right")
                        if game.get_current_player().pos.get_col() == 1 and plr.pos.get_col() == 4 or (plr.pos.get_col() == 3 and plr.pos.get_x() == 1 and game.get_current_player().pos.get_x() == 0) and game.get_current_player().pos.get_y() == plr.pos.get_y() and plr != game.get_current_player():
                            game.get_current_player().set_direction("left")
                        if game.get_current_player().pos.get_col() == 4 and plr.pos.get_col() == 1 or (plr.pos.get_col() == 2 and plr.pos.get_x() == 0 and game.get_current_player().pos.get_x() == 1) and game.get_current_player().pos.get_y() == plr.pos.get_y() and plr != game.get_current_player():
                            game.get_current_player().set_direction("right")
                        if game.get_current_player().pos.get_col() == plr.pos.get_col() and game.get_current_player().pos.get_y() == plr.pos.get_y() and game.get_current_player().pos.get_x() == plr.pos.get_x() - 1 and plr != game.get_current_player():
                            game.get_current_player().set_direction("right")
                        if game.get_current_player().pos.get_col() == plr.pos.get_col() and game.get_current_player().pos.get_y() == plr.pos.get_y() and game.get_current_player().pos.get_x() == plr.pos.get_x() + 1 and plr != game.get_current_player():
                            game.get_current_player().set_direction("left")
                        if game.get_current_player().pos.get_y() > 9 and game.get_current_player().pos.get_y() == plr.pos.get_y() and plr != game.get_current_player():
                            game.get_current_player().set_direction("right")
                if game.get_current_player().direction == None:
                    game.get_current_player().set_direction("up")
        elif game.get_current_player().moves_left:
            if game.get_current_player().direction == "up":
                game.get_current_player().go_up()
            elif game.get_current_player().direction == "left":
                game.get_current_player().go_left()
            elif game.get_current_player().direction == "right":
                game.get_current_player().go_right()
            elif game.get_current_player().direction == "down":
                game.get_current_player().go_down()

        # draw die
        if game.get_current_player().did_choose_row and not game.get_current_player().direction == None and not game.get_current_player().moves_left:
            if game.get_current_player().isAI:
                pygame.display.flip()
                if not game.get_current_player().did_roll:
                    pygame.display.flip()
                    time.sleep(0.4)
                    self.dice.onclick(game)
    
            self.dice.draw(game)

gamelogic = GameLogic()

def question_chosen(game, idx):
    # game.set_next_player()
    # gamelogic.dice.image = "assets\img\die0.png"
    # check if the question was answerred correctly
    # increment score for correct question, and set the amount of moves we can make.
    menumusic.timer_snd.stop()
    game.get_current_player().turn_start = 0

    if idx == 5:
        game.get_current_player().score -= 10
        game.get_current_player().set_direction(None)
        game.set_next_player()
        corrfont = pygame.font.Font(None, 72)
        label_1 = corrfont.render(translate.translate("OVERTIME"), 1, (200,0,0))
        size = corrfont.size(translate.translate("OVERTIME"))
        game.screen.blit(label_1,(int(game.width/2 - (size[0]/2 + 45)), game.height/5 - (size[1]/2)))
        pygame.display.flip()
        time.sleep(0.7)
    elif translate.translate(game.get_current_player().answers[idx-1]) == translate.translate("QUESTIONANSWER{}".format(game.question)):
        #correct sound
        menumusic.correct_snd.play()
        game.get_current_player().moves_left = math.ceil(game.get_current_player().dice_roll / 2)
        game.get_current_player().score += (15 * game.get_current_player().moves_left) + ((game.get_current_player().moves_left * 10) - 10)

        # update score in database
        score.update(game.get_current_player().name, game.get_current_player().score)

        corrfont = pygame.font.Font(None, 72)
        label_1 = corrfont.render("CORRECT!", 1, (0,200,0))
        label_2 = (pygame.font.Font(None, 30)).render("+" + str((15 * game.get_current_player().moves_left) + ((game.get_current_player().moves_left * 10) - 10)) + " score", 1, (0,200,0))
        size = corrfont.size("CORRECT!")
        size2 =  (pygame.font.Font(None, 30)).size("+" + str((15 * game.get_current_player().moves_left) + ((game.get_current_player().moves_left * 10) - 10)) + " score")
        game.screen.blit(label_1,(int(game.width/2 - (size[0]/2 + 45)), game.height/5.5 - (size[1]/2)))
        game.screen.blit(label_2,(int(game.width/2 - (size[0]/2 - 25)), game.height/5 - (size[1]/2) + 35))
        pygame.display.flip()
        time.sleep(0.7)
    else:
		#incorrect sound
        menumusic.wrong_snd.play()
        game.get_current_player().score -= 10
        game.get_current_player().set_direction(None)
        game.set_next_player()
        corrfont = pygame.font.Font(None, 72)
        label_1 = corrfont.render("INCORRECT!", 1, (200,0,0))
        label_2 = (pygame.font.Font(None, 30)).render("-10 score", 1, (200,0,0))
        size = corrfont.size("INCORRECT!")
        size2 =  (pygame.font.Font(None, 30)).size("-10 score")
        game.screen.blit(label_1,(int(game.width/2 - (size[0]/2 + 45)), game.height/5.5 - (size[1]/2)))
        game.screen.blit(label_2,(int(game.width/2 - (size[0]/2 - 50)), game.height/5 - (size[1]/2) + 35))
        pygame.display.flip()
        time.sleep(0.7)

def start_chosen(game, idx):
    game.get_current_player().setpos(idx, 0, 0)
    game.get_current_player().did_choose_row = True
    game.chosen.append(idx)
    game.set_next_player()

def TBcallback(game, box, isEnterPressed, id, next):
    SetName(id, game, box)
    if isEnterPressed == True and next != None:
        textbox.textfields[id].isFocussed = False
        textbox.textfields[next].isFocussed = True
    elif isEnterPressed == True and next == None:
        textbox.textfields[id].isFocussed = False

def SetPlayerCount(game, idx):
    if idx == 2:
        game.players.append(player.Player(game))
        game.players.append(player.Player(game))
        textbox.create(game, game.width * 0.3, game.height * 0.2, 250, "", lambda game,box,isEnterPressed: TBcallback(game, box, isEnterPressed, 0, 1))
        textbox.create(game, game.width * 0.3, game.height * 0.35, 250, "", lambda game,box,isEnterPressed: TBcallback(game, box, isEnterPressed, 1, None))
        checkbox.create(game, game.width * 0.7, game.height * 0.35, "AI", False, lambda game,box: SetAI(1, game, box))
    if idx == 3:
        game.players.append(player.Player(game))
        game.players.append(player.Player(game))
        game.players.append(player.Player(game))
        textbox.create(game, game.width * 0.3, game.height * 0.2, 250, "", lambda game,box,isEnterPressed: TBcallback(game, box, isEnterPressed, 0, 1))
        textbox.create(game,game.width * 0.3, game.height * 0.35, 250, "", lambda game,box,isEnterPressed: TBcallback(game, box, isEnterPressed, 1, 2))
        textbox.create(game, game.width * 0.3, game.height * 0.50, 250, "", lambda game,box,isEnterPressed: TBcallback(game, box, isEnterPressed, 2, None))
        checkbox.create(game, game.width * 0.7, game.height * 0.35, "AI", False, lambda game,box: SetAI(1, game, box))
        checkbox.create(game, game.width * 0.7, game.height * 0.50, "AI", False, lambda game,box: SetAI(2, game, box))
    if idx == 4:
        game.players.append(player.Player(game))
        game.players.append(player.Player(game))
        game.players.append(player.Player(game))
        game.players.append(player.Player(game))
        textbox.create(game, game.width * 0.3, game.height * 0.2, 250, "", lambda game,box,isEnterPressed: TBcallback(game, box, isEnterPressed, 0, 1))
        textbox.create(game, game.width * 0.3, game.height * 0.35, 250, "", lambda game,box,isEnterPressed: TBcallback(game, box, isEnterPressed, 1, 2))
        textbox.create(game, game.width * 0.3, game.height * 0.50, 250, "", lambda game,box,isEnterPressed: TBcallback(game, box, isEnterPressed, 2, 3))
        textbox.create(game, game.width * 0.3, game.height * 0.65, 250, "", lambda game,box,isEnterPressed: TBcallback(game, box, isEnterPressed, 3, None))
        checkbox.create(game, game.width * 0.7, game.height * 0.20, "AI", False, lambda game,box: SetAI(0, game, box))
        checkbox.create(game, game.width * 0.7, game.height * 0.35, "AI", False, lambda game,box: SetAI(1, game, box))
        checkbox.create(game, game.width * 0.7, game.height * 0.50, "AI", False, lambda game,box: SetAI(2, game, box))
        checkbox.create(game, game.width * 0.7, game.height * 0.65, "AI", False, lambda game,box: SetAI(3, game, box))

    game.playercount = idx

def StartGame(game):
    
    for x in range(0, game.playercount):
        if not len(game.players[x].name):
            return

    game.has_started = True
    

def draw(game):
    if game.has_started:
        # Make sure the playername boxes are gone
        textbox.remove(game)
        checkbox.remove(game)
	    # Achtergrond kleur
        pygame.draw.rect(game.screen,(204,204,204),(600,0,game.width * 0.9,game.height * 1))

	    # Teken categorie kleur
        pygame.draw.rect(game.screen,(255,0,0),(32,32,110,game.height * 0.8))
        pygame.draw.rect(game.screen,(255,239,0),(162,32,110,game.height * 0.8))
        pygame.draw.rect(game.screen,(52,163,253),(292,32,110,game.height * 0.8))
        pygame.draw.rect(game.screen,(24,208,27),(422,32,110,game.height * 0.8))
        game.screen.blit(pygame.image.load("assets\img\dots.png"), (60, 98))

	    # Start onder categorie
        font = pygame.font.Font(None, 48)
        font2 = pygame.font.Font(None, 20)
        font3 = pygame.font.Font(None, 28)
        # label_1 = font.render("Start", 1, (255,255,255))
        # size = font.size("Start")
        # game.screen.blit(label_1,(45, game.height * 0.9))
        # game.screen.blit(label_1,(175, game.height * 0.9))
        # game.screen.blit(label_1,(305, game.height * 0.9))
        # game.screen.blit(label_1,(435, game.height * 0.9))

        # Player turn info
        turnlabel = font3.render("It's \"{}'s\" turn.".format(game.get_current_player().name), 1, (255,255,255))
        game.screen.blit(turnlabel, (0, 0))
        game.screen.blit(font.render("SCORES:", 1, (0,0,0)), (700 - font.size("SCORES:")[0]/2, 10))
        sortedlist = sorted(game.players, key=lambda x: x.score, reverse=True)
        for x in range(game.playercount):
            game.screen.blit(font3.render(str(sortedlist[x].name) + ": " + str(sortedlist[x].score), 1, (0,0,0)), (700 - font3.size(str(sortedlist[x].name) + ": " + str(sortedlist[x].score))[0]/2, 50 + x*25))

        # Gamelogic drawing
        gamelogic.draw(game)
    elif game.playercount:
        game.screen.fill((60,60,60))
        font = pygame.font.Font(None, 30)
        label_1 = font.render(translate.translate("MAKE"), 1, (255,255,255))
        size = font.size(translate.translate("MAKE"))
        game.screen.blit(label_1,(game.width * 0.32, game.height * 0.1))
        # Draw the boxes for the player names
        textbox.draw(game)
        checkbox.draw(game)
        button.draw(game, game.width * 0.4, game.height * 0.8, 64, 32, "Start", 20, (0,0,0), (255,255,255), lambda game: StartGame(game))
    else:
        game.screen.fill((60,60,60))
        button.draw(game, 10, 10, game.width / 10, game.height / 20, translate.translate("BACK"), 20, (25,25,25), (255,255,255), lambda x: game.set_state(game.last_state))
        font = pygame.font.Font(None, 30)
        label_1 = font.render(translate.translate("AMOUNT"), 1, (255,255,255))
        size = font.size(translate.translate("AMOUNT"))
        game.screen.blit(label_1,(game.width * 0.37, game.height * 0.2))
        button.draw(game, game.width * 0.42, game.height * 0.3, 128, 64, "2", 30, (0,0,0), (255,255,255), lambda game: SetPlayerCount(game, 2))
        button.draw(game, game.width * 0.42, game.height * 0.45, 128, 64, "3", 30, (0,0,0), (255,255,255), lambda game: SetPlayerCount(game, 3))
        button.draw(game, game.width * 0.42, game.height * 0.60, 128, 64, "4", 30, (0,0,0), (255,255,255), lambda game: SetPlayerCount(game, 4))

# This function is being called when the text in a name box changes
def SetName(idx, game, box):
    game.players[idx].setname(box.text)

# This function is called when an AI checkbox is clicked.
def SetAI(idx, game, box):
    print("Player {} AI state is {}".format(idx, box.isChecked))
    game.players[idx].setai(box.isChecked)

def init(game):
    game.isMP = False