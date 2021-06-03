import math
import mediapipe as mp
import cv2

class SimpleGestureDetector:
    # region: Member variables
    # mediaPipe configuration hands object
    __mpHands = mp.solutions.hands
    # mediaPipe detector objet
    __mpHandDetector = None

    def __init__(self):
        self.__setDefaultHandConfiguration()

    def __setDefaultHandConfiguration(self):
        self.__mpHandDetector = self.__mpHands.Hands(
            # default = 2
            max_num_hands=2,
            # Minimum confidence value ([0.0, 1.0]) from the landmark-tracking model for the hand landmarks to be considered tracked successfully (default= 0.5)
            min_detection_confidence=0.5,
            # Minimum confidence value ([0.0, 1.0]) from the hand detection model for the detection to be considered successful. (default = 0.5)
            min_tracking_confidence=0.5
        )


    def __getEuclideanDistance(self, posA, posB):
        return math.sqrt((posA.x - posB.x)**2 + (posA.y - posB.y)**2)

    def __isThumbNearIndexFinger(self, thumbPos, indexPos):
        return self.__getEuclideanDistance(thumbPos, indexPos) < 0.1


    def detectHands(self, capture):
        if self.__mpHandDetector is None:
            return

        image = capture.color
        # Input image must contain three channel rgb data.
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # lock image for hand detection
        image.flags.writeable = False
        # start handDetector on current image
        detectorResults = self.__mpHandDetector.process(image)
        # unlock image
        image.flags.writeable = True

        if detectorResults.multi_hand_landmarks:
            for handLandmarks in detectorResults.multi_hand_landmarks:
                self.simpleGesture(handLandmarks.landmark)

    def simpleGesture(self, handLandmarks):

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

        elif not status[2] and status[3] and status[4] and status[5] and self.__isThumbNearIndexFinger(handLandmarks[4], handLandmarks[8]):
            status['gesture'] = "OK!"

        return status

        # print("FingerState: status[1]? " + str(status[1]) + " - status[2]? " + str(status[2]) + " - status[3]? " +
        #        str(status[3]) + " - status[4]? " + str(status[4]) + " - status[5]? " + str(status[5]))