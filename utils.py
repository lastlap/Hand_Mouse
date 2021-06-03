import cv2
import math

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

def getEuclideanDistance(posA, posB):
    return math.sqrt((posA.x - posB.x)**2 + (posA.y - posB.y)**2)

def isThumbNearIndexFinger(thumbPos, indexPos):
    return getEuclideanDistance(thumbPos, indexPos) < 0.1

def findGesture(handLandmarks):

    status = {1:False,2:False,3:False,4:False,5:False}

    status[1] = False # Open thumb
    status[2] = False # Open index
    status[3] = False # Open middle
    status[4] = False # Open ring
    status[5] = False # Open pinky

    pseudoFixKeyPoint = handLandmarks[2].x
    if handLandmarks[3].x < pseudoFixKeyPoint and handLandmarks[4].x < pseudoFixKeyPoint:
        status[1] = True

    pseudoFixKeyPoint = handLandmarks[6].y
    if handLandmarks[7].y < pseudoFixKeyPoint and handLandmarks[8].y < pseudoFixKeyPoint:
        status[2] = True

    pseudoFixKeyPoint = handLandmarks[10].y
    if handLandmarks[11].y < pseudoFixKeyPoint and handLandmarks[12].y < pseudoFixKeyPoint:
        status[3] = True      

    pseudoFixKeyPoint = handLandmarks[14].y
    if handLandmarks[15].y < pseudoFixKeyPoint and handLandmarks[16].y < pseudoFixKeyPoint:
        status[4] = True           

    pseudoFixKeyPoint = handLandmarks[18].y
    if handLandmarks[19].y < pseudoFixKeyPoint and handLandmarks[20].y < pseudoFixKeyPoint:
        status[5] = True

    if status[1] and status[2] and status[3] and status[4] and status[5]:
        status['gesture'] = 5

    elif not status[1] and status[2] and status[3] and status[4] and status[5]:
        status['gesture'] = 4

    elif not status[1] and status[2] and status[3] and status[4] and not status[5]:
        status['gesture'] = 3

    elif not status[1] and status[2] and status[3] and not status[4] and not status[5]:
        status['gesture'] = 2

    elif not status[1] and status[2] and not status[3] and not status[4] and not status[5]:
        status['gesture'] = 1

    elif not status[1] and status[2] and not status[3] and not status[4] and status[5]:
        status['gesture'] = 'ROCK!'

    elif status[1] and status[2] and not status[3] and not status[4] and status[5]:
        status['gesture'] = "SPIDERMAN!"

    elif not status[1] and not status[2] and not status[3] and not status[4] and not status[5]:
        status['gesture'] = "FIST!"

    elif not status[2] and status[3] and status[4] and status[5] and isThumbNearIndexFinger(handLandmarks[4], handLandmarks[8]):
        status['gesture'] = "OK!"

    return status