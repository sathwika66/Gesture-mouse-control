# Import necessary libraries
import cv2  # OpenCV for image processing and video capture
import mediapipe as mp  # MediaPipe for hand tracking
import time  # To calculate and display FPS
import math  # To calculate Euclidean distance
import numpy as np  # Used here for potential numerical operations

# Class for detecting and tracking hands using MediaPipe
class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=False, trackCon=0.5):
        """
        Initializes hand detection module with configuration.
        :param mode: Static image mode if True, otherwise video mode
        :param maxHands: Maximum number of hands to detect
        :param detectionCon: Minimum detection confidence threshold
        :param trackCon: Minimum tracking confidence threshold
        """
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        # Initialize MediaPipe hands module
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils  # Utility to draw hand landmarks
        self.tipIds = [4, 8, 12, 16, 20]  # Landmark indices for fingertips

    def findHands(self, img, draw=True):
        """
        Processes the image and draws hand landmarks if found.
        :param img: Input image (BGR)
        :param draw: Whether to draw landmarks on image
        :return: Processed image with or without drawings
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB for MediaPipe
        self.results = self.hands.process(imgRGB)  # Process the frame for hands

        # If hands are detected, draw them
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, handNo=0, draw=True):
        """
        Finds the positions of landmarks in the given hand.
        :param img: Input image
        :param handNo: Index of the hand (0 for first hand)
        :param draw: Whether to draw landmarks and bounding box
        :return: List of landmarks and bounding box around hand
        """
        xList = []
        yList = []
        bbox = []
        self.lmList = []

        # If landmarks detected
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]

            # Loop through landmarks and convert normalized coords to pixel
            #This block extracts, converts, stores, and optionally visualizes the hand landmarks from a MediaPipe detection result.
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)  # Convert to pixel coordinates
                xList.append(cx)
                yList.append(cy)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

            # Create bounding box around the hand
            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            bbox = xmin, ymin, xmax, ymax

            if draw:
                cv2.rectangle(img, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20),
                              (0, 255, 0), 2)

        return self.lmList, bbox

    def fingersUp(self):
        """
        Determines which fingers are up.
        :return: List of 0s and 1s for each finger (1 means finger is up)
        """
        fingers = []

        # Thumb (check x position because it opens sideways)
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Other four fingers (check y position - if tip is above knuckle, it's up)
        for id in range(1, 5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers

    def findDistance(self, p1, p2, img, draw=True, r=15, t=3):
        """
        Calculates the distance between two landmarks.
        :param p1: Index of first landmark
        :param p2: Index of second landmark
        :param img: Input image
        :param draw: Whether to draw line and points
        :param r: Radius of the circles
        :param t: Thickness of the line
        :return: Distance, modified image, and list of point coordinates
        """
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2  # Midpoint

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)  # Euclidean distance
        return length, img, [x1, y1, x2, y2, cx, cy]


# Main function for real-time video capture and hand detection
def main():
    pTime = 0  # Previous timestamp for FPS calculation
    cTime = 0  # Current timestamp

    cap = cv2.VideoCapture(1)  # Capture from webcam (device 1)
    detector = handDetector()

    while True:
        success, img = cap.read()  # Read frame from webcam
        img = detector.findHands(img)  # Detect hands
        lmList, bbox = detector.findPosition(img)  # Get landmarks

        if len(lmList) != 0:
            print(lmList[4])  # Print coordinates of landmark ID 4 (usually thumb tip)

        # Calculate and display FPS
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)

        # Display the frame
        cv2.imshow("Image", img)
        cv2.waitKey(1)


# Entry point of the script
if __name__ == "__main__":
    main()
