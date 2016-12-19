#The source files being used only contain players that have data from the given year. There are many players in ESPN's player
     #pool that do not have any data ("--" listed for each column). These players are not included in the source file
     
from collections import OrderedDict
from operator import itemgetter

#Set global variables
print("Enter scoring values for the following categories: H, AB, R, HR, TB, RBI, BB, K, SB, CS, CYC")
print()
H = float(input("How many points per hit? "))
AB = float(input("How many points per AB? "))
R = float(input("How many points per run? "))
HR = float(input("How many points per HR? "))
TB = float(input("How many points per total base? "))
RBI = float(input("How many points per RBI? "))
BB = float(input("How many points per BB? "))
K = float(input("How many points per K? "))
SB = float(input("How many points per SB? "))
CS = float(input("How many points per caught stealing? "))
CYC = float(input("How many points per cycle? "))

#Prints out the scoring settings that the user entered
def getScoringSettings():
     print("""
Scoring settings:
     H = %g     AB = %g     R = %g     HR = %g    TB = %g
     RBI = %g   BB = %g     K = %g    SB = %g     CS = %g     CYC = %g
     """ % (H, AB, R, HR, TB, RBI, BB, K, SB, CS, CYC))

#PrimeData is given a file that contains stat totals of players, and returns a dictionary of player information as
   #a key and their point total for the entered scoring settings as the key
def primeData(file):
     dataFile = open(file, "r")
     battingData = []
     for line in dataFile:
          theLine = line.split()
          battingData.append(theLine)
     
     pointsDict = {}
     
     for entry in battingData:
          #Header will list the player's first and last name, along with the team they play for and their positions
          headerList = entry[:-10]
          header = ""
          for item in headerList:
               if item != "DTD":
                    header = header + str(item) + " "
          header = header[:-1]
          
          #                           0  1   2  3   4   5    6   7   8  9   10
          #stats will have the form: [H, AB, R, HR, TB, RBI, BB, K, SB, CS, CYC] (List of float values)     
          stats = []
          
          #H and AB columns require a bit of work to separate the values (begins in form H/AB)
          hAB = str(entry[-10])
          x = hAB.split("/")
          stats.append(float(x[0]))
          stats.append(float(x[1]))
          
          for i in range(-9, 0, 1): #Using negative indicies bypasses extra details in header i.e. DL15 or a 3rd column for name (Jackie Bradley Jr.)
               stats.append(float(entry[i]))
     
          #Multiplying each category by the number of points per stat based on league settings,
               #then adding them all together to get total points scored, and adding that total to a dictonary (key is the header from above)
          pointsScored = stats[0]*H + stats[1]*AB + stats[2]*R + stats[3]*HR + stats[4]*TB + stats[5]*RBI + stats[6]*BB + stats[7]*K + stats[8]*SB + stats[9]*CS + stats[10]*CYC
          pointsDict[header] = pointsScored
          
     return pointsDict

#Given an unordered dictionary, creates an ordered dictionary sorted by point totals and returns it
def sortDictionary(aDict):
     orderedPointsDict = OrderedDict(sorted(aDict.items(), key=itemgetter(1), reverse=True))
     return orderedPointsDict

def main():
     getScoringSettings()
     
     year = input("Want to use 2016 or 2015 data? ")
     fileName = "RawBattingData" + year + ".txt"
     
     pointsDict = primeData(fileName)
     orderedPointsDict = sortDictionary(pointsDict)
     
     print("Hitter rankings and the points they scored under the above scoring settings:")
     print()
     
     for header, points in orderedPointsDict.items():
          print('{header}: {points}'.format(header=header, points=points))

main()