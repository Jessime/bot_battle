# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 21:13:59 2015

@author: JMK
"""

import graphics
import numpy as np
from time import sleep

class Player():
    def __init__(self, num):
        self.num = num
        self.name = raw_input("What is your name, Player {}? ".format(self.num))
        self.bot_loc = raw_input("Where is your bot script located? ")
        self.points = 0
        self.state = None
    
    def play(self):
        try:
            execfile(self.bot_loc)
            print self.num
#            print self.state
            print ""
        except IOError:
            print "The file couldn't be read. {} loses.".format(self.name)
            
class Board():
    """Each game is played on an 8x8 board which is updated throughout the game"""
    def __init__(self):
        self.state = self.init_state()
        self.win = graphics.GraphWin("Othello Code Battle", 802, 802)
        self.boxes = self.init_boxes()
        self.directions = {"up-left": [-1,-1],
                           "up": [-1,0],
                           "up-right": [-1, 1],
                           "right": [0,1],
                           "down-right": [1,1],
                           "down": [1, 0],
                           "down-left": [1,-1],
                           "left": [0,-1]}
    def init_state(self):
        """Set up the initial state of the board"""
        state = np.zeros([8,8])
        state[3][3] = 2
        state[3][4] = 1
        state[4][3] = 1
        state[4][4] = 2
        return state
    
    def init_boxes(self):
        """Initialize the graphic representation of the board"""
        boxes = []
        for i in xrange(8):
            boxes.append([])
            for j in xrange(8):
                point1 = graphics.Point(j*100+2, i*100+2)
                point2 = graphics.Point(j*100+102, i*100+102)
                rec = graphics.Rectangle(point1,point2)
                boxes[-1].append(rec)
        return boxes
    
    def init_drawing(self):
        """Draw the original state of the board"""
        for i, row in enumerate(self.boxes):
            for j, box in enumerate(row):
                self.refill(i, j, box)
                box.draw(self.win)

    def refill(self, i, j, box):
        """Set the fill of the boxes based on the current values of the board"""
        tile_owner = self.state[i][j]
        if tile_owner == 1:
            box.setFill("black")
        elif tile_owner == 2:
            box.setFill("yellow")
            
    def update_color(self):
        """Render a drawing of the board"""
        for i, row in enumerate(self.boxes):
            for j, box in enumerate(row):
                self.refill(i, j, box)        
    
class Game():
    """A single game is played between two players until someone crashes or wins"""
    def __init__(self):
        self.p1 = Player(1)
        self.p2 = Player(2)
        self.board = Board()
        self.running = True
        self.valid_play = True
        self.turn = 1
        self.play_loc = None
        
    def run(self):
        """Main loop of the game"""
        c = 0
        self.board.init_drawing()
        while self.running:
            sleep(3)
            if c == 15:
                break
            self.take_turn()
            self.update()
            self.board.win.flush()
            #self.running = False
            c += 1
        self.board.win.getMouse()
        self.board.win.close()

    def take_turn(self):
        """Check whose turn it is and run that player's bot"""
        if self.turn == 1:
            self.p1.state = np.copy(self.board.state)
            self.p1.play()
        else:
            self.p2.state = np.copy(self.board.state)
            self.p2.play()

    def update(self):
        """Update the state of the game"""
        if self.turn == 1:
            new_board = self.p1.state
        else:
            new_board = self.p2.state
        self.validate_play(new_board)
#        print self.valid_play
        if self.valid_play:
            self.update_state(new_board)
            self.board.update_color()
#            print "hi"
            self.change_turn()
        else:
            pass
        
    def validate_play(self, new):
        """Decide if play proposed last turn is a legal move"""
        self.basic_checks(new)
        if self.valid_play:
            self.position_check(new)

    def basic_checks(self, new):
        """Check to make sure the board hasn't been messed with, 
        that all the spots are 0,1,2, and that only one value as been changed."""
        print new
#        print ""
#        print self.board.state
#        print self.board.state is new
        try:
            play_loc = np.where(new != self.board.state)
#            print play_loc
#            print new.shape
#            print np.sum(new)
            if new.shape != (8, 8): 
                print "The board is no longer an 8x8 numpy array"
                self.valid_play = False
            if np.sum(new) != np.sum(self.board.state) + self.turn:
                print "The sum state of the board has not increased by the Player number."
                self.valid_play = False
            if len(play_loc[0]) != 1:
                print "More than 1 element has been changed"
                self.valid_play = False
            if np.sum((new >= 0) & (new <=2)) != 64:
                print "The elements of the board are no longer 0,1,2"
                self.valid_play = False
            else:
                self.play_loc = [play_loc[0][0], play_loc[1][0]]
        except Exception, e:
            print e
            self.valid_play = False

    def position_check(self, new):
        self.valid_play = False #Until proven otherwise
        for d in self.board.directions:
            d = self.board.directions[d]
            for i in xrange(1,8):
                row = self.play_loc[0] + i*d[0]
                col = self.play_loc[1] + i*d[1]
                try:
                    check = new[row][col]
                    if check == 0:
                        break
                    elif check == self.turn:
                        self.valid_play = True
                except IndexError:
                    break
                
        if self.valid_play == False:
            print "Error with play.\n\n"
            print new
            if self.turn == 1:
                print "The play made by {} was not valid. {} wins this game.".format(self.p1.name, self.p2.name)
            else:
                print "The play made by {} was not valid. {} wins this game.".format(self.p2.name, self.p1.name)
#        print "pos", self.valid_play
        
    def update_state(self, new):
        """Logic for flipping over pieces when new piece is played"""
        for d in self.board.directions:
#            print ""
#            print ""
#            print d, self.board.directions[d]
            d = self.board.directions[d]
            for i in xrange(1,8):
                
                #Walk out from the play location looking for a matching piece
                row = self.play_loc[0] + i*d[0]
                col = self.play_loc[1] + i*d[1]
#                print self.play_loc[0], i, d[0]
#                print "R, C", row, col
                try:
                    check = new[row][col]
#                    print "check", check
                    #If square is empy, quit checking this direction
                    if check == 0:
                        break
                    
                    #If square matches, traceback
                    #flip as you go back to the original play square
                    elif check == self.turn:
#                        print "match"
                        reverse_d = [-1*x for x in d]
                        for i_ in xrange(8):
                            row_ = i_*reverse_d[0]
                            col_ = i_*reverse_d[1]
                            if ((row+row_) == self.play_loc[0] and 
                                (col+col_) == self.play_loc[1]):
#                                print "R_ C_", row_, col_
                                break
                            else:
                                new[row+row_][col+col_] = self.turn
                                
                #If you check past the edge, quit looking in this direction
                except IndexError:
                    break
                
        self.board.state = new
#        print self.board.state
    
    def change_turn(self):
        """Change who's turn it is to play."""
        if self.turn == 1:
            self.turn = 2
        else:
            self.turn = 1

if __name__ == "__main__":
    game = Game()
    game.run()