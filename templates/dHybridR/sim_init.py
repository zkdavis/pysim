import dhybridr.initializer as sim
from pysim.parsing import File
from glob import glob
import os
import shutil
import numpy as np
from pathlib import Path

amp = 1.,
k = 1., np.pi

if __name__ == '__main__':
    # clean files
    for file in glob('input/*.unf'):
        os.remove(file)
    if os.path.exists("Output"): shutil.rmtree("Output")
    if os.path.exists("Restart"): shutil.rmtree("Restart")
    # make init
    xf = File('test')
    Init = sim.TurbInit(xf)#(amp, k)
    Init.saveFortran(path='input/')
    os.system("sh submit_anvil.sh")
