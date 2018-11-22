#!/usr/bin/env python3

import threading
import cv2
import numpy as np
import base64
import queue


# filename of clip to load
filename = 'clip.mp4'

# shared queues
extractionQ = Queue()
displayQ = Queue()

# semaphores & mutex
fill = threading.Semaphore()
empty = threading.Semaphore(10)

# threads
eT = threading.Thread(target=extractFrames(filename, extractionQ)).start()
gT = threading.Thread(target=grayScale(extractionQ, displayQ)).start()
dT = threading.Thread(target=displayFrames(displayQ)).start()

def extractFrames(fileName, outputBuffer):
    count = 0

    vidcap = cv2.VideoCapture(fileName)
    success,image = vidcap.read()
    print("Reading frame {} {} ".format(count, success))

    while success:
        empty.acquire()
        success, jpgImage = cv2.imencode('.jpg', image)
        jpgAsText = base64.b64encode(jpgImage)
        outputBuffer.put(jpgAsText)
        success,image = vidcap.read()
        print('Reading frame {} {}'.format(count, success))
        fill.release()
        count += 1

    print("Frame extraction complete")


def grayScale(inputBuffer, outputBuffer):
    count = 0

    while(eT.is_alive()):
        fill.acquire()
        frameAsText = inputBuffer.get()
        jpgRawImage = base64.b64decode(frameAsText)
        jpgImage = np.asarray(bytearray(jpgRawImage), dtype=np.uint8)
        img = cv2.imdecode( jpgImage ,cv2.IMREAD_UNCHANGED)
        grayscaleFrame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        jpgAsText = base64.b64encode(grayscaleFrame)
        outputBuffer.put(jpgAsText)
        empty.release()
        count += 1

    print("Frame conversion complete")


def displayFrames(inputBuffer):
    count = 0

    while(gT.is_alive()):
        if not inputBuffer.empty():
            frameAsText = inputBuffer.get()
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
