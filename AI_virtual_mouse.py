import cv2
import handTracxkingModule as htm
import time
import pyautogui as pg
import math

pg.FAILSAFE  = False

##################################################################################################################

screenSizeX , screenSizeY = pg.size()

wCam ,hCam = screenSizeX/3,screenSizeY/3

pTime = 0
cTime = 0


detector = htm.handDetector(maxHands=1)
##################################################################################################################

def distance_dt(x1,y1,x2,y2):
    return math.sqrt(math.pow(x2-x1,2)+math.pow(y2-y1,2))

def mouse_move():
    a,b = lmList[8][1]*4,lmList[8][2]*4
    if a>=screenSizeX :
        a=screenSizeX
    if a<=0:
        a=0    
    if b>=screenSizeY:
        b = screenSizeY
    if b<=0:
        b=0    
    pg.moveTo(a,b) 
    # print(l,m)

cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

pg.moveTo(screenSizeX/2,screenSizeY/2)

flag_click = 1
flag_right_click = 1

scrolVstart = 0
scrolVend = 0

while True:
    success , img = cap.read()
    img = cv2.flip(img,1)
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,f'FPS : {int(fps)}',(20,40),cv2.FONT_HERSHEY_SCRIPT_COMPLEX,1,(255,0,0),1)


    img = detector.findHands(img,draw=False)
    lmList = detector.findPosition(img,draw=False)

    if len(lmList)!=0:
        x1,y1 = lmList[8][1] , lmList[8][2]
        x2,y2 = lmList[12][1], lmList[12][2]

        ###### mouse poin moving part ######
        if lmList[0][2]>lmList[9][2]:
            if lmList[8][2]<lmList[6][2] and lmList[8][2]<lmList[4][2]:
                mouse_move()


        ###### mouse left click #####        
        if lmList[12][2]<lmList[10][2] and lmList[18][2]<lmList[16][2] and lmList[8][2]<lmList[4][2] and flag_click==1:
            dis = distance_dt(x1,y1,x2,y2)
            dis2 = distance_dt(x1,y1,lmList[7][1],lmList[7][2])
            disR = dis/dis2
            # print(dis , "      ",dis2,"        ", disR)
            if disR<1.2:
                pg.click()   
                print("left click")     
            flag_click = 0
        elif lmList[12][2]>lmList[10][2]:
            flag_click = 1     


        ########## mouse Right click ###############
        if lmList[20][2]<lmList[18][2] and lmList[18][2]<lmList[16][2] and lmList[8][2]<lmList[4][2] and flag_right_click ==1:
            pg.click(button='right')
            print("right click")
            # pg.mouseDown(button='left')
            flag_right_click=0
        elif lmList[20][2]>lmList[18][2]:
            # pg.mouseUp(button='left')
            flag_right_click =1    

        ####### mouse drag #############
        if lmList[8][2]<lmList[6][2] and lmList[8][2]<lmList[4][2] and lmList[16][2]<lmList[14][2]:
            pg.mouseDown(button='left')
        else:
            pg.mouseUp(button='left') 

        ##### mouse scroll vertical ######
        if lmList[4][2]<lmList[8][2] and lmList[4][2]<lmList[12][2] and lmList[4][1]>lmList[6][1]:
            scrolVend = lmList[4][2]
            if scrolVstart ==0:
                scrolVstart = scrolVend
            pg.scroll((scrolVend-scrolVstart)*8)
            scrolVstart = scrolVend
          


        cv2.circle(img,(lmList[12][1], lmList[12][2]),3,(120,120,44),3,cv2.FILLED)    
        cv2.circle(img,(lmList[8][1], lmList[8][2]),3,(120,100,0),3,cv2.FILLED)           
        # print(lmList)
        

    cv2.imshow("img",img)
    cv2.waitKey(1)
