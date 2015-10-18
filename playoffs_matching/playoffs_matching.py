from csv import reader
from lib.munkres import Munkres
from sys import argv

class PlayoffsMatching:
  def __init__(self):
    self.teams = []
    self.data = {}

  def yearToIndex(self, year):
    if (year > 1994):
      return 29 + year - self.lastYear
    else:
      return 30 + year - self.lastYear

  def indexToYear(self, index):
    if (index > 10):
      return index + self.lastYear - 29
    else:
      return index + self.lastYear - 30

  def populateData(self):
    with open('data/teams.csv', 'rb') as teamsCsv:
      read = reader(teamsCsv)
      for row in read:
        for item in row:
          self.teams.append(item)

    for team in self.teams:
      self.data[team] = [999 for x in range(30)]
      
    with open('data/playoffs_data.csv', 'rb') as dataCsv:
      read = reader(dataCsv)
      for row in read:
        year = int(row[0])
        yearIndex = self.yearToIndex(year)
        if year > self.lastYear or year < self.lastYear - 30:
          continue

        self.data[row[1]][yearIndex] = 0.01
        self.data[row[2]][yearIndex] = 1.01
        self.data[row[3]][yearIndex] = 2.01
        self.data[row[4]][yearIndex] = 2.01

        if len(row) > 5:
          self.data[row[5]][yearIndex] = 3.01
          self.data[row[6]][yearIndex] = 3.01
          self.data[row[7]][yearIndex] = 3.01
          self.data[row[7]][yearIndex] = 3.01
          
        if len(row) > 9:
          self.data[row[8]][yearIndex] = 4.01
          self.data[row[9]][yearIndex] = 4.01
    
  def dictToArray(self, dataMap):
    arr = [[0 for x in range(30)] for x in range(30)]
    for team in self.teams:
      arr[self.teams.index(team)] = dataMap[team]
    return arr

  def analyzeData(self):
    m = Munkres()
    matrix = self.dictToArray(self.data)
    changes = m.compute(matrix)
    self.printWinnerInfo(matrix, changes)
    
  def printWinnerInfo(self, matrix, changes):
    years = ['' for x in range(30)]
    modCounts = [0 for x in range(30)]
    totalModCount = 0
    for teamIndex, yearIndex in changes:
      team = self.teams[teamIndex]
      years[yearIndex] = team
      modCounts[yearIndex] = matrix[teamIndex][yearIndex]
      totalModCount += matrix[teamIndex][yearIndex]

    for yearIndex, team in enumerate(years):
      print '%d: %s - %d modifications' % (self.indexToYear(yearIndex), team, modCounts[yearIndex])
    print 'Total mod count is %d' % totalModCount

  def main(self):
    if len(argv) != 2:
      print 'Please run with ending year as arg'
    elif int(argv[1]) > 2014 or int(argv[1]) < 2008:
      print 'Please run with ending year between 2008 and 2014'
    else:
      self.lastYear = int(argv[1])
      self.populateData()
      self.analyzeData()

pm = PlayoffsMatching()
pm.main()