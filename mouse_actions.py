import autopy
import time
import cv2

def move_mouse(x, y, prev_x, prev_y, smoothening, screen_width):
    curr_x = prev_x + (x - prev_x) / smoothening
    curr_y = prev_y + (y - prev_y) / smoothening
    autopy.mouse.move(screen_width - curr_x, curr_y)
    return curr_x, curr_y

def left_click(img, lineInfo):
    cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
    autopy.mouse.click()

def right_click(img, lineInfo):
    cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 0, 255), cv2.FILLED)
    autopy.mouse.click(button=autopy.mouse.Button.RIGHT)

def press_esc(img):
    cv2.putText(img, "ESC Triggered", (400, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
    autopy.key.tap(autopy.key.Code.ESCAPE)
    time.sleep(0.5)

def exit_program(img):
    cv2.putText(img, "Exiting...", (400, 90), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
    # cv2.imshow("Exit Gesture Detected", img)
    cv2.waitKey(1000)
    time.sleep(0.5)
