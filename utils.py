#!/usr/bin/python3

import time
import cv2
import numpy as np

##### LOGGING FUNCTIONS ###############################################################
def display_total_time(start_time,title=''):
    stop_time = time.time() - start_time
    print("\tTotal {:} Time: {:.5f}s".format(title, stop_time))