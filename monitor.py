#!/usr/bin/env python

import math
import os
import sys
import time
import psutil
import scrollphat
from subprocess import PIPE, Popen
import docker

def get_cpu_temperature():
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
    output, _error = process.communicate()
    output = output.decode()

    pos_start = output.index('=') + 1
    pos_end = output.rindex("'")

    temp = float(output[pos_start:pos_end])

    return temp

scrollphat.set_brightness(100)
scrollphat.set_rotate(1)

print('CPU temperature: ' + str(get_cpu_temperature()))

load = psutil.cpu_percent(percpu=1)

for c in range(4):
	print("CPU " + str(c) + " load: " + str(load[c]))

print('CPU Load: ' + str(load))

client = docker.from_env()
for container in client.containers.list():
  print(container.id)

print("Number of docker machines running: " + str(len(client.containers.list())))

while(True):
    try:
        for c in range (4):
            for x in range (int(psutil.cpu_percent(percpu=1)[c]/10)):
                scrollphat.set_pixel(x,c,1)

        for x in range (int(get_cpu_temperature()/10)):
            scrollphat.set_pixel(x,4,1)

        for x in range (int(len(client.containers.list()))):
            scrollphat.set_pixel(10,4-x,1)

        scrollphat.update()
        scrollphat.clear()

    except KeyboardInterrupt:
        scrollphat.clear()
        sys.exit(-1)
