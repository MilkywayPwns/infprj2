import pygame
import database
import time
import score
from packet import Packet

# constant variables
row_xoff = [32, 162, 292, 422]
row_xoff_s = [32, 110 - 10 - 32]

class Position:
    def __init__(self, col, x, y):
        self.col = col
        self.x = x
        self.y = y
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def get_col(self):
        return self.col
    def get_pos(self):
        return (self.col, self.x, self.y)

class Player:
    def __init__(self, game):
        self.index = -1
        self.game = game
        self.our_turn = False
        self.did_generate_question = False
        self.dice_roll = 0
        self.did_roll = False
        self.did_answer = False
        self.answers = []           # holds the current answers the player can choose from
        self.pos = Position(0, 0, 0)
        self.name = ""
        self.isAI = False
        self.isMP = False
        self.did_choose_row = False
        self.moves_left = 0
        self.score = 0  
        self.direction = None
        self.turn_start = 0
    def setindex(self, index):
        self.index = index
    def setpos(self, col, x, y):
        self.pos = Position(col, x, y)
    def setname(self, name):
        self.name = name
    def setai(self, ai):
        self.isAI = ai
    def setmp(self, mp):
        self.isMP = mp
    def load(self, row):
        self.name = row["name"]
        self.our_turn = bool(row["ourturn"])
        self.pos = Position(row["poscol"], row["posx"], row["posy"])
        self.did_generate_question = False # bool(row["did_generate_question"])
        self.dice_roll = row["dice_roll"]
        self.did_answer = bool(row["did_answer"])
        self.isAI = bool(row["isAI"])
        self.did_choose_row = bool(row["did_choose_row"])
        self.moves_left = row["moves_left"]
        self.score = row["score"]
        pass
    def set_direction(self,dir):
        self.direction = dir
    # save current player to file
    def save(self, sid):

        # query data
        cols = "(sid, name, ourturn, posx, posy, poscol, did_generate_question, dice_roll, did_answer, isAI, did_choose_row, moves_left, score)"
        vals = "('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
            sid, self.name, int(self.our_turn), self.pos.x, self.pos.y, self.pos.col, int(self.did_generate_question), self.dice_roll, int(self.did_answer),
            int(self.isAI), int(self.did_choose_row), self.moves_left, self.score)

        # execute query
        database.execute_query("INSERT INTO savegames_player " + cols + " VALUES " + vals)

    # player movement funcs
    def go_left(self):
        self.moves_left -= 1
        if self.pos.y > 9:
            if self.pos.col != 1:
                self.pos.col -= 1
            else:
                self.pos.col = 4
        elif self.pos.get_col() == 1 and self.pos.get_x() == 0:
            self.pos.col = 4
            self.pos.x = 1
        elif self.pos.x == 0:
            self.pos.col -= 1
            self.pos.x = 1
        else:
            self.pos.x -= 1

        if not self.isMP and not self.moves_left:
            for player in self.game.players:
                if self.pos.get_pos() == player.pos.get_pos() and player != self:
                    player.move_down(6)
            self.direction = None
            self.game.set_next_player()
        if self.isMP and not self.moves_left:
            #for player in self.game.players:
            #    if self.pos.get_pos() == player.pos.get_pos() and player != self:
            #        game.sockets.send(Packet("throwdown:{}:6".format(plr.index)).get())
            return

    def go_right(self):
        self.moves_left -= 1
        if self.pos.y > 9:
            if self.pos.col != 4:
                self.pos.col += 1
            else:
                self.pos.col = 1
        elif self.pos.get_col() == 4 and self.pos.get_x() == 1:
            self.pos.col = 1
            self.pos.x = 0
        elif self.pos.x == 1:
            self.pos.col += 1
            self.pos.x = 0
        else:
            self.pos.x += 1

        if not self.isMP and not self.moves_left:
            for player in self.game.players:
                if self.pos.get_pos() == player.pos.get_pos() and player != self:
                    player.move_down(6)
            self.direction = None
            self.game.set_next_player()
        if self.isMP and not self.moves_left:
            #for player in self.game.players:
            #    if self.pos.get_pos() == player.pos.get_pos() and player != self:
            #        game.sockets.send(Packet("throwdown:{}:6".format(plr.index)).get())
            return

    def go_up(self):
        self.moves_left -= 1

        if self.isMP and not self.moves_left:
            #for player in self.game.players:
            #    if self.pos.get_pos() == player.pos.get_pos() and player != self:
            #        game.sockets.send(Packet("throwdown:{}:6".format(plr.index)).get())
            return

        self.pos.y += 1
        if self.pos.x == 1 and self.pos.y == 10:
            self.pos.x = 0

        if not self.isMP and not self.moves_left:
            for player in self.game.players:
                if self.pos.get_pos() == player.pos.get_pos() and player != self:
                    player.move_down(6)
            self.direction = None
            self.game.set_next_player()

        if self.pos.y > 14:
            # increment own win
            score.increment_wins(self.name)

            # increment other players loses
            for x in self.game.players:
                if x is not self:
                    score.increment_loses(x.name)

            # show end screen
            self.game.winner = self.name
            self.game.set_state(3)

    def go_down(self):
        self.moves_left -= 1
        if not self.isMP and not self.moves_left:
            self.direction = None
            self.game.set_next_player()
        if self.isMP and not self.moves_left:
            return

        if self.pos.y > 0:
            self.pos.y -= 1

    def move_down(self, steps):
        if not self.isMP and not self.moves_left:
            for x in range(steps):
                if self.pos.y > 0:
                    self.pos.y -= 1
        if self.isMP and not self.moves_left:
            return

    # player draw func
    def draw(self):
        if not self.pos.col == 0:
            # player coordinates
            xpos = row_xoff[self.pos.col - 1] + row_xoff_s[self.pos.x]
            ypos = (480 - (self.pos.y * 27))
            if self.pos.y > 9:
                xpos += 18

            # draw player name
            font = pygame.font.Font(None, 20)
            if not self.our_turn:
                playername = font.render(self.name, 1, (0,0,0))
            else:
                playername = font.render(self.name, 1, (255,255,255))
            size = font.size(self.name)

            # draw player
            if not self.isMP:
                for x in range(self.game.playercount):
                    if self.game.players[x] == self:
                        if x == 0:
                             icon1 = pygame.image.load("assets/img/13.png")
                             self.game.screen.blit(icon1,(xpos - 10,ypos - 10))
                        if x == 1:
                             icon2 = pygame.image.load("assets/img/4.png")
                             self.game.screen.blit(icon2,(xpos - 10,ypos - 10))
                        if x == 2:
                             icon3 = pygame.image.load("assets/img/6.png")
                             self.game.screen.blit(icon3,(xpos - 10,ypos - 10))
                        if x == 3:
                             icon4 = pygame.image.load("assets/img/7.png")
                             self.game.screen.blit(icon4,(xpos - 10,ypos - 10))
            else:
                if self.index == 0:
                    icon1 = pygame.image.load("assets/img/13.png")
                    self.game.screen.blit(icon1,(xpos - 10,ypos - 10))
                if self.index == 1:
                    icon2 = pygame.image.load("assets/img/4.png")
                    self.game.screen.blit(icon2,(xpos - 10,ypos - 10))
                if self.index == 2:
                    icon3 = pygame.image.load("assets/img/6.png")
                    self.game.screen.blit(icon3,(xpos - 10,ypos - 10))
                if self.index == 3:
                    icon4 = pygame.image.load("assets/img/7.png")
                    self.game.screen.blit(icon4,(xpos - 10,ypos - 10))

            self.game.screen.blit(playername, (xpos - size[0]/2, ypos - 22))

