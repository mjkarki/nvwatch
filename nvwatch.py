import subprocess
import re
from time import sleep

NVSMI = r'C:\Program Files\NVIDIA Corporation\NVSMI\nvidia-smi.exe'

def getNVdata():
    """
    Calls nvidia-smi.exe to acquire GPU information.
    Returns GPU statistics in a list:
    [Fan speed (%),
     Power usage (W),
     Max power (W),
     Memory usage (MiB),
     Max memory (MiB),
     GPU usage (%)]
    """
    retval = list()

    result = subprocess.run(NVSMI, stdout=subprocess.PIPE)
    res = result.stdout.decode('iso-8859-1')

    m = re.search(r'\|.+?([0-9]+)'
                  r'%.+?([0-9]+)C'
                  r'.+?([0-9]+)W'
                  r'.+?\/.+?([0-9]+)W'
                  r'.+?\|.+?([0-9]+)'
                  r'.+?\/.+?([0-9]+)'
                  r'.+?\|.+?([0-9]+)%', res)

    for i in range(1, 8):
        retval.append(int(m.group(i)))

    return retval

if __name__ == '__main__':
    running = True
    memmax   = 0
    loadmax  = 0
    tempmax  = 0
    powermax = 0
    fanmax  = 0

    while running:
        try:
            rslt = getNVdata()

            if memmax    < rslt[4]:
                memmax   = rslt[4]
            if loadmax   < rslt[6]:
                loadmax  = rslt[6]
            if tempmax   < rslt[1]:
                tempmax  = rslt[1]
            if powermax  < rslt[2]:
                powermax = rslt[2]
            if fanmax    < rslt[0]:
                fanmax   = rslt[0]

            print('Mem: {4:4d}MiB'
                  '    Load: {6:3d}%'
                  '    Temp: {1:2d}C'
                  '    Power: {2:3d}W'
                  '    Fan: {0:3d}%'.format(*rslt))
            sleep(1)
        except KeyboardInterrupt:
            print('\nPeak values:')
            print('Mem: {0:4d}MiB'
                '    Load: {1:3d}%'
                '    Temp: {2:2d}C'
                '    Power: {3:3d}W'
                '    Fan: {4:3d}%'.format(memmax, loadmax, tempmax, powermax, fanmax))

            response = input('\nMonitoring paused. Continue, restart or quit [c, r, q]? ').lower()

            if (response == 'r'):
                memmax   = 0
                loadmax  = 0
                tempmax  = 0
                powermax = 0
                fanmax  = 0
            elif (response == 'q'):
                running = False
