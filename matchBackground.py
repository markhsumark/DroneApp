import cv2
import numpy as np
from matplotlib import pyplot as plt
 
cap = cv2.VideoCapture("source/Jog.MOV")
template = cv2.imread('source/jogP1.jpg')
template = cv2.cvtColor(template, cv2.COLOR_BGR2RGB)
h, w = template.shape[ :2]
corner_size = 150
border_size =20
corners = 0
method_corner = cv2.TM_SQDIFF
method_people = cv2.TM_CCOEFF

def getDirect(dPostion):
    dx = dPostion[0]
    dy = dPostion[1]
    if dx >= 0 and dy >= 0: 
        return "右下"
    elif dx >= 0 and dy < 0:
        return "左下"
    elif dx < 0 and dy < 0:
        return "左上"
    elif dx < 0 and dy >= 0:
        return "右上"
    else: 
        return "其他"
def getCenter(TopLeft, BottomRight):
    x = (TopLeft[0]+BottomRight[0])/2
    y = (TopLeft[1]+BottomRight[1])/2
    return (x, y)
def getCornersImage(frame, corner_size):
    frame_h, frame_w = frame.shape[:2]
    corners = [ 
        frame[border_size:corner_size+border_size,border_size:corner_size+border_size], #左上角
        frame[-corner_size-border_size:-border_size, border_size:corner_size+border_size],  #左下角
        frame[-corner_size-border_size:-border_size,-corner_size-border_size:-border_size],  #右下角
        frame[border_size:corner_size+border_size,-corner_size-border_size:frame_w-border_size] #右上角
    ]
    corn_XY = ( 
        getCenter([border_size,border_size],[corner_size+border_size, corner_size+border_size]),    #左上角
        getCenter([frame_h-corner_size-border_size, border_size],[frame_h-corner_size, corner_size+border_size]),#左下角
        getCenter([frame_h-corner_size-border_size,frame_w-corner_size-border_size],[frame_h-border_size, frame_w-border_size]),#右下角
        getCenter([border_size,frame_w-corner_size-border_size], [border_size+corner_size, frame_w-border_size])   #右上角
    )
    return corners, corn_XY



while cap.isOpened():
    retval, frame = cap.read()

    frame_h, frame_w = frame.shape[:2]
    frame_out = frame.copy()
    
    if corners == 0:
        print("init")
        corners , corn_position= getCornersImage(frame, corner_size)
        res = cv2.matchTemplate(frame,template,method_people)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method_corner in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.imshow('template', template)
        cv2.rectangle(frame_out,top_left, bottom_right, 255, 2)
        center = [(top_left[0]+bottom_right[0])/2, (top_left[1]+bottom_right[1])/2]
        cv2.imshow('frame', frame_out)
    else:
        last_corners = corners.copy()
        title = ["1" ,'2', '3', '4']
        for i , corner in enumerate(last_corners):
            corn_h , corn_w = corner.shape[:2]
            corn_res = cv2.matchTemplate(frame,corner,method_corner)
            cv2.normalize(corn_res, corn_res, 0, 1, cv2.NORM_MINMAX, -1)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(corn_res)
            if method_corner in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                x1y1 = min_loc
            else:
                x1y1 = max_loc
            x2y2 = (x1y1[0] + corn_w, x1y1[1] + corn_h)
            new_center = getCenter(x1y1, x2y2)

            # 計算座標差
            dx = new_center[0] - corn_position[i][0]
            dy = new_center[1] - corn_position[i][1]
            dPosition = (dx, dy)
            print(corn_position[i], "移動到" , new_center, ": ",getDirect(dPosition),"\n")

            # frame_out = cv2.circle(frame_out, corn_position[i], 2, (0, 0, 0), 2)
            cv2.rectangle(frame_out,x1y1, x2y2, 255, 2)
        print("---")

        corners, corn_position = getCornersImage(frame, corner_size)

        res = cv2.matchTemplate(frame,template,method_people)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    
        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method_people in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.imshow('template', template)
        cv2.rectangle(frame_out,top_left, bottom_right, 255, 2)
        center = [(top_left[0]+bottom_right[0])/2, (top_left[1]+bottom_right[1])/2]
        cv2.imshow('frame', frame_out)

        key = cv2.waitKey(1)
        # ESC
        if key == 27:
            break
cap.release()
cv2.destroyAllWindows()
