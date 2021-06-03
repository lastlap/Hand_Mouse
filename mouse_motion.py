import cv2
import numpy as np
import math

import mediapipe as mp
from utils import findPosition, findGesture

import pyautogui

import argparse

def main(args):

    pyautogui.FAILSAFE = False

    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands

    cap = cv2.VideoCapture(0)

    # check what resolutions are supported by webcam.

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    with mp_hands.Hands(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:

        move_list = []
        count = 0
        move_freq = args.move_freq
        status = {}
        motion_factor = args.motion_factor

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

                status = findGesture(results.multi_hand_landmarks[0].landmark)

                # text = ''.join([str(status[key])+'  ' for key in status])
                if 'gesture' in status:
                    image = cv2.putText(image,str(status['gesture']),(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(255, 0, 0),2,cv2.LINE_AA)

            if len(lmlist)!=0:
                count+=1
                move_list.append([lmlist[9][1],lmlist[9][2]])

                # the gesture of thumb,index and middle open and rest closed is used for motion

                if count%move_freq==0 and ('gesture' in status) and status['gesture']==5: #(status[1] and status[2] and status[3] and not status[4] and not status[5]):
                    pyautogui.moveRel(int((move_list[count-1][0]-move_list[count-move_freq][0])*motion_factor),int((move_list[count-1][1]-move_list[count-move_freq][1])*motion_factor),duration = args.duration)
                    

            if 'gesture' in status:
                # the gesture 5 clicks on position
                if status['gesture']==1:
                    psn = pyautogui.position()
                    pyautogui.click(psn.x,psn.y)
                # # the gesture 4 right clicks on position
                # elif status['gesture']==4:
                #     pyautogui.click(button='right')

            cv2.imshow('MediaPipe Hands', image)

            # press x to exit
            if cv2.waitKey(5) & 0xFF == ord('x'):
                break

    cap.release()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hand Mouse Parameters')
    
    parser.add_argument('--move_freq', type=int, default=4,
                    help='number of frames taken for position of mouse cursor to update')

    parser.add_argument('--motion_factor', type=float, default=1.5,
                    help='controls distance of motion of cursor')

    parser.add_argument('--duration', type=float, default=0.2,
                    help='controls time taken for single motion of cursor')


    args = parser.parse_args()
    main(args)