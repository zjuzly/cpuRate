import numpy as np
import pylab as pl
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import FormatStrFormatter

def visualization(arrs1, arrs2): 
    pl.title('cpu usage')
    pl.ylabel('cpu usage(%)')
    pl.xlabel('x axis')

    pl.ylim(0, 100)
    
    ax = pl.subplot(111)
    for idx, arr in enumerate(arrs1):
        pl.plot(arr, label='proc ' + str(idx) + ' in ms')

    for idx, arr in enumerate(arrs2):
        pl.plot(arr, label='proc ' + str(idx) + ' in online')
    
    ymajorLocator = MultipleLocator(5.0)
    yminorLocator = MultipleLocator(2.0)
    ax.yaxis.set_major_locator(ymajorLocator)
    ax.yaxis.set_minor_locator(yminorLocator)

    pl.legend()
    pl.show()

def parseData(lines):
    length = len(lines[0].strip().split(' '))
    arrs = [None] * length 
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
