# Bot Battle

## reversi_battle.py

is a variation on the standard Reversi/Othello board game which aims to encourage quick coding. While quick writing code often isn't ideal, it's sometimes desirable to just get a working prototype up and running as quickly as possible.

Instead of playing a single game laying down piece-by-piece players write scripts to play a full game for them. The two bots will face off until one crashes or wins by standard Reversi rules. After a single game, script pauses and allows the players time to make the appropriate changes to their bots. Another game is played and the cycle repeats until one of the two players wins five games. Once five games have been won, the "Series" is over and an overall winner is declared.

I didn't bother to include a timer in the game. Players can figure out how to best handle that themselves, but some flexibility should probably be allowed.

Here's a link to a [blog post and video demonstration](http://what-is-bioinformatics.blogspot.com/2015/08/bot-battle.html).

## practice_bot.py and practice_bot2.py
are trivial examples of bots, but show how a script should be set up to interact with reversi_battle.py. The game exposes the board to each player's bot as a numpy array filled with 0's for empty spaces, and 1's and 2's for spots currently occupied by Player 1 and 2, respectively. The the script, no matter the complexity, should basically, take the current board as input, and output a new board when one of the player's pieces has been played in a valid spot (i.e. a 1 or a 2 has replaced one of the 0s). 

These particular bots simply scans for a valid position to play and plays in the first spot it comes across.

## practice_bot3.py and practice_bot4.py
are slightly more complicated, but no more strategically sound. These bots take one of two actions at random. They either copy the original bots and just play in the first available spot, or they scan all valid spots and play the spot that has the largest sum of indices (i.e. if the bottom right corner [7,7] were available, it would be chosen since it gets a score of 14).

These bots are slightly more useful for their ability to make a 2D array of all valid spots during a particular play. All higher level decision making written in will depend on this new array.

## graphics.py

is a light weight wrapper around Tkinker. It was developed by John Zelle and can also be downloaded from http://mcsp.wartburg.edu/zelle/python/graphics.py

## Version and Dependencies

Python 2.7

Numpy 1.9.2 (or similar)

The Anaconda distribution is the recommend method for obtaining numpy if necessary.
