#!/usr/bin/env python3

import threading
import cv2
import numpy as np
import base64
import queue

def extractFrames():
    global isDone, extractionQ
    count = 0

    vidcap = cv2.VideoCapture('clip.mp4')
    success,image = vidcap.read()
    print("Reading frame {} {} ".format(count, success))

    while success:
            success, jpgImage = cv2.imencode('.jpg', image)
            jpgAsText = base64.b64encode(jpgImage)
            empty.acquire()
            extractionQ.put(jpgAsText)
            fill.release()
            success,image = vidcap.read()
            print('Reading frame {} {}'.format(count, success))
            count += 1

    isDone = 1;
    print("Frame extraction complete")


def grayScale():
    global isDone, extractionQ, displayQ
    count = 0

    while isDone is not 1 or not extractionQ.empty():
        fill.acquire()
        frameAsText = extractionQ.get()
        empty.release()
        jpgRawImage = base64.b64decode(frameAsText)
        jpgImage = np.asarray(bytearray(jpgRawImage), dtype=np.uint8)
        img = cv2.imdecode( jpgImage ,cv2.IMREAD_UNCHANGED)
        grayscaleFrame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        jpgAsText = base64.b64encode(grayscaleFrame)
        displayQ.put(jpgAsText)
        print('Converted frame {}'.format(count))
        count += 1


    print("Frame conversion complete")


def displayFrames():
    global isDone, displayQ
    count = 0

    while isDone is not 1 or not displayQ.empty():
        frameAsText = displayQ.get()
        jpgRawImage = base64.b64decode(frameAsText)
        jpgImage = np.asarray(bytearray(jpgRawImage), dtype=np.uint8)
        img = cv2.imdecode( jpgImage ,cv2.IMREAD_UNCHANGED)
        print("Displaying frame {}".format(count))
        cv2.imshow("Video", img)
        if cv2.waitKey(42) and 0xFF == ord("q"):
            break

        count += 1

    print("Finished displaying all frames")
    cv2.destroyAllWindows()

filename = 'clip.mp4'
isDone = 0;

# shared queues
extractionQ = queue.Queue()
displayQ = queue.Queue()

# semaphores
fill = threading.Semaphore(0)
empty = threading.Semaphore(10)

# threads
eT = threading.Thread(target=extractFrames).start()
gT = threading.Thread(target=grayScale).start()
dT = threading.Thread(target=displayFrames).start()
