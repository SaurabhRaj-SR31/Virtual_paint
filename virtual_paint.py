import cv2
import numpy as np
cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
cap.set(10,120)

mycolors= [
    [35, 100, 100, 85, 255, 255],
    ]
    # [20, 100, 100, 30, 255, 255],
    # [10, 100, 100, 25, 255, 255]]
    # [130, 100, 100, 160, 255, 255],
    # [145, 100, 100, 175, 255, 255],
    # [85, 100, 100, 100, 255, 255],
    # [5, 50, 50, 25, 255, 255],
    # [0, 0, 200, 255, 50, 255],
    # [0, 0, 0, 255, 255, 50],
    # [0, 0, 50, 255, 50, 200],
    # [20, 100, 100, 40, 255, 255],
    # [0, 0, 150, 255, 50, 200],
    # [70, 100, 100, 100, 255, 255]]

mycolor_values=[ [0, 255, 0]]

    # Color 3: Blue
    # [255, 0, 0]]

mypoints=[]
def findcolor(img,mycolors,mycolor_values):
    imghsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    count=0
    newpoint=[]
    for colors in mycolors:
      lower=np.array(colors[0:3])
      upper = np.array(colors[3:6])
      mask=cv2.inRange(imghsv,lower,upper)
      x,y=getContours(mask)
      cv2.circle(imgresult,(x,y),10,mycolor_values[count],cv2.FILLED)
      if x!=0 and y!=0 :
          newpoint.append([x,y,count])
      count+=1
    return newpoint

def getContours(img):
    contours,hierarchy=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h=0,0,0,0
    for cnt in contours:
        area=cv2.contourArea(cnt)
        if(area>500):
            cv2.drawContours(imgresult,cnt,-1,(255,0,0),3)
            peri=cv2.arcLength(cnt,True)
            approx=cv2.approxPolyDP(cnt,0.02*peri,True)
            x,y,w,h=cv2.boundingRect(approx)
    return x+w//2,y

def drawoncanvas(mypoints,mycolor_values):
    for point in mypoints:
        cv2.circle(imgresult, (point[0], point[1]), 10, mycolor_values[point[2]], cv2.FILLED)

while True:
    success,img=cap.read()
    imgresult=img.copy()
    newpoint=findcolor(img,mycolors,mycolor_values)
    if len(newpoint)!=0:
       for newp in newpoint:
         mypoints.append(newp)

    if len(mypoints)!=0:
        drawoncanvas(mypoints,mycolor_values)
    cv2.imshow("video",imgresult)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break