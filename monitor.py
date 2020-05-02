#!/usr/bin/env python

import argparse
import scrollphat
import time
import sys
from subprocess import PIPE, Popen
import psutil
import docker

def get_cpu_temperature():
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
    output, _error = process.communicate()
    output = output.decode()

    pos_start = output.index('=') + 1
    pos_end = output.rindex("'")

    temp = float(output[pos_start:pos_end])

    return temp

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v','--verbose',action='store_true',help='increase output verbosity')
    parser.add_argument('-b','--brightness',help='set the brightness (default is 25)',type=int,default=25)
    parser.add_argument('-r','--rotate',action='store_true',help='Rotate the display on the ScrollPhate',default=False)
    parser.add_argument('-i','--interval',help='set the refresh interval (default is 0.05)',type=int,default=0.05)
    parser.add_argument('-t','--temperature',help='Define on which line the temperature graph is displayed (default is 0)',type=int,default=0)
    parser.add_argument('-c','--cpu',help='Define on which line the cpu load graph is displayed (default is 1)',type=int,default=1)
    parser.add_argument('-d','--docker',help='Define on which line the number of docker containers is displayed (default is 4)',type=int,default=4)
    args = parser.parse_args()
    temp = get_cpu_temperature()
    client = docker.from_env()
    nb_containers = len(client.containers.list())
    if args.verbose:
        print('monitor.py - program wrote by FX')
        print('Last modification: 02-may-2020')
        print('Verbosity mode turned on')
        print('Press Ctrl+C to exit!')
        print('Brightness: '+str(args.brightness))
        print('CPU temperature: '+str(temp))
        print('Rotate: '+str(args.rotate))
        print('Interval: '+str(args.interval))
        print('Number of docker containers running: '+str(nb_containers))
    scrollphat.set_rotate(args.rotate)
    scrollphat.set_brightness(args.brightness)

    prev_temp = 0
    prev_load = 0
    prev_nb_containers = 0
    while True:
        try:
            # Display the temperature
            temp = get_cpu_temperature()
            if (temp>prev_temp):
                for x in range(int(temp/80*11)):
                    scrollphat.set_pixel(x,args.temperature,1)
            elif (temp<prev_temp):
                for x in range(int(temp/80*11),int(prev_temp/80*11)):
                    scrollphat.set_pixel(x,args.temperature,0)
            prev_temp = temp
            # Display the cpu load
            load = psutil.cpu_percent()
            if (load>prev_load):
                for x in range(int(load/100*11)):
                    scrollphat.set_pixel(x,args.cpu,1)
            elif (load<prev_load):
                for x in range(int(load/100*11),int(prev_load/100*11)):
                    scrollphat.set_pixel(x,args.cpu,0)
            prev_load = load
            # Display the number of containers running
            nb_containers = len(client.containers.list())
            if (nb_containers>prev_nb_containers):
                for x in range(int(nb_containers)):
                    scrollphat.set_pixel(x,args.docker,1)
            elif (nb_containers<prev_nb_containers):
                for x in range(int(nb_containers),int(prev_nb_containers)):
                    scrollphat.set_pixel(x,args.docker,0)
            prev_nb_containers = nb_containers
            scrollphat.update()
            time.sleep(args.interval)
        except KeyboardInterrupt:
            # shut off pixels and exit
            scrollphat.clear()
            sys.exit(-1)
