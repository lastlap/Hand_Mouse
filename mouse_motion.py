import cv2
import numpy as np
import math

import mediapipe as mp
from gesture_recognition import SimpleGestureDetector

import pyautogui

gesdet = SimpleGestureDetector()

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)


def findPosition(results,image):
    lmlist = []
    if results.multi_hand_landmarks:
        hand_1 = results.multi_hand_landmarks[0]
        for Id, lm in enumerate(hand_1.landmark):
            h, w, c = image.shape
            cx, cy = int(lm.x*w), int(lm.y*h)
            # print(Id,cx,cy)
            lmlist.append([Id,cx,cy])
            cv2.circle(image,(cx,cy),7,(255,0,255),cv2.FILLED)

    return lmlist, image


with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

    move_list = []
    count = 0
    move_freq = 5
    text = ''
    motion_factor = 2

    while cap.isOpened():
        
        ret, image = cap.read()

        if not ret:
            print('Empty frame')
            continue

        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        lmlist,image = findPosition(results,image)


        if results.multi_hand_landmarks:
            
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            text = gesdet.simpleGesture(results.multi_hand_landmarks[0].landmark)

            image = cv2.putText(image,text,(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(255, 0, 0),2,cv2.LINE_AA)

        if len(lmlist)!=0:
            count+=1
            # print(lmlist[9])
            move_list.append([lmlist[9][1],lmlist[9][2]])

            if count%move_freq==0 and text=='FIVE!':
                # print(move_list)
                try:
                    pyautogui.moveRel((move_list[count-1][0]-move_list[count-move_freq][0])*motion_factor,(move_list[count-1][1]-move_list[count-move_freq][1])*motion_factor,duration = 0.2)
                except:
                    pass
                # move_list = []
            # else:
            #     print(text)

        cv2.imshow('MediaPipe Hands', image)

        if cv2.waitKey(5) & 0xFF == ord('x'):
            break

cap.release()

