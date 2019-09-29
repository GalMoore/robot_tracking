#!/usr/bin/env python
# Software License Agreement (BSD License)

import time 
import rospy
from object_msgs.msg import ObjectsInBoxes
import subprocess
import os
from std_msgs.msg import String
from os.path import expanduser
home = expanduser("~") + "/"
import requests
import math
import random 
import time
from random import randrange

closed_lips_already = False
biggest_face = 0
headPositionX = 5
headPositionY = 5
counter = 0
object_index_to_track = 0
no_person_start_time = True
counter_two = 0
array_count_person_in_vector = []
counter_three = 0
when_reach_this_counter_two_num_centre_face = 500
pub = rospy.Publisher('is_person_nearby', String, queue_size=10)
threshold_width = 400
thresh_found = 0

message = "http://127.0.0.1:8081/motor={}?position={}?speed={}"

def callback(data):
    global closed_lips_already
    global biggest_face
    global headPositionX
    global headPositionY
    global counter
    global object_index_to_track
    global start
    global no_person_start_time 
    global counter_two
    global counter_three
    global threshold_width
    global thresh_found

    # if no detections at all - straighten head
    if (len(data.objects_vector)==0):
        counter_two = counter_two +1
        if counter_two>when_reach_this_counter_two_num_centre_face:
            requests.get(message.format(1,5,1))
            headPositionX = 5
            counter_two = 0

    # reset counter_three
    counter_three = 0

    # check if one of the found classes is person
    for i in range(len(data.objects_vector)):
        if data.objects_vector[i].object.object_name !="person":
            counter_three = counter_three +1
            if counter_three==len(data.objects_vector):
                counter_two = counter_two +1
                if counter_two>when_reach_this_counter_two_num_centre_face:
                    requests.get(message.format(1,5,1))
                    time.sleep(1)
                    requests.get(message.format(0,5,1))
                    time.sleep(1)
                    requests.get(message.format(2,5,1))
                    headPositionX = 5
                    counter_two = 0

    # iterate through objects found and track a person (any person)
    for i in range(len(data.objects_vector)):

        if data.objects_vector[i].object.object_name == "person" and data.objects_vector[i].roi.width >125 and data.objects_vector[i].roi.height >200 :   

            counter_two = 0
            # if current object is person follow it
            x = data.objects_vector[i].roi.x_offset
            y = data.objects_vector[i].roi.y_offset
            h = data.objects_vector[i].roi.height
            w = data.objects_vector[i].roi.width

            # grab dimensions of image and create circle in middle of frame
            circleX = 640/2
            circleY= 400/2
            # create circle in centre of bounding box
            BBcircleX= int(x+(w/2))
            BBcircleY= int(y+(h/2))

            # only X times per second
            if (counter%10==0):

                #  If you go LEFT
                if BBcircleX > circleX+50:
                    if headPositionX >1:
                        headPositionX = headPositionX-0.2
                        requests.get(message.format(1,headPositionX,1))

                #  If you go RIGHT
                if BBcircleX < circleX-50:
                    if headPositionX <9:
                        headPositionX = headPositionX+0.2
                        requests.get(message.format(1,headPositionX,1))

                # # If you go UP
                # if BBcircleY < circleY-50:
                #     if headPositionY <9:
                #         headPositionY = headPositionY+0.5
                #         requests.get(message.format(0,headPositionY,1))

                # # #  If you go Down
                # if BBcircleY > circleY+50:
                #     if headPositionY >1:
                #         headPositionY = headPositionY-0.5
                #         requests.get(message.format(0,headPositionY,1))

                #  check if any of th persons found are bigger than threshold width - than
                #  we will launch face detection instead of object detcetion that will filter  out small faces
                if w>threshold_width:
                    thresh_found = thresh_found +1
                    # print(thresh_found)
                    if thresh_found == 40:
                        pub.publish("yes")

                else:
                    pub.publish("no")
                    thresh_found = 0
                    # print(thresh_found)

        else:
            pass

        # counter will run at somewhere between 15 and 70 fps
        counter = counter +1

def track_vino():
    print("hello")
    requests.get(message.format(1,5,1))
    time.sleep(1)
    requests.get(message.format(0,5,1))
    time.sleep(1)
    requests.get(message.format(2,5,1))
    rospy.Subscriber("/ros_openvino_toolkit/detected_objects", ObjectsInBoxes, callback)
    rospy.spin()


if __name__ == '__main__':
    rospy.init_node('robot_object_tracking_from_vino')
    track_vino()


