#!/usr/bin/env python

import time 

def run():
    while True:
        time.sleep(1)
#        cur = time.time()
#        print("current time: %4.2f" % cur)

    print("terminated")


def stop():
    print("stop scenario running")


run();
stop();
   
