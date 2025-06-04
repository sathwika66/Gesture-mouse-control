import cv2
import time
import numpy as np
import autopy

import gesture_detection as ht
import mouse_actions as ma
import config

# ----------------------- Variable Declarations -----------------------
prev_x, prev_y = 0, 0
curr_x, curr_y = 0, 0
pTime = 0

# ----------------------- Setup -----------------------
cap = cv2.VideoCapture(0)
cap.set(3, config.CAM_WIDTH)
cap.set(4, config.CAM_HEIGHT)

detector = ht.handDetector(maxHands=1)
screen_width, screen_height = autopy.screen.size()

# ----------------------- Main Loop -----------------------
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist, _ = detector.findPosition(img)

    if lmlist:
        x1, y1 = lmlist[8][1:]  # Index tip
        x2, y2 = lmlist[12][1:]  # Middle tip
        fingers = detector.fingersUp()

        # Draw rectangle boundary
        cv2.rectangle(img, (config.FRAME_MARGIN, config.FRAME_MARGIN),
                      (config.CAM_WIDTH - config.FRAME_MARGIN, config.CAM_HEIGHT - config.FRAME_MARGIN),
                      (255, 0, 255), 2)

        # ----------------------- Move Mouse -----------------------
        # Convert the index fingertip coordinates (x1, y1) from the webcam's video frame into screen coordinates so you can control the mouse pointer.
        # Let’s say:
        #       Camera width is 640, height is 480
        #       Frame margin is 100
        #       Screen width is 1920, height is 1080
        #     Then:
        #       Index finger moves from [100, 540] on webcam → [0, 1920] on screen (X-axis)
        #       And from [100, 380] → [0, 1080] (Y-axis)
        if fingers[1] == 1 and fingers[2] == 0:
            x3 = np.interp(x1, (config.FRAME_MARGIN, config.CAM_WIDTH - config.FRAME_MARGIN), (0, screen_width))
            y3 = np.interp(y1, (config.FRAME_MARGIN, config.CAM_HEIGHT - config.FRAME_MARGIN), (0, screen_height))

            curr_x, curr_y = ma.move_mouse(x3, y3, prev_x, prev_y, config.SMOOTHENING, screen_width)
            cv2.circle(img, (x1, y1), 7, (255, 0, 255), cv2.FILLED)
            prev_x, prev_y = curr_x, curr_y

        # ----------------------- Left Click -----------------------
        if fingers[1] == 1 and fingers[2] == 1:  # fingers[1] corresponds to indexfinger LM8
            length, img, lineInfo = detector.findDistance(8, 12, img)
            if length < 40:
                ma.left_click(img, lineInfo)

        # ----------------------- Right Click -----------------------
        if fingers[0] == 1 and fingers[1] == 1:    # fingers[0] is thumb and [1] is index fing
            length, img, lineInfo = detector.findDistance(4, 8, img)
            if length < 40:
                ma.right_click(img, lineInfo)

        # ----------------------- ESC Key (Only thumb down) -----------------------
        if fingers == [0, 1, 1, 1, 1]:
            ma.press_esc(img)

        # # ----------------------- Exit (Only thumb down) -----------------------
        if fingers == [1, 1, 1, 1, 1]:
            thumb_tip = lmlist[4]   # Landmark 4
            thumb_base = lmlist[3]  # Landmark 2

            # Check if thumb is extended horizontally (x difference high, y difference low)
            # if abs(thumb_tip[1] - thumb_base[1]) > 50 and abs(thumb_tip[2] - thumb_base[2]) < 40:
            if abs(thumb_tip[2] > thumb_base[2]):
                ma.exit_program(img)
                break
    # ----------------------- FPS -----------------------
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    # ----------------------- Show Window -----------------------
    cv2.imshow("Virtual Mouse", img)
    cv2.waitKey(1)
