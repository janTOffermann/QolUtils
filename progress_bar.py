import time
import datetime
import numpy as np

# Print iterations progress.
# Adapted from https://stackoverflow.com/a/34325723.
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()

# Progress bar with color.
def printProgressBarColor (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    fill_prefix = '\33[31m'
    fill_suffix = '\033[0m'
    prog = iteration/total
    if(prog > 0.33 and prog <= 0.67): fill_prefix = '\33[33m'
    elif(prog > 0.67): fill_prefix = '\33[32m'
    fill = fill_prefix + fill + fill_suffix
    printProgressBar(iteration, total, prefix = prefix, suffix = suffix, decimals = decimals, length = length, fill = fill, printEnd = printEnd)
    return

class ProgressBar():
    """
    An object-oriented approach to the progress bar.
    Gives an estimated time remaining.
    """

    def __init__(self,prefix = '', suffix = '', decimals = 1, length = 25, fill = '█', printEnd = "\r", memory_depth=10):
        self.prefix = prefix
        self.suffix = suffix
        self.decimals = decimals
        self.length = length
        self.fill = fill
        self.printEnd = printEnd

        self.mem_depth = memory_depth
        self.timestamps = np.zeros(self.mem_depth)
        self.ncalls = 0

    def Print(self,iteration,total):

        if(self.ncalls < self.mem_depth):
            self.timestamps[self.ncalls] = time.time()
            suffix = self.suffix
        else:
            self.timestamps = np.roll(self.timestamps,-1)
            self.timestamps[-1] = time.time()
            # For now, do a simple average speed.
            # (could consider something fancier?)
            remaining_time = (total - iteration) * (self.timestamps[-1] - self.timestamps[0]) / (self.mem_depth - 1)
            remaining_time_string = str(datetime.timedelta(seconds=remaining_time)).split('.')[0]
            suffix = self.suffix + '   Estimated remaining: {}   '.format(remaining_time_string)

        printProgressBar(iteration,total,self.prefix,suffix,self.decimals,self.length,self.fill,self.printEnd)
        self.ncalls += 1
