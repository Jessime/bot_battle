# -*- coding: utf-8 -*-
"""
Created on Sat Aug 22 21:19:10 2015

@author: JMK
"""
import numpy as np

board = self.state
    
def main(board):
    def choice_1(board, directions, player_num):
        for y, array in enumerate(board):
            for x, element in enumerate(array):            
                if element == 0:
                    for d in directions.values():
                        for i in xrange(1,8):
                            row = y + i*d[0]
                            col = x + i*d[1]
                            if 0 <= row <= 7 and 0 <= col <= 7:
                                check = board[row][col]
                                if check == 0:
                                    break
                                elif i == 1 and check == player_num:
                                    break
                                elif i != 1 and check == player_num:
                                    board[y][x] = player_num
                                    return board
                            else:
                                break
        return board    
    
    def choice_2(board, directions, player_num):
        playable = np.zeros(board.shape, dtype=bool)
        for y, array in enumerate(board):
            for x, element in enumerate(array):
                if element == 0:
                    for d in directions.values():
                        for i in xrange(1,8):
                            row = y + i*d[0]
                            col = x + i*d[1]
                            if 0 <= row <= 7 and 0 <= col <= 7:
                                check = board[row][col]
                                if check == 0:
                                    break
                                elif i == 1 and check == player_num:
                                    break
                                elif i != 1 and check == player_num:
                                    playable[y][x] = True
                            else:
                                break
        play_spots = np.where(playable)
        play_spots = zip(play_spots[0], play_spots[1])
        max_play_spot = np.argmax([sum(i) for i in play_spots])
        max_play_spot = play_spots[max_play_spot]
        board[max_play_spot] = player_num
        return board
    
    directions = {"up-left": [-1,-1],
                  "up": [-1,0],
                  "up-right": [-1, 1],
                  "right": [0,1],
                  "down-right": [1,1],
                  "down": [1, 0],
                  "down-left": [1,-1],
                  "left": [0,-1]}    
    player_num = 1
    choice = np.random.choice([True, False])
    if choice:
        board = choice_1(board, directions, player_num)
    else:
        board = choice_2(board, directions, player_num)
    return board

self.state = main(board)