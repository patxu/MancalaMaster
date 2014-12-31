"""
Author: Patrick Xu and Jie Xu
"""

import os
import copy

class mancala:
  def __init__(self):
    """create a blank board"""
    self.board = {'0': 0, '1': 4, '2': 4, '3': 4, '4': 4, '5': 4, '6': 4,
                    '7': 0, '8': 4, '9': 4, '10': 4, '11': 4, '12': 4, '13': 4}
    self.moveLog = []

  """setup the game"""
  def setup(self):
    os.system("clear")
    
    while True:
      """options"""
      options = open("gamefiles/options", "r")
      print options.read()

      while True:
        try:
          selection = raw_input("Choice: ")
          if selection not in ("q","r","h"): raise ValueError
          else: break
        except (NameError, ValueError):
          print "Please enter a valid option."
      if selection == "q":
        self.players = ["player1", "player2"]
        return
      elif selection == "r":
        player1 = raw_input("Enter name of player 1: ")
        player2 = raw_input("Enter name of player 2: ")
        self.players = [player1, player2]
        return
      elif selection == "h":
        help = open("gamefiles/help", "r")
        print help.read()
        raw_input("[Enter] to continue: ")

  def printBoard(self):
    os.system("clear")
    for x in range(2): print "\n"
    print "Past Moves (max: 10)"
    for x,y in enumerate(self.moveLog):
      if x >= len(self.moveLog) - 10:
        print y
    for x in range(max(10-len(self.moveLog), 0) + 2): print ""
    print "\t", 
    for x in range(1,7): print self.board[str(7-x)],
    print ""
    print self.board['7'], "\t\t\t   ", self.board['0']
    print "\t",
    for x in range(1,7): print self.board[str(x+7)], 
    print "\n"

  """takes in the current player number as an argument"""
  def getMove(self, playerNum):
    print "It's " + self.players[playerNum] + "'s turn!"

    """get player's move"""
    if playerNum == 0:
      """get upper and lower bound on valid moves based on current player"""
      moveLower = 1 + 7*playerNum
      moveUpper = 6 + 7*playerNum

      """get valid user input"""
      while True: 
        try:
          move = int(input("Enter a position to move: "))
          if move < moveLower or move > moveUpper:
            raise ValueError
          break
        except (NameError, SyntaxError, ValueError):
          print "Please enter a move between {0} and {1}.\n".format(moveLower, moveUpper)
      self.moveLog.append("Player: {0}".format(move))

    elif playerNum == 1: move = self.getAIMove()

    return move

  """get the best AI move"""
  def getAIMove(self):
    bestMove = self.findBestMove()
    print "The AI's move is", bestMove
    self.moveLog.append("AI: {0}".format(bestMove))
    return bestMove

  """implements the algorithm to determine the best AI move"""
  def findBestMove(self):

    """naive, depth 1 score maximizer"""
    bestMove = 8
    bestVal = 0
    for current in range(8,14):
      tempGame = mancala()
      tempGame.board = copy.deepcopy(self.board)
      tempGame.executeMove(current)
      if tempGame.board['0'] > bestVal: 
        bestMove = current
        bestVal = tempGame.board['0']
    return bestMove
    
  """given a position on the board to be moved, make that move"""
  def executeMove(self, move):
    anotherTurn = False
    val = self.board[str(move)]
    self.board[str(move)] = 0
    x = 1
    while x < val + 1:
      """get the pit to place a seed into"""
      current = (move + x) % 14
      """check if we would be placing into opponent's end pit"""
      if move < 7 and current == 0:
        val += 1
        x += 1
        continue
      if move > 7 and current == 7:
        val += 1
        x += 1
        continue

      """check if the last seed is being placed into an empty pit on our side
         or if the last seed is being placed into our end pit"""
      if x == val:
        if self.board[str(current)] == 0:
          """player steals from opponent"""
          if move < 7 and current < 7: 
            self.board['7'] += 1 + self.board[str(14-current)]
            self.board[str(14-current)] = 0
          elif move > 7 and current > 7: 
            self.board['0'] += 1 + self.board[str(14-current)]
            self.board[str(14-current)] = 0
          x += 1
          if 0 < current < 7 and move < 7:
            self.board[str(current)] += -1
          if 7 < current < 14 and move > 7:
            self.board[str(current)] += -1

        """player gets another turn"""
        if move < 7 and current == 7: 
          anotherTurn = True
        elif move > 7 and current == 0: 
          anotherTurn = True

      """add one to the pit"""
      self.board[str(current)] += 1
      x += 1
      
    return anotherTurn

  """check that both players have pieces left"""
  def gameOver(self):
    for x in range(1,7):
      current = str(x)
      if self.board[current] != 0: return False 
    for x in range(8,14):
      current = str(x)
      if self.board[current] != 0: return False 
    return True

  def getWinner(self):
    scoreOne = 0
    scoreTwo = 0

    """sum scores"""
    for x in range(1, 8): scoreOne += self.board[str(x)]
    for x in range(8, 15): scoreTwo += self.board[str(x%14)]

    print "The final score is", scoreOne, "to", scoreTwo, "-",
    if scoreOne > scoreTwo: print "player one wins!"
    elif scoreOne < scoreTwo: print "player two wins!"
    else: print "it's a tie!"

if __name__ == '__main__':

  game = mancala()
  game.setup()
  game.printBoard()
  currentPlayer= 0
  while game.gameOver() == False:
    move = game.getMove(currentPlayer%2)
    """true means the same player gets another turn"""
    if game.executeMove(move) == True: 
      currentPlayer += -1
    game.printBoard()
    currentPlayer += 1
  game.getWinner()
