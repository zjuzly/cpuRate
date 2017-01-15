from ctypes import *
from ctypes.wintypes import *
import win32api
import win32process
import win32con
import time
import psutil
import sys
import getopt

argsLen = len(sys.argv)
sysTime = argsLen > 1 and sys.argv[1] or 0 
sleepTime = argsLen > 2 and sys.argv[2] or 1
iterCount = argsLen > 3 and sys.argv[3] or 10
procName = argsLen > 4 and sys.argv[4] or 'YNoteCefRender.exe'

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


def cpu_utilization():
        """
        Returns the total cpu usage

        Source: http://www.codeproject.com/Articles/9113/Get-CPU-Usage-with-GetSystemTimes
        :return: CPU usage (int)
        """

        FirstSystemTimes = GetSystemTimes()
        time.sleep(sleepTime)
        SecSystemTimes = GetSystemTimes()

        """
         CPU usage is calculated by getting the total amount of time
         the system has operated since the last measurement
         made up of kernel + user) and the total
         amount of time the process has run (kernel + user).
        """

        usr = SecSystemTimes['userTime'] - FirstSystemTimes['userTime']
        ker = SecSystemTimes['kernelTime'] - FirstSystemTimes['kernelTime']
        idl = SecSystemTimes['idleTime'] - FirstSystemTimes['idleTime']

        # print(usr)
        # print(ker)
        
        global sysTime
        sysTime = usr + ker
        return int((sysTime - idl) * 100 / sysTime)

def cpu_process_util(PID):
        """
        Returns the process usage of CPU

        Source: http://www.philosophicalgeek.com/2009/01/03/determine-cpu-usage-of-current-process-c-and-c/
        :return: Process CPU usage (int)
        """

        # Creates a process handle
        proc = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, PID)

        FirstProcessTimes = win32process.GetProcessTimes(proc)
        time.sleep(sleepTime)
        SecProcessTimes = win32process.GetProcessTimes(proc)

        """
         Process CPU usage is calculated by getting the total amount of time
         the system has operated since the last measurement
         made up of kernel + user) and the total
         amount of time the process has run (kernel + user).
        """

        proc_time_user_prev = FirstProcessTimes['UserTime']
        proc_time_kernel_prev = FirstProcessTimes['KernelTime']

        proc_time_user = SecProcessTimes['UserTime']
        proc_time_kernel = SecProcessTimes['KernelTime']

        proc_usr = proc_time_user - proc_time_user_prev
        proc_ker = proc_time_kernel - proc_time_kernel_prev

        proc_total_time = proc_usr + proc_ker

        global sysTime
        # print(sysTime)

        return (100 * proc_total_time) / sysTime


cpu_utilization()

# PID = input("Enter a PID: ")

fp = open('cpu_usage.txt', 'w')

processes = [proc for proc in psutil.process_iter()]
processes = filter(myfilter, processes)
pids = []
for proc in processes:    
    pids.append(str(proc.pid))

fp.write(" ".join(pids) + "\n")

for i in range(iterCount):
    print('+--------------+')
    processes = [proc for proc in psutil.process_iter()]
    processes = filter(myfilter, processes)
    cpu_usage = []
    for proc in processes:
        cpu_usage.append(str(cpu_process_util(proc.pid)))
        print('PID: %d, usage: %s' % (proc.pid, cpu_usage[-1]))
    print('+--------------+')
    fp.write(" ".join(cpu_usage) + "\n")

fp.close()
