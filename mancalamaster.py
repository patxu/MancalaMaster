"""
Author: Patrick Xu and Jie Xu
"""

import string

class mancala:
  def __init__(self):
    """create a blank board"""
    self.board = {'0': 0, '1': 4, '2': 4, '3': 4, '4': 4, '5': 4, '6': 4,
                    '7': 0, '8': 4, '9': 4, '10': 4, '11': 4, '12': 4, '13': 4}

  """setup the game"""
  def setup():
    """options"""
    print

  def printBoard(self):
    print "\n\t", 
    for x in range(1,7): print self.board[str(7-x)],
    print ""
    print self.board['7'], "\t\t\t   ", self.board['0']
    print "\t",
    for x in range(1,7): print self.board[str(x+7)], 
    print "\n"

  """takes in the current player number as an argument"""
  def getMove(self, playerNum):
    print "It's player" + str(playerNum+1) + "'s turn!"

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
        print "Please enter a position between {0} and {1}.\n".format(moveLower, moveUpper)
    self.executeMove(move)
  
  """given a position on the board to be moved, make that move"""
  def executeMove(self, move):
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

      """check if the last seed is being placed into an empty pit on our side"""
      if x == val and self.board[str(current)] == 0:
        if move < 7:
          self.board['7'] += 1 + self.board[str(14-current)]
          self.board[str(14-current)] = 0
        elif move > 7:
          self.board['0'] += 1 + self.board[str(14-current)]
          self.board[str(14-current)] = 0
        x += 1
        continue

      """add one to the pit"""
      self.board[str(current)] += 1
      x += 1


  """check that both players have pieces left"""
  def gameOver(self):
    for x in range(1,7):
      current = str(x)
      if self.board[current] != 0: return False 
    return True
    for x in range(8,14):
      current = str(x)
      if self.board[current] != 0: return False 
    return True

  def getWinner(self):
    scoreOne = 0
    scoreTwo = 0

    """sum scores"""
    for x in range(1, 8): scoreOne += self.board[str(x)]
    for x in range(8, 14): scoreTwo += self.board[str(x%14)]

    print "The final score is", scoreOne, "to", scoreTwo, "-",
    if scoreOne > scoreTwo: print "player one wins!"
    elif scoreOne < scoreTwo: print "player two wins!"
    else: print "it's a tie!"

if __name__ == '__main__':

  game = mancala()
  game.setup()
  game.printBoard()
  turnNum = 0
  while game.gameOver() == False:
    game.getMove(turnNum%2)
    game.printBoard()
    turnNum += 1
  game.getWinner()
