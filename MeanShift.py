import numpy as np
import cv2
from collections import deque


'''
If we want to mannually select the object, Uncomment this section
'''

# Use mouse to select objects
def get_Object(img_select, title='get_Object'):
    # tl stands for top left, br stands for bottom right
    mouse_params = {'tl': None, 'br': None, 'current_pos': None, 'released_once': False}

    cv2.namedWindow(title)
    cv2.moveWindow(title, 100, 100)

    def onMouse(event, x, y, flags, param):
        param['current_pos'] = (x,y)

        if param['tl'] is not None and not (flags & cv2.EVENT_FLAG_LBUTTON):
            param['released_once'] = True

        if flags & cv2.EVENT_FLAG_LBUTTON:
            if param['tl'] is None:
                param['tl'] = param['current_pos']
            elif param['released_once']:
                param['br'] = param['current_pos']

    cv2.setMouseCallback(title, onMouse, mouse_params)
    cv2.imshow(title, img_select)


    while mouse_params['br'] is None:
        im_draw = np.copy(img_select)

        if mouse_params['tl'] is not None:
            cv2.rectangle(im_draw, mouse_params['tl'],
                          mouse_params['current_pos'], (255, 0, 0))

        cv2.imshow(title, im_draw)
        _ = cv2.waitKey(10)

    cv2.destroyWindow(title)

    tl = (min(mouse_params['tl'][0], mouse_params['br'][0]),
          min(mouse_params['tl'][1], mouse_params['br'][1]))
    br = (max(mouse_params['tl'][0], mouse_params['br'][0]),
          max(mouse_params['tl'][1], mouse_params['br'][1]))

    return (tl, br)




# cap = cv2.VideoCapture('data/mean_shift.avi')
cap = cv2.VideoCapture('/home/kevin/Videos/test.mp4')


# take first frame of the video
ret, frame = cap.read()
cv2.imshow('initial', frame)
# cv2.waitKey(0)


# setup initial location of window
# r, c, h, w -- region of image, rows, cols, height, width
# r, h, c, w = 260, 60,  450, 60

# Uncomment this to manually select object
# a1 is top left point, a2 is bottom right point
a1, a2 = get_Object(frame, title='get_Object')
r, h, c, w = a1[1], a2[1] - a1[1], a1[0], a2[0] - a1[0]



track_window = (c,r,w,h)

# set up the ROI for tracking
roi = frame[r:r + h, c:c + w]

hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv_roi, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
# cv2.imshow('mask', mask)

roi_hist = cv2.calcHist([hsv_roi], [0], mask, [180], [0, 180])
cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)


'''
Termination criteria can be used as flag to show whether tracker is tracking Object.
If Not, we can use Detection like YOLO to track object.
'''
# set up the termination criteria, either 10 iteration or move by at least 1 pt
term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)


'''
Plot the tracking trajectory
'''
pts_maxBuffer = 100000
center_pts = deque(maxlen= pts_maxBuffer)


while(True):

    ret, frame = cap.read()

    if ret == True:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)

        # apply meanshift to get the new location
        ret, track_window = cv2.meanShift(dst, track_window, term_crit)

        # Draw it on image
        x, y, w, h = track_window
        img2 = cv2.rectangle(frame, (x,y), (x+w, y+h), 255, 2)
        # cv2.imshow('img2', img2)

        # calculate center and store it in pts  and save it
        object_center = (int(x+w/2), int(y+h/2))
        center_pts.append(object_center)
        for i in range(1, len(center_pts)):
            if center_pts[i-1] is None or center_pts[i] is None:
                continue
            # thickness = int(np.sqrt(64/float(i+1)*2.5))
            cv2.line(frame, center_pts[i-1], center_pts[i], (0,0,255), 1)
        cv2.imshow('img2', frame)

        k = cv2.waitKey(60) & 0xff
        if k == 27:
            break
        else:
            cv2.imwrite(chr(k)+".jpg", img2)

    else:
        break

cv2.destroyAllWindows()
cap.release()