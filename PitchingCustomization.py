#The source files being used only contain players that have data from the given year. There are many players in ESPN's player
     #pool that do not have any data ("--" listed for each column). These players are not included in the source file

from collections import OrderedDict
from operator import itemgetter

print("Enter scoring values for the following categories: IP, H, ER, BB, K, PKO, QS, CG, SO, NH, PG, W, L, SV, BS")
print()
IP = float(input("How many points per IP? "))
H = float(input("How many points per H? "))
ER = float(input("How many points per ER? "))
BB = float(input("How many points per BB? "))
K = float(input("How many points per K? "))
PKO = float(input("How many points per pickoff? "))
QS = float(input("How many points per quality start? "))
CG = float(input("How many points per complete game? "))
SO = float(input("How many points per shutout? "))
NH = float(input("How many points per no hitter? "))
PG = float(input("How many points per perfect game? "))
W = float(input("How many points per win? "))
L = float(input("How many points per loss? "))
SV = float(input("How many points per save? "))
BS = float(input("How many points per blown save? "))

def getScoringSettings():
    print("""
Scoring settings:
     IP = %g              H = %g     ER = %g     BB = %g         K = %g
     PKO = %g             QS = %g    CG = %g     Shutout = %g    No hitter = %g
     Perfect game = %g    W = %g     L = %g      SV = %g         BS = %g
"""%(IP, H, ER, BB, K, PKO, QS, CG, SO, NH, PG, W, L, SV, BS))

def primeData(file):
    dataFile = open(file, "r")
    pitchingData = []
    for line in dataFile:
        theLine = line.split()
        pitchingData.append(theLine)
    
    pointsDict = {}
        
    for entry in pitchingData:
        #Header will list the player's first and last name, along with the team they play for and their positions
        headerList = entry[:-15]
        header = ""
        for item in headerList:
            if item != "DTD":
                header = header + str(item) + " "
        header = header[:-1] #Removes last space
        
        #stats has the form: [IP, H, ER, BB, K, PKO, QS, CG, SO, NH, PG, W, L, SV, BS] (List of float values)
        stats = []
        for i in range(-15, 0, 1): #Using negative indicies bypasses extra details in header i.e. DL15 or a 3rd column for name (Seung Hawn Oh)
            stats.append(float(entry[i]))
        
        #IP requires some extra work, as a player that pitched, for example, 200 and 1/3rd innings has 200.1 as their entry
             #The correct IP total doesn't work if you just take 200.1 * points per IP
        inningsPitched = stats[0]
        rounded = inningsPitched // 1
        extra = inningsPitched % 1
        
        if extra > 0.0 and extra <= 0.1:
            extra = 1.0
        elif extra > 0.1 and extra <= 0.2:
            extra = 2.0
        else:
            extra = 0.0
        totalIP = rounded
        IPpoints1 = rounded*IP
        IPpoints2 = extra*(IP/3)
        totalIPpoints = IPpoints1 + IPpoints2
        
        #Multiplying each category by the number of points per stat based on league settings,
           #then adding them all together to get total points scored, and adding that total to a dictonary (key is the header from above)
        pointsScored = totalIPpoints + stats[1]*H + stats[2]*ER + stats[3]*BB + stats[4]*K + stats[5]*PKO + stats[6]*QS + stats[7]*CG + stats[8]*SO + stats[9]*NH + stats[10]*PG + stats[11]*W + stats[12]*L + stats[13]*SV + stats[14]*BS    
        pointsDict[header] = pointsScored
        
    return pointsDict

def sortDictionary(aDict):
    orderedPointsDict = OrderedDict(sorted(aDict.items(), key=itemgetter(1), reverse=True))
    return orderedPointsDict

def main():
    getScoringSettings()
    
    year = input("Want to use 2016 or 2015 data? ")
    fileName = "RawPitchingData" + year + ".txt"
    
    pointsDict = primeData(fileName)
    orderedPointsDict = sortDictionary(pointsDict)    

    print("Pitcher rankings and the points they scored under the above scoring settings:")
    print()

    for header, points in orderedPointsDict.items():
        print('{header}: {points}'.format(header=header, points=points))

main()