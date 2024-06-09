import cv2
from time import sleep
from pynput.keyboard import Controller
from cvzone.HandTrackingModule import HandDetector

width, height = 1280, 720
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)
t1, t2 = 0, 0

keyboard = Controller()
detector = HandDetector(detectionCon=0.8, maxHands=1)
typed_string = ""
alphabets = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
             ["A", "S", "D", "F", "G", "H", "J", "K", "L", 'era'],
             ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "sp"]]

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)
    if hands:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        if fingers[0] == 0:
            fingers[0] = 1
        else:
            fingers[0] = 0
    xst, yst = 23, 23
    lmlist = detector.lmList
    for i in range(3):
        for j in range(10):
            img = cv2.rectangle(img, (xst, yst), (xst+80, yst+80), (170, 51, 106), -1)
            img = cv2.putText(img, alphabets[i][j], (xst+40, yst+40),
                              cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
            xst = xst+80+23
        xst = 23
        yst = yst+32+80
    if len(lmlist) > 0:
        x1, y1 = lmlist[8][0], lmlist[8][1]
        x2, y2 = lmlist[12][0], lmlist[12][1]
        length, info = detector.findDistance((x1, y1),
                                             (x2, y2))
        x3, y3 = (x1+x2)/2, (y1+y2)/2
        x3, y3 = int(x3), int(y3)
        img = cv2.circle(img, (x3, y3), 10, (255, 0, 0), 2)
        img = cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)
        if length < 40:
            xs, ys = 23, 23
            for i in range(3):
                for j in range(10):
                    if (x3 < (xs+80)) and (x3 > xs) and (y3 < ys+80) and (y3 > ys):
                        img = cv2.rectangle(img, (xs, ys), (xs + 80, ys + 80), (255, 51, 106), -1)
                        if alphabets[i][j] == "sp":
                            typed_string = typed_string + " "
                            keyboard.press(" ")
                        elif alphabets[i][j] == "era":
                            typed_string = typed_string[0:len(typed_string)-2]
                        else:
                            typed_string = typed_string + alphabets[i][j]
                            keyboard.press(alphabets[i][j])
                        sleep(0.15)
                    xs = xs + 80 + 23
                xs = 23
                ys = ys + 32 + 75
        img = cv2.putText(img, typed_string, (100, 500), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255))

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break
