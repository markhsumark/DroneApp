import cv2
import numpy as np
from matplotlib import pyplot as plt


CORNER = 1
TARGET = 0
cap = cv2.VideoCapture("source/Jog.MOV")
template = cv2.imread('source/jogP1.jpg')
template = cv2.cvtColor(template, cv2.COLOR_BGR2RGB)
h, w = template.shape[ :2]
corner_size = 150
border_size =30
corners = 0
method_corner = cv2.TM_SQDIFF
person_path =[]
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
    return [x, y]
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

class Target:
    def __init__(self, source, img, type):
        self.type = type
        if type == TARGET:
            self.method_target = cv2.TM_CCOEFF
        elif type == CORNER:
            self.method_target = cv2.TM_SQDIFF
        self.img = img
        self.h, self.w = img.shape[:2]
        self.source = source

        #初始化
        print(type)
        self.bottom_right = [-1,-1]
        self.top_left = [-1,-1]
    def match(self):
        res = cv2.matchTemplate(self.source, self.img, self.method_target)
        cv2.normalize(res, res, 0, 1, cv2.NORM_MINMAX, -1)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if self.method_target in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            self.top_left = min_loc
        else:
            self.top_left = max_loc

        if self.type == TARGET:
            self.bottom_right = (self.top_left[0] + self.w, self.top_left[1] + self.h)
        elif self.type == CORNER:
            self.bottom_right = (self.top_left[0] + self.h, self.top_left[1] + self.w)
    def drawRect(self):
        color = (255, 0, 0)
        thresh = 2
        cv2.rectangle(self.source, self.top_left, self.bottom_right, color, thresh)
    def getRect(self): 
        return [self.top_left, self.bottom_right]

while cap.isOpened():
    retval, frame = cap.read()
    retval, frame = cap.read()
    if retval == False:
        continue

    frame_h, frame_w = frame.shape[:2]
    
    if corners == 0:
        print("-----init-----")

        corners , ls_corn_position= getCornersImage(frame, corner_size)

        target = Target(frame, template, type = TARGET)
        target.match()
        target.drawRect()
        cv2.imshow('frame', target.source)
    else:
        # 處理四個角的部分 背景移動
        last_corners = corners
        total_dPosition = [0, 0]
        dx =0
        dy =0
        dx_res = 0
        dy_res = 0
        for corner, last_corn_position in zip(last_corners, ls_corn_position):
            corner_tmp = Target(frame, corner, CORNER)
            corner_tmp.match()  
            corner_tmp.drawRect()
            
            # corn_h , corn_w = corner.shape[:2]
            # corn_res = cv2.matchTemplate(frame,corner,method_corner)
            # cv2.normalize(corn_res, corn_res, 0, 1, cv2.NORM_MINMAX, -1)
            # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(corn_res)
            # # min_loc 是[y, x]
            # if method_corner in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            #     x1y1 = min_loc
            # else:
            #     x1y1 = min_loc
            # x2y2 = (x1y1[0] + corn_h, x1y1[1] + corn_w)
            new_center = getCenter(corner_tmp.top_left, corner_tmp.bottom_right)
            # new_center = getCenter([x1y1[0], x1y1[1]], [x2y2[0], x2y2[1]])

            #這裡不知道哪裡出錯 需要x y交換
            new_center = [new_center[1], new_center[0]]
            # print("新中心",new_center, "-- 原", last_corn_position)

            # 計算座標差
            dx += new_center[0] - last_corn_position[0]
            dy += new_center[1] - last_corn_position[1]
            print(last_corn_position, "移動到" , new_center, ": ",getDirect([dx,dy]))


        dx_res = dx/5
        dy_res = dy/5
        print([dx_res, dy_res])
        print("---")

        

        target = Target(frame, template, TARGET)
        target.match()
        target.drawRect()
        frame = target.source   #拿回結果
        

        # 畫出路徑
        #過去的路徑
        if len(person_path) > 0:
            for i in range(len(person_path)):
                person_path[i] = [person_path[i][0]+dx_res, person_path[i][1]+dx_res]
                position = (int(person_path[i][0]), int(person_path[i][1]))
                cv2.circle(frame, position, 3, (0, 255, 255), 3)
        # 現在的路徑點
        person_position = getCenter(target.top_left, target.bottom_right)
        person_path.append(person_position)
        person_position = (int(person_position[0]), int(person_position[1]))
        cv2.circle(frame, person_position, 3, (0, 255, 255), 3)
        cv2.imshow('frame', target.source)
        
        corners, ls_corn_position = getCornersImage(frame, corner_size)     # 獲取這一偵的corner img 以提供給下一frame使用

        key = cv2.waitKey(1)
        # ESC
        if key == 27:
            break
cap.release()
cv2.destroyAllWindows()
