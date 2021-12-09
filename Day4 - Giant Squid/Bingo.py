from Board import Board

class Bingo:

  def __init__(self, filename):
    self.filename = filename
    self.boards = []
    
    with open(filename) as file:
      self.draws = file.readline().split(",")

      # skip blank
      file.readline()
      
      board = Board()
      while True:
        line = next(file, None)

        if (line == None):
          self.boards.append(board)
          break
        elif line == "\n" or line == "":
          self.boards.append(board)
          board = Board()
          continue

        board.addRow(line)

  def play(self):
    for draw in self.draws:
      for board in self.boards:
        if board.mark(draw):
          # board has won
          print("\nWinner!")
          board.print()
          print("Final score:", str(board.sumUnmarked() * int(draw)))
          return board

  def takeADive(self):
    boardsRemaining = self.boards.copy()
    for draw in self.draws:
        for i in range(len(boardsRemaining) -1, -1, -1):
            if boardsRemaining[i].mark(draw):
                if len(boardsRemaining) > 1:
                    boardsRemaining.remove(boardsRemaining[i])
                else:
                    print("\nLoser!")
                    boardsRemaining[0].print()
                    print("Final score:", str(boardsRemaining[0].sumUnmarked() * int(draw)))
                    return


  def print(self):
    for n in range(0, len(self.boards)):
      print("Board " + str(n + 1))
      self.boards[n].print()
