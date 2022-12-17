import time
import cv2
import numpy as np
import mss
from pynput.keyboard import Key, Controller

keyboard = Controller()

with mss.mss() as sct:
    # Подбираем разрешение
    monitor = {"top": 130, "left": 420, "width": 90, "height": 115} 
    
    lowerBound=np.array([0,0,83])
    upperBound=np.array([0,0,83])

    while "Screen capturing":
        last_time = time.time()
        img = np.array(sct.grab(monitor))
        imgHSV= cv2.cvtColor(img,cv2.COLOR_RGB2HSV)
        mask=cv2.inRange(imgHSV,lowerBound,upperBound)
        kernelOpen=np.ones((5,5))
        kernelClose=np.ones((20,20))
        maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
        maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)

        _,conts,h=cv2.findContours(maskClose.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        if(len(conts)>1):
            keyboard.press(Key.space)
            keyboard.release(Key.space)
        else:
            pass
            
        # Для дебага
        cv2.imshow("OpenCV/Numpy normal", img)

        # Нажмите "q" для выходы
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break