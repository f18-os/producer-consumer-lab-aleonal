Producer Consumer Lab

To run:
  $ chmod -x project.py
  $ ./project.py

This file contains the algorithms to extract frames from a video, apply a grayscale to them, and then display them using CV2. The extraction and filter algorithms are bound by a producer-consumer algorithm which uses 1 queue and two semaphores to work. An additional queue outside of the producer-consumer paradigm is used in order to dump the processed frames so that the display algorithm can display them at a proper framerate.

During this lab, I had trouble with finding bugs regarding the threading mechanisms on Python. I wasn't aware that the "target" parameter of a threat had to be the simple def structure declaration and not an actual structure call. This led to the execution of only 1 auxiliary thread. Moreover, I was not aware of how exactly the producer-consumer algorithm was to be implemented. I was confused on whether or not a producer had to fill up a queue before a consumer could access it, or whether they could access it simultaneously (for faster processing of data). Also, I was unsure about how to apply the P/C algorithm, since for example, the filter algorithm could be both a consumer and producer for the extraction and display algorithms respectively. 

In total, I spent 5 hours on this lab. Due to family duties and unexpected issues such as my laptop not holding any charge, I was not able to complete in time but thought I would share how long it took me to complete.
