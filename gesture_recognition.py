import cv2
import numpy as np
import os

''' only recognizes hand gestures from video feed.
does not process the video or the images it gets in any way - all video options and tweaks need to be done externally
'''

class recognizer:
    def __init__(self, cascades_folder='cascades', palm_cascade='palm2.xml', fist_cascade='fist2.xml'):
        self.palm=cv2.CascadeClassifier(os.path.join(cascades_folder,palm_cascade))
        self.fist=cv2.CascadeClassifier(os.path.join(cascades_folder,fist_cascade))
        
        
    def find_biggest(seld, rect_list):
        # finds biggest (closest) recognized hand (by bounding rectangle size)
        
        if type(rect_list) != tuple:
            # largest format is (scale, index)
            largest = (0, 0)
        
            for idc in range(len(rect_list)):
                l = rect_list[idc]
                
                scale_a = l[2]
                scale_b = l[3]
                
                if ((scale_a + scale_b) / 2) > largest[0]:
                    largest = (int((scale_a + scale_b) / 2), idc)
            
            # return center position of the largest object
            center_a = rect_list[idc][0] + int(rect_list[idc][2] / 2)
            center_b = rect_list[idc][1] + int(rect_list[idc][3] / 2)
            
            return (center_a, center_b)
                    
        else:
            # means the list is empty
            return 'NA'