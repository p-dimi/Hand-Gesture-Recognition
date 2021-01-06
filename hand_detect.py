import cv2
import numpy as np
import os

from grid_position import GridPos


## SETTINGS ##
grid_size=3

dshow = True
contrast = False
contrast_clip = 2.0
contrast_tile = 8
denoise = False
large_frame = False
tiny_frame = False

palm_cascade = 'palm2.xml'
closed_palm_cascade = 'fist2.xml'




g_p = GridPos(grid_size,grid_size)

dshow = True
contrast = False
contrast_clip = 2.0
contrast_tile = 8
denoise = False
large_frame = False
tiny_frame = False

# cascades 
cascade_path = 'cascades'

palm = cv2.CascadeClassifier(os.path.join(cascade_path, palm_cascade))
closed_palm = cv2.CascadeClassifier(os.path.join(cascade_path, closed_palm_cascade))

'''fist = cv2.CascadeClassifier(os.path.join(cascade_path, fist_cascade))'''

# cascade detection settings
if tiny_frame:
    min_neighbors = 3
    scaling_size = 1.05
else:
    min_neighbors = 5
    scaling_size = 1.1
    
# video capture & settings
if dshow:
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
else:
    cap = cv2.VideoCapture(0)

if large_frame:
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
elif tiny_frame:
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 180)

# function to improve contrast
def contrast_fix(img, clip, tile):
    #-----Converting image to LAB Color model----------------------------------- 
    lab= cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    
    #-----Splitting the LAB image to different channels-------------------------
    l, a, b = cv2.split(lab)
    
    #-----Applying CLAHE to L-channel-------------------------------------------
    clahe = cv2.createCLAHE(clipLimit=clip, tileGridSize=(tile,tile))
    cl = clahe.apply(l)
    
    #-----Merge the CLAHE enhanced L-channel with the a and b channel-----------
    limg = cv2.merge((cl,a,b))
    
    #-----Converting image from LAB Color model to RGB model--------------------
    final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    return final


# function going over list of rectangles to find the biggest one and returns it's center
def find_biggest(rect_list):
    # the format of input should be a list of lists, where each nested list has four items representing a rectangle's origin corner and scale

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

# track last position
grid_states = (0,0), False
        
# video capture test
while True:
    ret, frame = cap.read()

    # frame captured mirrored, mirror back
    frame = cv2.flip(frame, 1)

    # improve contrast
    if contrast:
        frame = contrast_fix(frame, contrast_clip, contrast_fix)
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # image denoising
    if denoise:
        gray = cv2.fastNlMeansDenoising(gray)
    
    # detected objects
    palms = palm.detectMultiScale(gray, scaling_size, min_neighbors)

    closed_palms = closed_palm.detectMultiScale(gray, scaling_size, min_neighbors)
    
    '''fists = fist.detectMultiScale(gray, scaling_size, min_neighbors)'''

    # if both right and left palms are detected, combine both left and right palms detected & find the biggest one
    
    palm_center = find_biggest(palms)
        
    closed_palm_center = find_biggest(closed_palms)
    
    current_palm_status = 'NA'
    
    # check which item was last seen
    if palm_center != 'NA' and closed_palm_center == 'NA':
        # open palm
        current_palm_status = 'open'

    elif palm_center == 'NA' and closed_palm_center != 'NA':
        # closed palm
        current_palm_status = 'closed'

    elif palm_center == 'NA' and closed_palm_center == 'NA':
        # neither open nor closed
        current_palm_status = 'NA'
        
    elif palm_center != 'NA' and closed_palm_center != 'NA':
        # both open and closed are seen - consider only the open
        current_palm_status = 'open'

    # get new position on the grid defined in GridPos
    if current_palm_status == 'open':
        grid_states = g_p.run(palm_center, current_palm_status)
    
    elif current_palm_status == 'closed':
        grid_states = g_p.run(closed_palm_center, current_palm_status)
        
    elif current_palm_status == 'NA':
        # if the palm status is NA, for position - I'd like to simply not consider the movement
        #pos, select = g_p.run(last_pos, current_palm_status)
        pass
    
    pos, select = grid_states
    
    print(pos)
    print(select)
    
    key = cv2.waitKey(1)

    try:
        cv2.circle(frame, palm_center, 50, (0,0,255), 5)
    except:
        pass
    try:
        cv2.circle(frame, closed_palm_center, 50, (0,255,0), 5)
    except:
        pass

    cv2.imshow('frame', frame)
    
    if key == ord('q'):
        break

cap.release()        
cv2.destroyAllWindows()