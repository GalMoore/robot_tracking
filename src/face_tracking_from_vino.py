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



def callback(data):
    global closed_lips_already
    global biggest_face
    global headPositionX
    global headPositionY
    global counter
    # print(data.objects_vector)
    # print(len(data.objects_vector))

    # if data.objects_vector[0]

    # if face found and it's wider than 170 pixel get coords
    # os.system("python3 /home/gal/catkin_ws/src/robot_face/src/headnod.py %s" %(str(headPositionX)))

    # print(counter)

    if len(data.objects_vector)==1 and \
    data.objects_vector[0].roi.width>120:

    # if len(data.objects_vector)==1:

        # print(data.objects_vector[0].roi.width)

        x = data.objects_vector[0].roi.x_offset
        y = data.objects_vector[0].roi.y_offset
        h = data.objects_vector[0].roi.height
        w = data.objects_vector[0].roi.width

        # headnod and position
        # os.system("python3 /home/gal/catkin_ws/src/robot_face/src/headnod.py 5")

        # print(x,y,h,w)

        circleX = 640/2
        circleY= 400/2
        BBcircleX= int(x+(w/2))
        BBcircleY= int(y+(h/2))

        # print(circleX)
        # print(circleY)
        # print(BBcircleX)
        # print(BBcircleY)

        # print("BBcircleX: " + str(BBcircleX))
        # print("circleX: " + str(circleX))
        if (counter%8==0):

            #  If you go LEFT
            if BBcircleX > circleX+120:
                if headPositionX >1:
                    headPositionX = headPositionX-1
                    print("Im here!")
                    # ohbot.move(ohbot.HEADTURN,headPositionX,1)
                    os.system("python3 /home/gal/catkin_ws/src/robot_face/src/headturn.py %s" %(str(headPositionX)))

                    # ohbot.wait(0.)

            #  If you go RIGHT
            if BBcircleX < circleX-120:
                if headPositionX <9:
                    headPositionX = headPositionX+1
                    os.system("python3 /home/gal/catkin_ws/src/robot_face/src/headturn.py %s" %(str(headPositionX)))
                    # ohbot.move(ohbot.HEADTURN,headPositionX,1)
                    # ohbot.wait(3)

            # If you go UP
            if BBcircleY < circleY-100:
                if headPositionY <9:
                    headPositionY = headPositionY+3
                    # os.system("python3 /home/gal/catkin_ws/src/robot_face/src/headnod.py %s" %(str(headPositionX)))
                    # ohbot.move(ohbot.HEADNOD,headPositionY,1)
                    # ohbot.wait(3)

            #  If you go Down
            if BBcircleY > circleY+100:
                if headPositionY >1:
                    headPositionY = headPositionY-1
                    # os.system("python3 /home/gal/catkin_ws/src/robot_face/src/headnod.py %s" %(str(headPositionX)))

                    # ohbot.move(ohbot.HEADNOD,headPositionY,1)
                    # ohbot.wait(3)


        # move motors with this (arg 1, arg 2)
        # os.system("python3 /home/gal/catkin_ws/src/robot_face/src/go_left.py 4 6")





    else:
        "nope"

    counter = counter +1




    # # if no faces found = close lips
    # if len(data.objects_vector)==0 and closed_lips_already!=True:
    #     python_bin3 = "/usr/bin/python3"
    #     subprocess.Popen([python_bin3, "/home/gal/catkin_ws/src/robot_face/src/close_lips.py"]).wait()
    #     closed_lips_already = True



    # # if more than one face = open lips
    # elif len(data.objects_vector)>=1:
    #     python_bin3 = "/usr/bin/python3"
    #     subprocess.Popen([python_bin3, "/home/gal/catkin_ws/src/robot_face/src/open_lips.py"]).wait()
    #     closed_lips_already = False

    # else:
    #     pass






def track_vino():
    print("hello")
    # RESET ROBOT BEFORE START
    # ohbot.move(ohbot.HEADTURN,headPositionX,1)
    # ohbot.move(ohbot.HEADNOD,headPositionY,1)
    # ohbot.move(ohbot.EYETURN,5,1)
    os.system("python3 /home/gal/catkin_ws/src/robot_face/src/headturn.py %s" %(str(5)))
    time.sleep(1)
    os.system("python3 /home/gal/catkin_ws/src/robot_face/src/headnod.py %s" %(str(9)))
    rospy.Subscriber("/ros_openvino_toolkit/face_detection", ObjectsInBoxes, callback)
    rospy.spin()



if __name__ == '__main__':
    rospy.init_node('robot_tracking_from_vino')
    track_vino()


