#!/usr/bin/env python
# Software License Agreement (BSD License)

import sys
sys.path.insert(0, '/home/gal/dlib')
import face_recognition
import cv2
from ohbot import ohbot
import time 

def facetrackingandrecognition(whoToFollow):

    headPositionX = 5
    headPositionY = 5
    ohbot.move(ohbot.HEADTURN,headPositionX,1)
    ohbot.move(ohbot.HEADNOD,headPositionY,1)
    ohbot.move(ohbot.EYETURN,5,1)

    video_capture = cv2.VideoCapture(1)

    # Load a sample picture and learn how to recognize it.
    miriam_image = face_recognition.load_image_file("/home/gal/catkin_ws/src/robot_tracking/face_images_for_tracking/miriam.jpg")
    miriam_face_encoding = face_recognition.face_encodings(miriam_image)[0]

    # Load a second sample picture and learn how to recognize it.
    gal_image = face_recognition.load_image_file("/home/gal/catkin_ws/src/robot_tracking/face_images_for_tracking/gal.jpg")
    gal_face_encoding = face_recognition.face_encodings(gal_image)[0]

    # Load a third sample picture and learn how to recognize it.
    amit_image = face_recognition.load_image_file("/home/gal/catkin_ws/src/robot_tracking/face_images_for_tracking/amit.jpg")
    amit_face_encoding = face_recognition.face_encodings(amit_image)[0]

        # Load a fourth sample picture and learn how to recognize it.
    arielle_image = face_recognition.load_image_file("/home/gal/catkin_ws/src/robot_tracking/face_images_for_tracking/arielle.jpg")
    arielle_face_encoding = face_recognition.face_encodings(arielle_image)[0]


    # Create arrays of known face encodings and their names
    known_face_encodings = [
        miriam_face_encoding,
        gal_face_encoding,
        amit_face_encoding,
        arielle_face_encoding
    ]
    known_face_names = [
        "Miriam",
        "Gal",
        "Amit",
        "Arielle"
    ]

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    counter = 0



####################################################
###### FROM HERE TILL BOTTOM ONE FUNCTION #########
####################################################

    while True:

        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame


        # IF KNOWN PERSON FOUND:FOlLOW THAT PERSON
        # top right bottom and left are coordinates of the face found

        # WHEN FACE FOUND THE FOR LOOP IS CALLED
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            counter = counter +1
            print(counter)

            # we dont want to take every single frame because it makes robot jump from side to side

            if (counter%3==0):

                if name==whoToFollow:

                    #  PROCESS_THIS_FRAME MAKES SURE YOU ONLY TAKE EVERY OTHER FRAME
                    #  SO IT BECOMES A CONDITION HERE TOO
                    #  IF NOT THAN YOU TWICE CHECK THE SAME IMAGE AND GET DOUBLE UP OF OHBOT MOVEMENT
                        # print(process_this_frame)

                    # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4

                    # Draw a box around each face
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                    # Draw a label with a name below the face
                    # cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, name, (left + 30, top - 30), font, 3.0, (0, 0, 255), 3)


                    #  AND TRACK THE FACE WITH OHBOT MOTORS! EVERY SECOND TIME ONLY
                    # 1280 x 800 
                        #  Centre point of screen is: x= 640, y = 400
                        #  Draw circle in middle of screen
                    # print(face_names)
                    # if face_names==['Gal']:

                    circleX = int(640)
                    circleY= int(400)

                    # Draw circle of centre of screen onto visualisation
                    cv2.circle(frame,(circleX,circleY),13,(255,0,255),-1)

            # IN PREVIOUS SCRIPT: cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            # IN THIS SCRIPT:      cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                    w = right-left
                    h = bottom-top

                    BBcircleX= int(left+(w/2))
                    BBcircleY= int(top+(h/2))

                        # print ("bb circleX " + str(BBcircleX))

                    # Draw circle of centre of face being tracked onto visualisation
                    cv2.circle(frame,(BBcircleX,BBcircleY),13,(0,0,255),-1)

                    #  If you go LEFT
                    if BBcircleX > circleX+250 and process_this_frame:
                        if headPositionX >1:
                            headPositionX = headPositionX-1
                            ohbot.move(ohbot.HEADTURN,headPositionX,1)
                            # ohbot.wait(0.)

                    #  If you go RIGHT
                    if BBcircleX < circleX-250 and process_this_frame:
                        if headPositionX <9:
                            headPositionX = headPositionX+1
                            ohbot.move(ohbot.HEADTURN,headPositionX,1)
                            # ohbot.wait(3)

                    # If you go UP
                    if BBcircleY < circleY-200 and process_this_frame:
                        if headPositionY <9:
                            headPositionY = headPositionY+3
                            ohbot.move(ohbot.HEADNOD,headPositionY,1)
                            # ohbot.wait(3)

                    #  If you go Down
                    if BBcircleY > circleY+200 and process_this_frame:
                        if headPositionY >1:
                            headPositionY = headPositionY-1
                            ohbot.move(ohbot.HEADNOD,headPositionY,1)
                            # ohbot.wait(3)

                else:
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4

                    # Draw a box around each face
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                    # Draw a label with a name below the face
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, name, (left + 30, top - 30), font, 3.0, (255, 255, 255), 3)



        cv2.namedWindow("facetrkVideo", cv2.WINDOW_NORMAL)
        frame = cv2.resize(frame, (640,360))
        cv2.imshow('facetrkVideo', frame)

        # Display the resulting image
        # cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()




################ RUN FUCNTION FROM HERE######################
#Tell function who to follow (Gal / Miriam / Arielle / Amit)


# if __name__ == '__main__':
#     rospy.init_node('robot_ears_node')
facetrackingandrecognition("Gal")


