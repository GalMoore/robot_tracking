#!/usr/bin/env python
# Software License Agreement (BSD License)

# import sys
# sys.path.insert(0, '/home/gal/dlib')
# import face_recognition
# import cv2
# from ohbot import ohbot
import time 
import rospy
from object_msgs.msg import ObjectsInBoxes
import subprocess
import os

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


    # if no detections at all - straighten head
    if (len(data.objects_vector)==0):
        print(counter_two)
        print("no objects at all!")
        counter_two = counter_two +1
        if counter_two>when_reach_this_counter_two_num_centre_face:
            os.system("python3 /home/gal/catkin_ws/src/robot_face/src/headturn.py %s" %(str(5)))
            headPositionX = 5
            counter_two = 0


    # reset counter_three
    counter_three = 0

    # check if one of the found classes if person
    for i in range(len(data.objects_vector)):
        if data.objects_vector[i].object.object_name !="person":
            counter_three = counter_three +1
            # print(counter_three)
            if counter_three==len(data.objects_vector):
                print(counter_two)
                print("NO PERSON")
                counter_two = counter_two +1
                if counter_two>when_reach_this_counter_two_num_centre_face:
                    os.system("python3 /home/gal/catkin_ws/src/robot_face/src/headturn.py %s" %(str(5)))
                    headPositionX = 5
                    counter_two = 0

            
    # iterate through objects found and track a person (any person)
    for i in range(len(data.objects_vector)):

        # print("object index: " + str(i))
        # print("object name: " + str(data.objects_vector[i].object.object_name))

        if data.objects_vector[i].object.object_name == "person":
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
                        os.system("python3 /home/gal/catkin_ws/src/robot_face/src/headturn.py %s" %(str(headPositionX)))


                #  If you go RIGHT
                if BBcircleX < circleX-50:
                    if headPositionX <9:
                        headPositionX = headPositionX+0.2
                        os.system("python3 /home/gal/catkin_ws/src/robot_face/src/headturn.py %s" %(str(headPositionX)))

                # # If you go UP
                # if BBcircleY < circleY-150:
                #     if headPositionY <9:
                #         headPositionY = headPositionY+0.1
                #         os.system("python3 /home/gal/catkin_ws/src/robot_face/src/headnod.py %s" %(str(headPositionY)))
                #         # ohbot.move(ohbot.HEADNOD,headPositionY,1)
                #         # ohbot.wait(3)

                # #  If you go Down
                # if BBcircleY > circleY+150:
                #     if headPositionY >1:
                #         headPositionY = headPositionY-0.1
                #         os.system("python3 /home/gal/catkin_ws/src/robot_face/src/headnod.py %s" %(str(headPositionY)))

                        # ohbot.move(ohbot.HEADNOD,headPositionY,1)
                        # ohbot.wait(3)

        # all objects recognized but not person will go here
        # even when person is identified
        else:
            pass

        # counter will run at somewhere between 15 and 70 fps
        counter = counter +1


def track_vino():
    print("hello")
    os.system("python3 /home/gal/catkin_ws/src/robot_face/src/headturn.py %s" %(str(5)))
    time.sleep(1)
    os.system("python3 /home/gal/catkin_ws/src/robot_face/src/headnod.py %s" %(str(3)))
    time.sleep(1)
    os.system("python3 /home/gal/catkin_ws/src/robot_face/src/eyes.py %s" %(str(5))) 
    rospy.Subscriber("/ros_openvino_toolkit/detected_objects", ObjectsInBoxes, callback)
    rospy.spin()


if __name__ == '__main__':
    rospy.init_node('robot_tracking_from_vino')
    track_vino()


