# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 21:13:59 2015

@author: Jessime Kirk
"""

import graphics
import numpy as np
from time import sleep

class Player():
    def __init__(self):
        self.name = raw_input("What is your name, Player? ")
        self.bot_loc = raw_input("Where is your bot script located? ")
        self.game_points = 0
        self.series_points = 0
        self.state = None
    
    def play(self):
        """Try executing player bot. 
        Any crashes inside the bot will be reported but not crash the game.
        The player will lose a game when they fail the basic_checks."""
        try:
            execfile(self.bot_loc)
        except Exception, e:
            print e
            
class Board():
    """Each game is played on an 8x8 board which is updated throughout the game"""
    def __init__(self):
        self.state = self.init_state()
        self.win = graphics.GraphWin("Othello Code Battle", 1002, 802)
        self.boxes = self.init_boxes()
        self.game_points = [None, None]
        self.series_points = [None, None]
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
            box.setFill("blue")
            self.win.flush()
        elif tile_owner == 2:
            box.setFill("red")
            self.win.flush()
        else:
            box.setFill("white")
            
    def update_color(self):
        """Render a drawing of the board"""
        for i, row in enumerate(self.boxes):
            for j, box in enumerate(row):
                self.refill(i, j, box)
                
    def update_game_points(self, p1, p2):
        """Draw the current points for each player this turn"""
        self.game_points[0].setText(p1.game_points)
        self.game_points[1].setText(p2.game_points)

    def update_series_points(self, p1, p2):
        """Draw the current points for the series"""
        self.series_points[0].setText(p1.series_points)
        self.series_points[1].setText(p2.series_points)
        
    def init_data(self, p1, p2):
        """Draw all of the static information for the game"""
        p1_letter = "P1:  {}".format(p1.name[0].upper())
        p2_letter = "P2:  {}".format(p2.name[0].upper())
        p1_letter = graphics.Text(graphics.Point(900,50), p1_letter)
        p2_letter = graphics.Text(graphics.Point(900,450), p2_letter)
        p1_letter.setSize(35)
        p2_letter.setSize(35)
        p1_letter.setFill("blue")
        p2_letter.setFill("red")
        p1_letter.draw(self.win)             
        p2_letter.draw(self.win)
        
        p1_series1 = graphics.Text(graphics.Point(900, 125), "Series Points:")
        p2_series1 = graphics.Text(graphics.Point(900, 525), "Series Points:")
        p1_series1.setSize(20)
        p2_series1.setSize(20)
        p1_series1.setFill("blue")
        p2_series1.setFill("red")
        p1_series1.draw(self.win)
        p2_series1.draw(self.win)
        
        self.series_points[0] = graphics.Text(graphics.Point(900, 160), str(p1.series_points))
        self.series_points[1] = graphics.Text(graphics.Point(900, 560), str(p2.series_points))
        self.series_points[0].setSize(30)
        self.series_points[1].setSize(30)
        self.series_points[0].setFill("blue")
        self.series_points[1].setFill("red")
        self.series_points[0].draw(self.win)
        self.series_points[1].draw(self.win)        
        
        p1_game1 = graphics.Text(graphics.Point(900, 225), "Game Points:")
        p2_game1 = graphics.Text(graphics.Point(900, 625), "Game Points:")
        p1_game1.setSize(20)
        p2_game1.setSize(20)
        p1_game1.setFill("blue")
        p2_game1.setFill("red")
        p1_game1.draw(self.win)
        p2_game1.draw(self.win)

        self.game_points[0] = graphics.Text(graphics.Point(900, 260), "2")
        self.game_points[1] = graphics.Text(graphics.Point(900, 660), "2")
        self.game_points[0].setSize(30)
        self.game_points[1].setSize(30)
        self.game_points[0].setFill("blue")
        self.game_points[1].setFill("red")
        self.game_points[0].draw(self.win)
        self.game_points[1].draw(self.win)
        
    def total_refresh(self, p1, p2):
        "Wrapper for updating the board"""
        self.update_series_points(p1, p2)
        self.state = self.init_state()
        self.update_color()
        self.win.flush()
        
class Game():
    """A single game is played between two players until someone crashes or wins.
    Games are wrapped by a Series of (usually) 5 games."""
    def __init__(self, player1, player2, board, count):
        self.p = {1: player1, 2: player2}
        self.board = board
        self.game_num = count
        self.valid_play = True
        self.turn = 1
        self.not_turn = 2
        self.play_loc = None
        self.winner = None
        self.loser = None
        self.series_over = False
        self.end_flags = {"Possible": [True,""],
                          "Board": [True,"The board is no longer an 8x8 numpy array"],
                          "Sum State": [True,"The sum state of the board has not increased by the Player number."],
                          "1 Element": [True,"More or less than 1 element has been changed"],
                          "0-2": [True, "The elements of the board are no longer 0,1,2"],
                          "Position": [True, "The play was not made at a valid position"]}
                          
    def run(self, delay):
        """Loop of a single game"""
        print "\nWelcome, players! Good luck to you and your bot."
        print "Launching Game {}...\n".format(self.game_num)
        self.board.total_refresh(self.p[1], self.p[2])
        while not self.winner:
            sleep(delay)
            self.check_playability()
            if not self.winner:
                self.take_turn()
                self.update()
                self.board.win.flush()
                print self.board.state
                print ""
        return self.winner                
    
    def check_playability(self):
        """Make sure there's the possibility for a valid play before running a bot.
        If the next player doesn't have a place to play, 
        check if the player that just played can go again. 
        If they can't, and there are no spots left for anyone to go, end the game."""
        try_repeat = self.playability(self.turn)
        if try_repeat:
            end_game = self.playability(self.not_turn)
            if not end_game:
                print "There are no valid plays for {}.".format(self.p[self.turn].name)
                print "So {} will get to go again.".format(self.p[self.not_turn].name)
                self.turn, self.not_turn = self.not_turn, self.turn
            
    def playability(self, expected):
        """Core logic for checking the validity of plays,
        and decisions about what to do if there isn't a viable play.
        If there are no valid plays for either player, call winner_by_points."""
        #Check if each space is valid
        for y, array in enumerate(self.board.state):
            for x, element in enumerate(array):
                
                #Continue if space is empty
                if element == 0:
                    #Look in each direction
                    for d in self.board.directions.values():
                        #For as far as the board extends, if necessary
                        for i in xrange(1,8):
                            #Try checking to see if the next space in the direction looks valid
                            row = y + i*d[0]
                            col = x + i*d[1]
                            if 0 <= row <= 7 and 0 <= col <= 7:
                                #If you aren't out of bounds, get the value of the space
                                check = self.board.state[row][col]
                                #It's not valid if the next space is empty
                                if check == 0:
                                    break
                                #It's not valid if the next space is mine
                                elif i == 1 and check == expected:
                                    break
                                #If there's at least 1 of the opposite pieces in a sandwich,
                                #then the play is valid
                                elif i != 1 and check == expected:
                                    return False
                            else:
                                break
        #If no viable spot was found, decide whether to check other player or end game
        if expected == self.turn:
            return True
        else:
            self.end_flags["Possible"][0] = False
            self.winner_by_points()
            if self.series_over:
                return True
        
    def take_turn(self):
        """Check whose turn it is and run that player's bot"""
        self.p[self.turn].state = np.copy(self.board.state)
        self.p[self.turn].play()

    def update(self):
        """Update the state of the game if the play proposed by the bot is valid.
        The pieces on the boared, the player points, the visuals,
        and the turn all need to be changed."""
        new_board = self.p[self.turn].state
        self.validate_play(new_board)

        if self.valid_play:
            self.update_state(new_board)
            self.p[1].game_points = np.sum(self.board.state == 1)
            self.p[2].game_points = np.sum(self.board.state == 2)
            self.board.update_game_points(self.p[1], self.p[2])
            self.board.update_color()
            self.turn, self.not_turn = self.not_turn, self.turn
        else:
            self.winner = self.p[self.not_turn]
            
    def validate_play(self, new):
        """Decide if play proposed last turn is a legal move. This is a two-step
        process. If the proposed board doesn't pass basic checks (such as crashing),
        then there's no plint in checking if the position played was technically okay."""
        self.basic_checks(new)
        if self.valid_play:
            self.position_check(new)
            
    def basic_checks(self, new):
        """Check to make sure the board hasn't been messed with, 
        that all the spots are 0,1,2, and that only one value as been changed.
        Definitions of the errors can be found in self.end_flags.
        If a play fails these checks go to winner_by_mistake to end the game."""
        try:
            play_loc = np.where(new != self.board.state)

            if new.shape != (8, 8):
                self.end_flags["Board"][0] = False                
                self.valid_play = False

            if np.sum(new) != np.sum(self.board.state) + self.turn:
                self.end_flags["Sum State"][0] = False                
                self.valid_play = False

            if len(play_loc[0]) != 1:
                self.end_flags["1 Element"][0] = False                
                self.valid_play = False

            if np.sum((new >= 0) & (new <=2)) != 64:
                self.end_flags["0-2"][0] = False                
                self.valid_play = False

            else:
                self.play_loc = [play_loc[0][0], play_loc[1][0]]
        except Exception, e:
            print e
            self.valid_play = False
            
        if self.valid_play == False:
            self.winner_by_mistake()

    def position_check(self, new):
        """Logic for seeing if a play is technically valid. The basic idea is to
        find one instance of a sandwich of the other player's piece between two
        of the current player's pieces."""
        #Assume the play is bad until proven otherwise
        self.valid_play = False
        #Look in each direction
        for d in self.board.directions.values():
            #For as far as the board extends, if necessary
            for i in xrange(1,8):
                #Try checking to see if the next space in the direction looks valid
                row = self.play_loc[0] + i*d[0]
                col = self.play_loc[1] + i*d[1]
                if 0 <= row <= 7 and 0 <= col <= 7:
                    #If you aren't out of bounds, get the value of the space
                    check = new[row][col]
                    #It's not valid (in that direction) if the next space is empty
                    if check == 0:
                        break
                    #It's not valid (in that direction) if the next space is the same as the one played
                    elif i == 1 and check == self.turn:
                        break
                    #If there's at least 1 of the opposite pieces in a sandwich,
                    #then the play is valid
                    elif i != 1 and check == self.turn:
                        self.valid_play = True
                else:
                    break
                
        if self.valid_play == False:
            self.end_flags["Position"][0] = False
            self.winner_by_mistake()
        
    def update_state(self, new):
        """Logic for flipping over pieces when new piece is played.
        Once all of the checks have cleared, actually make changes to the game board."""
        for d in self.board.directions:
            d = self.board.directions[d]
            for i in xrange(1,8):
                
                #Walk out from the play location looking for a matching piece
                row = self.play_loc[0] + i*d[0]
                col = self.play_loc[1] + i*d[1]

                if 0 <= row <= 7 and 0 <= col <= 7:
                    check = new[row][col]
                    #If square is empy, quit checking this direction
                    if check == 0:
                        break
                    
                    #If square matches, traceback
                    #flip as you go back to the original play square
                    elif check == self.turn:
                        reverse_d = [-1*x for x in d]
                        for i_ in xrange(8):
                            row_ = i_*reverse_d[0]
                            col_ = i_*reverse_d[1]
                            if ((row+row_) == self.play_loc[0] and 
                                (col+col_) == self.play_loc[1]):
                                break
                            else:
                                new[row+row_][col+col_] = self.turn
                        break        
                #If you check past the edge, quit looking in this direction
                else:
                    break
                
        self.board.state = new
     
    def winner_by_points(self):
        """Decide who wins the game on the basis of points. 
        If there's a tie, still declare a winner as a signal to end the game.
        Call the winner "tie", which will start a new game."""
        if self.p[1].game_points > self.p[2].game_points:
            self.winner = self.p[1]
            self.loser = self.p[2]
        elif self.p[2].game_points > self.p[1].game_points:
            self.winner = self.p[2]
            self.loser = self.p[1]
        else:
            print "This game was a tie. Neither player recieves a point."
            self.winner = "tie"
            
        if np.sum(self.board.state == 0) != 0:
            print "There are no more valid moves."
        if self.winner and self.winner != "tie":
            print "{} wins this game with a score of {} to {}.".format(
            self.winner.name, self.winner.game_points, self.loser.game_points)
        self.end_game()
    
    def winner_by_mistake(self):
        """When one person makes an error, the other person wins.
        Show the proposed play compared to the last valid state of the board."""
        self.winner = self.p[self.not_turn]
        self.loser = self.p[self.turn]
        
        print "Error with play by {}".format(self.loser.name)
        print "Proposed State:"
        print self.loser.state
        print "Old State:"
        print self.board.state
        for e in self.end_flags.values():
            if e[0] == False:
                print e[1]
        print "{} wins this game.".format(self.winner.name)
        self.end_game()
        
    def end_game(self):
        """Print the state of the series and wait for mouse to end."""
        if self.winner and self.winner != "tie":
            print "The Series score is {}:{} and {}:{}\n".format(
            self.winner.name, self.winner.series_points+1, self.loser.name, self.loser.series_points) 
        else:
            print "The Series score is {}:{} and {}:{}\n".format(
            self.p[1].name, self.p[1].series_points, self.p[2].name, self.p[2].series_points)
        if self.p[1].series_points != (5-1) and self.p[2].series_points != (5-1): #(5-1) since the point hasn't actually been given yet.
            print "Get ready for Game {}.".format(self.game_num+1)
        else:
            self.series_over = True
        self.board.win.getMouse()

class Series():
    """A Series of Games are played until one Player wins 5 games"""
    def __init__(self):
        self.p1 = Player()
        self.p2 = Player()
        self.delay = 3
        self.board = Board()
        self.game = None
    
    def run(self):
        """Main loop of a Series of games."""
        count = 1
        self.board.init_drawing()
        self.board.init_data(self.p1, self.p2)
	self.board.win.getMouse()
        while self.p1.series_points != 5 and self.p2.series_points != 5:
            self.game = Game(self.p1, self.p2, self.board, count)
            winner = self.game.run(self.delay)
            if winner and winner != "tie":
                winner.series_points += 1
            count += 1
        self.end_series()
    
    def end_series(self):
        """Display who wins the series."""
        self.board.update_series_points(self.p1, self.p2)
        self.board.win.flush()
        print "Game Over"
        if self.p1.series_points == 5:
            print "Congratulations, {}. You've won this Series.".format(self.p1.name)
            self.draw_w(1)
        else:
            print "Congratulations, {}. You've won this Series.".format(self.p2.name)
            self.draw_w(2)
            
    def draw_w(self, num):
        fill = [(0,0), (0,1), (0,2), (0,5), (0,6), (0,7),
                (1,0), (1,7),
                (2,0), (2,7), 
                (3,0), (3,3), (3,4), (3,7),
                (4,0), (4,1), (4,3), (4,4), (4,6), (4,7),
                (5,1), (5,2), (5,5), (5,6),
                (6,1), (6,2), (6,5), (6,6),
                (7,2), (7,5),
                ]
        for y in xrange(8):
            for x in xrange(8):
                self.board.state[y][x] = num if (y, x) in fill else 0
                box = self.board.boxes[y][x]
                self.board.refill(y, x, box)
                sleep(.1)
                
        self.board.win.getMouse()
        self.board.win.close()  
        
if __name__ == "__main__":
    series = Series()
    series.run()
