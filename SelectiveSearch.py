'''
Usage:
    selective search method to give region proposal

'''

import sys
import cv2

if __name__ == '__main__':

    # speed up using multithreads
    cv2.setUseOptimized(True)
    cv2.setNumThreads(4)


    # read image
    # img = cv2.imread("1002.jpeg")
    img = cv2.imread('ss_test.png')
    cv2.imshow('my_img', img)

    # resize image
    newHeight = 200
    newWidth = int(newHeight*img.shape[1]/img.shape[0])
    img = cv2.resize(img, (newHeight, newWidth))
    # print(img.shape)


    # create selective search segmentation object using default parameters
    # if this gives error, you need to install opencv-contrib-python
    ss = cv2.ximgproc.segmentation.createSelectiveSearchSegmentation()

    # set an image which we will run selective search algorithm
    ss.setBaseImage(img)

    # choose different mode to run
    cmd = input("F for fast but low recall, H for high recall, enter you cmd: ")
    # print(cmd)

    # fast but low recall selective search method
    if(cmd.upper()=='F'):
        ss.switchToSelectiveSearchFast()

    # high recall but low speed selective search method
    elif(cmd.upper()=='H'):
        ss.switchToSelectiveSearchQuality()

    # print out comments information in the file
    else:
        print(__doc__)
        sys.exit(1)


    # run selective search segmentation on the input image
    rects = ss.process()
    print('Total Number of Region Proposals: {}'.format(len(rects)))


    # number of region proposals to show
    numShowRects = 100
    # increment to increase /decrease total number
    increment = 50


    while True:
        # create a copy of original image
        imgOut = img.copy()

        # iterative over all the region proposals
        for i, rect in enumerate(rects):
            # draw rectangle for region proposal till numShowRects
            if(i<numShowRects):
                x, y, w, h = rect
                cv2.rectangle(imgOut, (x,y), (x+w, y+h), (0,255,0), 1, cv2.LINE_AA)
            else:
                break

        # show output
        cv2.imshow("Output", imgOut)

        # record key press, you will get the ASCII code for this number
        key_press = cv2.waitKey(0) & 0xFF

        # m is 109
        if key_press == 109:
            numShowRects += increment

        # l is 108
        elif key_press == 108 and numShowRects > increment:
            numShowRects -= increment

        # q is pressed
        elif key_press == 113:
            break

    # close image show window
    cv2.destroyAllWindows()


