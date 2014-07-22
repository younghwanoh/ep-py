#!/usr/bin/python

import os
from time import sleep

tests = ["line-key","line-raw","line-norm","getter-test"]

for i in tests:
    print("\033[1;31m%s\033[m test !! ============================================" % i)
    os.system('./ep.py -s %s' % i)
    print("\033[0;34mfinish !! ============================================\033[m")
    sleep(1)

