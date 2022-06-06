import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self ,mode=False, maxHands = 2, capacity=1 ,detectionCon = 0.5, trackCon = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.capacity = capacity
        self.detectionCon = detectionCon
        self.trackCon = trackCon


        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands ,self.capacity, self.detectionCon , self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self , img , draw=True):
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        self.h_landmark = self.results.multi_hand_landmarks
        # print(h_landmark)
        if self.h_landmark:
            for handLMS in self.h_landmark:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLMS, self.mpHands.HAND_CONNECTIONS)
        return img    
    
    def findPosition(self, img , handNo=0, draw=True):
        lmList = []
        if self.h_landmark:
            myhand = self.h_landmark[handNo]
            for id , lm in enumerate(myhand.landmark):
            # print(id)
                h, w, c = img.shape
                cx , cy = int(lm.x*w) , int(lm.y*h)
                
                lmList.append([id,cx,cy])
                if draw:
                    cv2.circle(img,(cx,cy),5,(0,0,255),cv2.FILLED)
                    cv2.putText(img,str(int(id)), (cx,cy), cv2.FONT_HERSHEY_PLAIN, 1, (25,0,120),1)
        return lmList        
            


   

def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True :
        success, img = cap.read()
        img = detector.findHands(img)
        
        lmlist = detector.findPosition(img)
        if len(lmlist)!=0:
            print(lmlist)

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime 

        cv2.putText(img,str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,120),3)       

        cv2.imshow("image", img)
        cv2.waitKey(1)    


if __name__ == "__main__":
    main()    