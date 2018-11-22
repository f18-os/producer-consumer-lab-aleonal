#!/usr/bin/env python3

import threading
import cv2
import numpy as np
import base64
import queue


# filename of clip to load
filename = 'clip.mp4'

# shared queues
extractionQ = Q(10)
displayQ = Q(10)

# semaphores & mutex
eS = threading.Semaphore()
dS = threading.Semaphore()
eM = threading.Lock()
dM = threading.Lock()

# threads
eT = threading.Thread(target=extractFrames(filename, extractionQ)).start()
gT = threading.Thread(target=grayScale(extractionQ, displayQ)).start()
dT = threading.Thread(target=displayFrames(displayQ)).start()

class Q:
    def __init__(self, initArray = []):
        self.a = []
        self.a = [x for x in initArray]

    def put(self, item):
        self.a.append(item)

    def get(self):
        a = self.a
        item = a[0]
        del a[0]
        return item

    def __repr__(self):
        return "Q(%s)" % self.a

def extractFrames(fileName, outputBuffer):
    count = 0

    vidcap = cv2.VideoCapture(fileName)
    success,image = vidcap.read()
    print("Reading frame {} {} ".format(count, success))

    while success:
        eS.acquire()
        success, jpgImage = cv2.imencode('.jpg', image)
        jpgAsText = base64.b64encode(jpgImage)

        eM.acquire()
        outputBuffer.put(jpgAsText)
        eM.release()

        success,image = vidcap.read()
        print('Reading frame {} {}'.format(count, success))
        count += 1
        eS.release()

    print("Frame extraction complete")


def grayScale(inputBuffer, outputBuffer):
    count = 0

    while not inputBuffer.empty():
        eS.acquire()
        eM.acquire()
        frameAsText = inputBuffer.get()
        eM.release()
        eS.release()

        jpgRawImage = base64.b64decode(frameAsText)
        jpgImage = np.asarray(bytearray(jpgRawImage), dtype=np.uint8)
        img = cv2.imdecode( jpgImage ,cv2.IMREAD_UNCHANGED)
        grayscaleFrame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        jpgAsText = base64.b64encode(grayscaleFrame)

        dS.acquire()
        dM.acquire()
        outputBuffer.put(jpgAsText)
        dM.release()
        dS.release()

        count += 1
    print("Frame conversion complete")


def displayFrames(inputBuffer):
    count = 0

    while not inputBuffer.empty():
        dS.acquire()
        dM.acquire()
        frameAsText = inputBuffer.get()
        dM.release()

        jpgRawImage = base64.b64decode(frameAsText)
        jpgImage = np.asarray(bytearray(jpgRawImage), dtype=np.uint8)
        img = cv2.imdecode( jpgImage ,cv2.IMREAD_UNCHANGED)
        print("Displaying frame {}".format(count))
        cv2.imshow("Video", img)
        if cv2.waitKey(42) and 0xFF == ord("q"):
            break

        count += 1
        dS.release()

    print("Finished displaying all frames")
    cv2.destroyAllWindows()
