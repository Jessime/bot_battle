# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 13:10:56 2015

@author: JMK
"""

"""
Your bot exists as the main function found below,
and whatever other edits you want to make to this script.
The current state of the game is stored here as a numpy array called "board".

Initial State of Board
[[ 0.  0.  0.  0.  0.  0.  0.  0.]
 [ 0.  0.  0.  0.  0.  0.  0.  0.]
 [ 0.  0.  0.  0.  0.  0.  0.  0.]
 [ 0.  0.  0.  2.  1.  0.  0.  0.]
 [ 0.  0.  0.  1.  2.  0.  0.  0.]
 [ 0.  0.  0.  0.  0.  0.  0.  0.]
 [ 0.  0.  0.  0.  0.  0.  0.  0.]
 [ 0.  0.  0.  0.  0.  0.  0.  0.]]

If you prefer to interact with traditional Python lists,
uncomment the statement "board = self.state.tolist". 

For each execution of the script,
your bot should decide to play a single "piece", 
represented by either a 1 or a 2 depending on your player number.
The play should be made by altering an element on the board,
before returning the board from main and exiting the script.

Basic rules and strategies can be found here:
http://www.samsoft.org.uk/reversi/strategy.htm
"""
board = self.state
#board = self.state.tolist


def main(board):
    directions = {"up-left": [-1,-1],
                  "up": [-1,0],
                  "up-right": [-1, 1],
                  "right": [0,1],
                  "down-right": [1,1],
                  "down": [1, 0],
                  "down-left": [1,-1],
                  "left": [0,-1]}
    
    player_num = 1
    
    #Check if each space is valid
    for y, array in enumerate(board):
        for x, element in enumerate(array):
            
            #Continue if space is empty
            if element == 0:
                #Look in each direction
                for d in directions.values():
                    #For as far as the board extends, if necessary
                    for i in xrange(1,8):
                        #Try checking to see if the next space in the direction looks valid
                        row = y + i*d[0]
                        col = x + i*d[1]
                        try:
                            #If you aren't out of bounds, get the value of the space
                            check = board[row][col]
                            #It's not valid if the next space is empty
                            if check == 0:
                                break
                            #It's not valid if the next space is mine
                            elif i == 1 and check == player_num:
                                break
                            #If there's at least 1 of the opposite pieces in a sandwich,
                            #then the play is valid
                            elif i != 1 and check == player_num:
                                board[y][x] = player_num
                                return board
                        except IndexError:
                            break

    return board

self.state = main(board)
    