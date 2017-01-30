import os
import subprocess

for file in os.listdir('./sample_images'):
    pic = str(file)
    proc = subprocess.getoutput('./getShotClock.sh ./sample_images/{}'.format(pic))
    print(proc, ":",pic)
