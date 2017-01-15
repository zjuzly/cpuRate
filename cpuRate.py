import psutil

def myfilter(proc):
    return proc.name() == 'YNoteCefRender.exe'

cpu = psutil.cpu_percent(interval=1)
print(cpu)

# while(True):
#    processes = [proc for proc in psutil.process_iter()]
#
#    processes = filter(myfilter, processes)

 #   cpu_count = psutil.cpu_count()

#    for proc in processes:
#        print(proc.cpu_percent() / (proc.num_threads() * cpu_count))
