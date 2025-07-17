#!/usr/bin/env python3
"""
Very small background‑subtraction vehicle detector.
Usage:
    python vehicle_detection.py --video path/to/traffic.mp4
or python vehicle_detection.py             # webcam
"""
import cv2
import imutils
import argparse
from collections import deque

# ---------- argument parsing ----------
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to video file (omit for webcam)")
ap.add_argument("-m", "--min-area", type=int, default=700,
                help="skip small contours under this area (pixels)")
args = ap.parse_args()

# ---------- video source ----------
cap = cv2.VideoCapture(args.video if args.video else 0)
if not cap.isOpened():
    raise SystemExit("❌  Could not open video source.")

# ---------- background subtractor ----------
bgs = cv2.createBackgroundSubtractorMOG2(history=500,
                                         varThreshold=40,
                                         detectShadows=True)

trail = deque(maxlen=20)          # keeps recent centroids for a blue trail

while True:
    ret, frame = cap.read()
    if not ret:
        break                     # end of file or camera error

    frame = imutils.resize(frame, width=900)
    mask  = bgs.apply(frame)                      # raw foreground
    mask  = cv2.medianBlur(mask, 5)               # speckle noise
    _, mask = cv2.threshold(mask, 200, 255, cv2.THRESH_BINARY)
    mask  = cv2.morphologyEx(mask, cv2.MORPH_OPEN,
                             cv2.getStructuringElement(cv2.MORPH_RECT,(3,3)), 2)
    mask  = cv2.morphologyEx(mask, cv2.MORPH_CLOSE,
                             cv2.getStructuringElement(cv2.MORPH_RECT,(15,15)), 2)
    mask  = cv2.dilate(mask,
                       cv2.getStructuringElement(cv2.MORPH_RECT,(5,5)), 2)

    cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    for c in cnts:
        if cv2.contourArea(c) < args.min_area:   # ignore tiny blobs
            continue
        x, y, w, h = cv2.boundingRect(c)
        cx, cy = x + w//2, y + h//2
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
        cv2.circle(frame, (cx, cy), 4, (0,0,255), -1)
        trail.appendleft((cx, cy))

    # draw trailing path
    for i in range(1, len(trail)):
        if trail[i-1] and trail[i]:
            thickness = max(1, 6 - i//4)
            cv2.line(frame, trail[i-1], trail[i], (255,0,0), thickness)

    # ---------- display ----------
    cv2.imshow("Vehicle detection", frame)
    cv2.imshow("Foreground mask", mask)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
