from imutils.video import FPS
import imutils
import cv2
import time
import imagezmq
from imutils.video.pivideostream import PiVideoStream
from picamera.array import PiRGBArray
from picamera import PiCamera
import threading 
class Publisher():

    def __init__(self, port,quality=20):
        self.port=port
        self.sender=imagezmq.ImageSender("tcp://*:{}".format(port), REQ_REP=False)
        self.quality=quality
    
    def publish(self,frame,message=None):
        if message is None:
            message="Supbois"
        ret_code, jpg_buffer = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), self.quality])
        self.sender.send_jpg(message,jpg_buffer)

class Pipelines():
    stream=PiVideoStream().start()
    def __init__(self,name='nameless',port=5555,func=None,quality=50,set_fps=80):
        
        self.name=name
        self.port=port
        if func == None:
            self.func= self.doNothing
        else:
            self.func=func
        self.quality=quality
        self.set_fps=set_fps
        self.publisher=Publisher(self.port,self.quality)
    def doNothing(self,img):
        return img
    def startStream(self):
        self.thread= threading.Thread(target=self.process)
        self.thread.start()
        
    def process(self):
        while True:
            frame=self.stream.read()
            img=self.func(frame)
            self.publisher.publish(img)
            time.sleep((1/self.set_fps)  -0.0047)
    def wait(self):
        self.thread.join()
            
        
#mainpip=Pipelines()
#time.sleep(2)
#mainpip.startStream()

