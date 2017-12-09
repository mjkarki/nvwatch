import subprocess
import re
import time

def getNVdata():
    """
    Returns GPU statistics in a list:
    Fan speed (%)
    Power usage (W)
    Max power (W)
    Memory usage (MiB)
    Max memory (MiB)
    GPU usage (%)
    """
    retval = list()

    result = subprocess.run(r'C:\Program Files\NVIDIA Corporation\NVSMI\nvidia-smi.exe', stdout=subprocess.PIPE)
    res = result.stdout.decode('iso-8859-1')

    m = re.search(r'\|.+?([0-9]+)%.+?([0-9]+)C.+?([0-9]+)W.+?\/.+?([0-9]+)W.+?\|.+?([0-9]+).+?\/.+?([0-9]+).+?\|.+?([0-9]+)%', res)

    for i in range(1, 8):
        retval.append(int(m.group(i)))

    return retval

if __name__ == '__main__':
    while True:
        print('Fan: {:3d}%\tTemp: {:2d}C ({:3d}/{:3d}W)\tMem: {:4d}/{:4d}MiB\tLoad: {:3d}%'.format(*getNVdata()))
        time.sleep(1)
