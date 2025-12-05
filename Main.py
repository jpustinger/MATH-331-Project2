import sys
import math
import copy

def main():
    if len(sys.argv) != 5:
        sys.exit(1)
    Ns = int(sys.argv[1])
    Nl = int(sys.argv[2])
    S = int(sys.argv[3])
    L = int(sys.argv[4])
    myArray = init(Ns, Nl, S, L)
    fillLargeClasses(myArray, Nl, L)
    print(myArray)
    print(primaryGoal(myArray))
    print(secondaryGoal(myArray, Nl))
    beginIteration(myArray, Ns, Nl, S, L)
    
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
def primaryGoal(myArray):
    Zt = 0
    for i in range(len(myArray)):
        if(myArray[i][0] > 0 or myArray[i][0]):
            Zt += 1
    return Zt

#finds number of wasted classes by finding total classes booked in large classrooms and subtracting number of large classes
def secondaryGoal(myArray, Nl):
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
    print("Arr set to bestArr")      
    for i in range(Ns):
        #print(startArray)
        diff = i + 1
        currArr = copy.deepcopy(startArray)
        if(Ns - diff > S * len(startArray) or diff + Nl > L * len(startArray)):
            print("Input of SinS = " + str(Ns - diff) + " and SinL = " + str(diff) + " will not be optimal")
            continue
        fillSmallClasses(currArr, S, L, Ns - diff, diff)
        if (bestPrimary(currArr) < bestPrimary(bestArr)):
            print("New best found")
            bestArr = copy.deepcopy(currArr)
            bestPrimary = primaryGoal(bestArr)
            bestSecondary = secondaryGoal(bestArr, Nl)
    return

def fillSmallClasses(currArr, S, L, SinS, SinL):
    print("Filled Array w/ SinS = " + str(SinS) + " and SinL = " + str(SinL) + ":")
    for i in range(len(currArr)):
        if SinS == 0 and SinL == 0:
            break
        while currArr[i][0] < L and SinL > 0:
            currArr[i][0] += 1
            SinL -= 1
        while currArr[i][1] < S and SinS > 0:
            currArr[i][1] += 1
            SinS -= 1
    print(currArr)

if __name__ == "__main__":
    main()
