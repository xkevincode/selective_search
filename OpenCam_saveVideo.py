# -*- coding: utf-8 -*-
# @Time     : 18-6-20 下午7:20
# @File     : OpenCam_saveVideo.py
# @Author   : Kevin X

import cv2
import numpy as np


# open camera
cap = cv2.VideoCapture(0)


# define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
img_out = cv2.VideoWriter('../data/mean_shift.avi', fourcc, 20, (640, 480))

while(True):

    # get a frame
    ret, frame = cap.read()

    # show a frame
    cv2.imshow("capture", frame)

    # save a frame
    img_out.write(frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
img_out.release()
cv2.destroyAllWindows()
