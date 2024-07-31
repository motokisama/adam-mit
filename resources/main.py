# initialize
import sys
import math
import copy
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
import statistics
from nptyping import NDArray
from typing import Any, Tuple, List, Optional
from enum import Enum
import matplotlib.pyplot as plt

from wallfollow import *
from linefollow import *
from mode_manage import * 


sys.path.insert(1, '../../library')
import racecar_core
import racecar_utils as rc_utils

rc = racecar_core.create_racecar()

#################
#variables
#################

mode = 99

#wallfollow
kp_angle = 0.01
ki_angle = 0.005
kd_angle = 0.005
kp_dist = 0.01
ki_dist = 0.005
kd_dist = 0.005

goal_dist = 50
wall_speed = 0.8

#linefollow
kp_insec = 0.01
ki_insec = 0.005
kd_insec = 0.005
kp_gap = -0.8
ki_gap= 0.0
kd_gap = 0.0

line_speed = 0.8

BLUE_LINE = ((58, 98, 143), (158, 255, 255))
GREEN_LINE = ((50, 131, 173), (103, 255, 255))  # The HSV range for the color green
RED_LINE = ((0, 105, 94), (18, 255,255))
LINE_PRIORITY = (GREEN_LINE, BLUE_LINE, RED_LINE)

UPPER_CROP = ((360,0),(420, 640))
LOWER_CROP = ((420, 0), (480, 640))

################
#PID object
################
wallfollow = WallFollow(rc, kp_angle, ki_angle, kd_angle, kp_dist, ki_dist, kd_dist, wall_speed, goal_dist)
linefollow = LineFollow(kp_insec, ki_insec, kd_insec, kp_gap, ki_gap, kd_gap, line_speed, LINE_PRIORITY, UPPER_CROP, LOWER_CROP)


def start():
    pass

def update():

    global mode
    mode_dict = {0:"wallfollow",2:"linefollow", 99:"No AR Marker"}
    image = rc.camera.get_color_image()
    mode, square = detect_marker(image)

    if image is None:
        print("no image")
        speed, angle = 0,0

    else:
        if mode == 0:
            speed, angle = wallfollow.update()

        elif mode == 99:
            speed, angle = linefollow.update(image)
    
        print(f"mode:{mode_dict[mode]}")
        #print(f"marker square: {square}")

    
    print()
    print(f"speed:{speed}")
    print(f"angle:{angle}")
    print()
    

    
    rc.drive.set_speed_angle(speed, angle)
    
# update slow
def update_slow():
    pass


if __name__ == "__main__":
    rc.set_start_update(start, update, update_slow)
    rc.go()


