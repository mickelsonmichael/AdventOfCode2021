class Column:
  def __init__(self, value):
    self.value = value.strip("\n")
    self.marked = False

  def mark(self):
    self.marked = True

  def toString(self):
    return " *" if self.marked else self.value.rjust(2, " ")

  def createColumns(row):
    values = filter(lambda x : x != "", row.split(" "))
    return map(Column, values)

class Board:
  def __init__(self):
    self.rows = []

  def addRow(self, row):
    cols = []
    
    for col in Column.createColumns(row):
      cols.append(col)

    self.rows.append(cols)
  
  def print(self):
    for row in self.rows:
      padded = map(lambda col : col.toString(), row)
      print(" ".join(padded))

  def isWon(self):
    columns = len(self.rows[0])
    colStars = [0] * columns

    for row in self.rows:
      isRowWin = True
      for i in range(0, len(row)):
        colStars[i] = colStars[i] + (1 if row[i].marked == True else 0)
        isRowWin = row[i].marked and isRowWin
      
      if isRowWin:
        return True

    for colStar in colStars:
      if colStar == columns:
        return True

    return False

  def mark(self, n):
    for row in self.rows:
      for col in row:
        if col.value == n:
          col.mark()

    return self.isWon()

  def sumUnmarked(self):
    sum = 0
    for row in self.rows:
      for col in filter(lambda c : not c.marked, row):
        sum += int(col.value)

    return sum