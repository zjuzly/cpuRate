import psutil as ps
import operator

def myfilter(proc):
    return proc.name() == 'YNoteCefRender.exe'

def getProcesses():
    processes = [proc for proc in ps.process_iter()]
    return list(filter(myfilter, processes))

class cpu_percent:
    '''Keep track of cpu usage.'''

    def __init__(self):
        processes = getProcesses()
        self.last = processes[2].cpu_times()
        print(self.last)

    def update(self):
        '''CPU usage is specific CPU time passed divided by total CPU time passed.'''

        last = self.last
        processes = getProcesses()
        current = processes[2].cpu_times()
        print(current)
        currentList = list(current)
        lastList = list(last)

        total_time_passed = sum(list(map(operator.sub, currentList, lastList)))
        print(total_time_passed)


        #only keeping track of system and user time
        sys_time = current.system - last.system
        usr_time = current.user - last.user

        self.last = current

        if total_time_passed > 0:
            sys_percent = 100 * sys_time / total_time_passed
            usr_percent = 100 * usr_time / total_time_passed
            return sys_percent + usr_percent
        else:
            return 0