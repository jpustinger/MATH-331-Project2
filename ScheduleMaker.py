import sys
import math
import copy
import csv
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--smallclasses", "-ns", type = int, default = 40, help = "Number of small classes to schedule")
    parser.add_argument("--largeclasses", "-nl", type = int, default = 10, help = "Number of large classes to schedule")
    parser.add_argument("--smallclassrooms", "-s", type = int, default = 5, help = "Number of small classrooms available per hour")
    parser.add_argument("--largeclassrooms", "-l", type = int, default = 3, help = "Number of large classrooms available per hour")
    parser.add_argument("--detailed", "-d", action = "store_true", default = False)
    args = parser.parse_args()
    Ns = args.smallclasses
    Nl = args.largeclasses
    S = args.smallclassrooms
    L = args.largeclassrooms
    myArray = init(Ns, Nl, S, L)
    fillLargeClasses(myArray, Nl, L)
    myArray = beginIteration(myArray, Ns, Nl, S, L)
    if args.detailed:
        printScheduleDetailed(myArray, Nl)
    else:
        printSchedule(myArray, Nl)
    
#creates initial 2D array based on the greater of total classroom constraints and large classroom constraints
def init(Ns, Nl, S, L):
    constr1 = math.ceil(Ns / S)
    constr2 = math.ceil(Nl / L)
    rows = constr1 if constr1 > constr2 else constr2
    columns = 2
    returnArr = []
    for i in range(rows):
        row = [0] * columns
        returnArr.append(row)
    return returnArr

#optimal solution always has large classes filled first, so this method is simple
def fillLargeClasses(myArray, Nl, L):
    for i in range(len(myArray)):
        while(myArray[i][0] < L and Nl > 0):
            myArray[i][0] += 1
            Nl -= 1

#finds number of time slots used
def primaryGoal(myArray) -> int:
    Zt = 0
    for i in range(len(myArray)):
        if(myArray[i][0] > 0 or myArray[i][1] > 0):
            Zt += 1
    return Zt

#finds number of wasted classes by finding total classes booked in large classrooms and subtracting number of large classes
def secondaryGoal(myArray, Nl) -> int:
    SLt = 0
    for i in range(len(myArray)):
        SLt += myArray[i][0]
    return SLt - Nl

#have idea but not sure if it is the most efficient, can discuss in class
def beginIteration(startArray, Ns, Nl, S, L):
    currArr = copy.deepcopy(startArray)
    fillSmallClasses(currArr, S, L, Ns, 0)
    bestArr = copy.deepcopy(currArr)
    bestPrimary = primaryGoal(bestArr)
    bestSecondary = secondaryGoal(bestArr, Nl)    
    for i in range(Ns):
        diff = i + 1
        currArr = copy.deepcopy(startArray)
        if(Ns - diff > S * len(startArray) or diff + Nl > L * len(startArray)):
            continue
        fillSmallClasses(currArr, S, L, Ns - diff, diff)
        if bestPrimary > primaryGoal(currArr) or (bestPrimary == primaryGoal(currArr) and bestSecondary > secondaryGoal(currArr, Nl)):
            bestArr = copy.deepcopy(currArr)
            bestPrimary = primaryGoal(bestArr)
            bestSecondary = secondaryGoal(bestArr, Nl)
    return bestArr

def fillSmallClasses(currArr, S, L, SinS, SinL):
    for i in range(len(currArr)):
        if SinS == 0 and SinL == 0:
            break
        while currArr[i][0] < L and SinL > 0:
            currArr[i][0] += 1
            SinL -= 1
        while currArr[i][1] < S and SinS > 0:
            currArr[i][1] += 1
            SinS -= 1


def printSchedule(myArray, Nl):
    with open("Schedule.csv", "w", newline="") as file:
        writer = csv.writer(file)
        currentLine = ["t", "Lt", "St"]
        writer.writerow(currentLine)
        hours = primaryGoal(myArray)
        currentLine.clear()
        for i in range(hours):
            currentLine.append(i + 1)
            if(myArray[i][0] < Nl):
                currentLine.append(myArray[i][0])
                currentLine.append(myArray[i][1])
                Nl -= myArray[i][0]
            else:
                currentLine.append(Nl)
                currentLine.append(myArray[i][0] + myArray[i][1] - Nl)
                Nl = 0
            writer.writerow(currentLine)
            currentLine.clear()


def printScheduleDetailed(myArray, Nl):
    with open("Schedule.csv", "w", newline="") as file:
        writer = csv.writer(file)
        currentLine = ["t", "Lt", "Slt", "Sst", "St"]
        writer.writerow(currentLine)
        hours = primaryGoal(myArray)
        Slt = 0
        currentLine.clear()
        for i in range(hours):
            currentLine.append(i + 1)
            if(myArray[i][0] < Nl):
                currentLine.append(myArray[i][0])
                Nl -= myArray[i][0]
                currentLine.append(0)
            else:
                currentLine.append(Nl)
                Slt = myArray[i][0] - Nl
                currentLine.append(Slt)
                Nl = 0
            currentLine.append(myArray[i][1])
            currentLine.append(myArray[i][1] + Slt)
            writer.writerow(currentLine)
            currentLine.clear()
        
        

if __name__ == "__main__":
    main()
