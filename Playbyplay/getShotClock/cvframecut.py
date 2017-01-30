import cv2
vidcap = cv2.VideoCapture('game.mp4')
success,image = vidcap.read()
count = 0
success = True
while success:
    success,image = vidcap.read()
    if count%15 == 0:
        print ('Read a new frame: ', success)
        cv2.imwrite("sample_images/frame%d.png" % count, image)     # save frame as JPEG file
    count += 1


'''
import cv2
vidcap = cv2.VideoCapture('shortmov.mp4')
success,image = vidcap.read()
count = 0
success = True
while success:
    success,image = vidcap.read()
    if count%15 == 0:
        print 'Read a new frame: ', success
        cv2.imwrite("testfolder/frame%d.jpg" % count, image)     # save frame as JPEG file
    count += 1

'''
