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
        print('Mem: {4:4d}MiB    Load: {6:3d}%    Temp: {1:2d}C    Power: {2:3d}W    Fan: {0:3d}%'.format(*getNVdata()))
        time.sleep(1)
