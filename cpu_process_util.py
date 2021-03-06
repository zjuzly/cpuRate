from ctypes import *
from ctypes.wintypes import *
import win32api
import win32process
import win32con
import time
import psutil
import sys
import getopt


sysTime = 0 
sleepTime = 1
iterCount = 10
procName = 'YNoteCefRender.exe'
procArray = []

def usage():
    """
    Usage: cpuRate.py -s -i -p -v -h
    
    Description
        -s, the interval of sampling system time or process time, in seconds
        -i, the count of sampling cpu usage 
        -p, the process name
        -v, visualizing the cpu usage
        -h, help

    for example:
        python cpu_process_util.py -s 1 -i 10 -p YNoteCefRender.exe -h
    """

def run():
    global sleepTime, iterCount, procName
    #try:
    v = False;
    options, args = getopt.getopt(sys.argv[1:], "s:i:p:hv")
    for opt1, opt2 in options:
        if opt1 == '-s':
           	sleepTime = float(opt2)
        elif opt1 == '-i':
           	iterCount = int(opt2)
        elif opt1 == '-p':
           	procName = str(opt2)
        elif opt1 == '-v':
           	v = True       
        elif opt1 == '-h':
           	print(usage.__doc__)
    calcCpuUsage()
    #except:
    #  print(usage.__doc__)


class FILETIME(Structure):
    _fields_ = [
        ("dwLowDateTime", DWORD),
        ("dwHighDateTime", DWORD)]

def myfilter(proc):
    return procName == proc.name()


def GetSystemTimes():
    """
    Uses the function GetSystemTimes() (win32) in order to get the user mode time, kernel mode time and idle mode time
    :return: user time, kernel time and idle time (Dictinary)
    """

    __GetSystemTimes = windll.kernel32.GetSystemTimes
    idleTime, kernelTime, userTime = FILETIME(), FILETIME(), FILETIME()

    success = __GetSystemTimes(

            byref(idleTime),
            byref(kernelTime),
            byref(userTime))

    assert success, ctypes.WinError(ctypes.GetLastError())[1]

    return {
        "idleTime": idleTime.dwLowDateTime,
        "kernelTime": kernelTime.dwLowDateTime,
        "userTime": userTime.dwLowDateTime}


#def cpu_utilization():
#        """
#        Returns the total cpu usage
#
#        Source: http://www.codeproject.com/Articles/9113/Get-CPU-Usage-with-GetSystemTimes
#        :return: CPU usage (int)
#        """
#
#        FirstSystemTimes = GetSystemTimes()
#        time.sleep(sleepTime)
#        SecSystemTimes = GetSystemTimes()
#
#        """
#         CPU usage is calculated by getting the total amount of time
#         the system has operated since the last measurement
#         made up of kernel + user) and the total
#         amount of time the process has run (kernel + user).
#        """
#
#        usr = SecSystemTimes['userTime'] - FirstSystemTimes['userTime']
#        ker = SecSystemTimes['kernelTime'] - FirstSystemTimes['kernelTime']
#        idl = SecSystemTimes['idleTime'] - FirstSystemTimes['idleTime']
#
#        # print(usr)
#        # print(ker)
#        
#        global sysTime
#        sysTime = usr + ker
#        return int((sysTime - idl) * 100 / sysTime)
#
def cpu_process_util(pHandler):
        """
        Returns the process usage of CPU

        Source: http://www.philosophicalgeek.com/2009/01/03/determine-cpu-usage-of-current-process-c-and-c/
        :return: Process CPU usage (int)
        """
        FirstProcessTimes = 0
        SecProcessTimes = 0
        cpu_usage = 0 
        
        FirstProcessTimes = win32process.GetProcessTimes(pHandler)

        FirstSystemTimes = GetSystemTimes()
        time.sleep(sleepTime)
        SecSystemTimes = GetSystemTimes()
        
        usr = SecSystemTimes['userTime'] - FirstSystemTimes['userTime']
        ker = SecSystemTimes['kernelTime'] - FirstSystemTimes['kernelTime']
        idl = SecSystemTimes['idleTime'] - FirstSystemTimes['idleTime']
        sysTime = usr + ker
        
        SecProcessTimes = win32process.GetProcessTimes(pHandler)
        
        proc_time_user_prev = FirstProcessTimes['UserTime']
        proc_time_kernel_prev = FirstProcessTimes['KernelTime']
        
        proc_time_user = SecProcessTimes['UserTime']
        proc_time_kernel = SecProcessTimes['KernelTime']

        proc_usr = proc_time_user - proc_time_user_prev
        proc_ker = proc_time_kernel - proc_time_kernel_prev

        proc_total_time = proc_usr + proc_ker
        cpu_usage = (100 * proc_total_time) / sysTime
        return cpu_usage

def filterProcess(pids):
    global procArray
    maxUsage = 0
    maxPid = -1
    pHandler = None
    for idx, pid in enumerate(pids):
        usage = cpu_process_util(procArray[idx])
        if maxUsage < usage:
            maxUsage = usage
            maxPid = pid
            pHandler = procArray[idx]
    return (maxUsage, maxPid, pHandler)


def calcCpuUsage():
    fp = open('cpu_usage.txt', 'w')
    processes = [proc for proc in psutil.process_iter()]
    processes = filter(myfilter, processes)
    pids = []
    for proc in processes:
        pids.append(proc.pid)
     
    global procArray
    procArray = [None] * len(pids)
    for idx, PID in enumerate(pids):
        # Creates a process handle
        procArray[idx] = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, PID)
    
    maxUsage = 0
    maxPid = -1
    pHandler = None
    (maxUsage, maxPid, pHandler) = filterProcess(pids)

    fp.write(str(maxPid) + "\n")
 
    i = 0
    for i in range(iterCount):
        print('+--------------+')
        maxUsage = cpu_process_util(pHandler)
        print('PID: %d, usage: %s' % (maxPid, maxUsage))
        print('+--------------+')
        fp.write(str(maxUsage) + "\n")

    fp.close()

run()
