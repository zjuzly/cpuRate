import numpy as np
import pylab as pl

def visualization(arrs1, arrs2): 
    pl.title('cpu usage')
    pl.ylabel('cpu usage(%)')
    pl.xlabel('x axis')

    pl.ylim(0, 100)

    for idx, arr in enumerate(arrs1):
        pl.plot(arr, label='proc ' + str(idx) + ' in ms')

    for idx, arr in enumerate(arrs2):
        pl.plot(arr, label='proc ' + str(idx) + ' in online')

    pl.legend()
    pl.show()

def parseData(lines):
    length = len(lines[0].strip().split(' '))
    arrs = [None] * length 
    lines = lines[1:]
    for line in lines:
        ratios = line.strip().split(' ')
        print(ratios)
        for index in range(length):
            arrs[index] = arrs[index] or []
            arrs[index].append(float(ratios[index]))
    return arrs

    
def loadData(filename1, *filename2):
    arrs1 = []
    arrs2 = []

    fp = open(filename1)
    lines = fp.readlines()
    arrs1 = parseData(lines[1:])
    fp.close()
    
    if filename2:
        fp = open(filename2)
        lines = fp.readlines()
        arrs2 = parseData(lines[1:])
        fp.close()

    return (arrs1, arrs2)

(arrs1, arrs2) = loadData('cpu_usage.txt')
visualization(arrs1, arrs2)
