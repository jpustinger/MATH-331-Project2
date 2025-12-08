#python3 331.py -ns 10 -nl 15 -s 5 -l 3 -p example run
import sys
import math
import copy
import csv
import argparse
import matplotlib.pyplot as plt

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--smallclasses", "-ns", type=int, default=40, help="Number of small classes to schedule")
    parser.add_argument("--largeclasses", "-nl", type=int, default=10, help="Number of large classes to schedule")
    parser.add_argument("--smallclassrooms", "-s", type=int, default=5, help="Number of small classrooms available per hour")
    parser.add_argument("--largeclassrooms", "-l", type=int, default=3, help="Number of large classrooms available per hour")
    parser.add_argument("--detailed", "-d", action="store_true", default=False)
    parser.add_argument("--plot", "-p", action="store_true", default=False, help="Generate visualization plot")
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
    
    if args.plot:
        plotSchedule(myArray, args.largeclasses, args.smallclasses, S, L, detailed=args.detailed)


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


def fillLargeClasses(myArray, Nl, L):
    for i in range(len(myArray)):
        while(myArray[i][0] < L and Nl > 0):
            myArray[i][0] += 1
            Nl -= 1


def primaryGoal(myArray) -> int:
    Zt = 0
    for i in range(len(myArray)):
        if(myArray[i][0] > 0 or myArray[i][1] > 0):
            Zt += 1
    return Zt


def secondaryGoal(myArray, Nl) -> int:
    SLt = 0
    for i in range(len(myArray)):
        SLt += myArray[i][0]
    return SLt - Nl


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


def plotSchedule(myArray, original_Nl, original_Ns, S, L, detailed=False):
    import matplotlib.pyplot as plt
    import numpy as np
    
    hours = primaryGoal(myArray)
    if hours == 0:
        print("No classes scheduled - nothing to plot")
        return

    fig = plt.figure(figsize=(14, 8))
    gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.2], hspace=0.25, wspace=0.3)
    
 
    total_slots = len(myArray)
    used_slots = hours
    wasted_capacity = secondaryGoal(myArray, original_Nl)
    efficiency = (1 - wasted_capacity / (L * used_slots)) * 100 if used_slots > 0 else 0
    
 
    ax1 = fig.add_subplot(gs[0, 0])
    
    metrics = ['Slots\nUsed', 'Slots\nUnused', 'Wasted\nCapacity']
    values = [used_slots, total_slots - used_slots, wasted_capacity]
    colors = ['#2ca02c', '#e0e0e0', '#ff4444']
    
    bars = ax1.bar(metrics, values, color=colors, alpha=0.85, edgecolor='black')
    ax1.set_ylabel('Count', fontsize=11)
    ax1.set_title('Optimization Results', fontsize=12, fontweight='bold')
    ax1.grid(axis='y', alpha=0.4)
    
    for bar, value in zip(bars, values):
        ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.15,
                f'{int(value)}', ha='center', va='bottom', fontweight='bold', fontsize=11)
    

    ax1.text(0.5, 0.85, f'Efficiency: {efficiency:.1f}%', 
            transform=ax1.transAxes, ha='center', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))
    

    ax2 = fig.add_subplot(gs[0, 1])
    
    large_used = sum(slot[0] for slot in myArray)
    small_used = sum(slot[1] for slot in myArray)
    
    used_pct = [(large_used/(L*used_slots))*100, (small_used/(S*used_slots))*100]
    categories = ['Large\nRooms', 'Small\nRooms']
    
    bars = ax2.bar(categories, used_pct, color=['#1f77b4', '#4e79a7'], alpha=0.8)
    ax2.set_ylabel('Utilization (%)', fontsize=11)
    ax2.set_title('Room Utilization', fontsize=12, fontweight='bold')
    ax2.set_ylim(0, 105)
    ax2.grid(axis='y', alpha=0.3)
    
    for bar, value in zip(bars, used_pct):
        ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1,
                f'{value:.1f}%', ha='center', va='bottom', fontweight='bold')
    

    ax3 = fig.add_subplot(gs[1, :])
    
    time_slots = list(range(1, hours + 1))
    large_classes = []
    small_classes = []
    Nl = original_Nl
    
    for i in range(hours):
        actual_large = min(Nl, myArray[i][0])
        overflow_small = max(0, myArray[i][0] - actual_large)
        large_classes.append(actual_large)
        small_classes.append(myArray[i][1] + overflow_small)
        Nl -= actual_large
    

    ax3.bar(time_slots, small_classes, label=f'Small Classes', color='#4e79a7', alpha=0.8)
    ax3.bar(time_slots, large_classes, bottom=small_classes, label=f'Large Classes', 
            color='#f28e2c', alpha=0.8)
    

    ax3.axhline(y=S, color='blue', linestyle='--', linewidth=1.5, alpha=0.7)
    ax3.axhline(y=S+L, color='red', linestyle='--', linewidth=1.5, alpha=0.7)
    ax3.text(0.02, S+0.1, f'Small limit = {S}', transform=ax3.get_yaxis_transform(), 
             va='bottom', fontsize=9, color='blue')
    ax3.text(0.02, S+L+0.1, f'Total limit = {S+L}', transform=ax3.get_yaxis_transform(), 
             va='bottom', fontsize=9, color='red')
    

    for i, sc in enumerate(small_classes):
        if sc > S:
            ax3.bar(i + 1, sc - S, bottom=S, color='red', alpha=0.25, width=0.8, hatch='///')
    
    ax3.set_xlabel('Time Slot (t)', fontsize=12)
    ax3.set_ylabel('Number of Classes', fontsize=12)
    ax3.set_title(f'Final Schedule (Red hatch = Small classes in Large rooms)', 
                  fontsize=13, fontweight='bold')
    ax3.set_ylim(0, S + L + 1)
    ax3.legend(loc='upper right', fontsize=10)
    ax3.grid(axis='y', alpha=0.3)
    
    for i, (lt, st) in enumerate(zip(large_classes, small_classes)):
        total = lt + st
        if total > 0:
            ax3.text(i + 1, total + 0.1, f'{int(total)}', 
                    ha='center', va='bottom', fontweight='bold')
    

    fig.suptitle(f'Classroom Schedule: {original_Ns} Small, {original_Nl} Large Classes | {S} Small, {L} Large Rooms', 
                 fontsize=14, fontweight='bold', y=0.995)
    
    plt.savefig("schedule_dashboard.png", dpi=300, bbox_inches='tight')
    print("Schedule dashboard saved as 'schedule_dashboard.png'")
    plt.show()
if __name__ == "__main__":
    main()
