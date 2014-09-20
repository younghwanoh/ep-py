#!/usr/bin/python

import os
from time import sleep
import sys

tests = ["line-key","line-raw","line-flat","line-norm","pie","bar-clustered",
         "bar-norm-clustered","bar-key-clustered","bar-stacked","bar-clustacked",
         "bar-stacked-trans","bar-key-cc","bar-single", "box-key","box-time",
         "cbp+lp","cbp+sbp+line","box-multi-time","jaws","getter-test"]

additional_tests = ["sc-bar", "cbar-line"]

for i in tests:
    print("\033[1;31m%s\033[m test !! ============================================" % i)
    os.system('./examples.py -s %s -o %s.pdf' % (i,i))
    print("\033[0;34mfinish !! ============================================\033[m")
    sleep(1)

for i in additional_tests:
    print("\033[1;31m%s\033[m test !! ============================================" % i)
    os.system('./%s.py' % i)
    print("\033[0;34mfinish !! ============================================\033[m")
    sleep(1)
