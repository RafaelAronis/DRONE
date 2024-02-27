# ------- Import --------------------------------------------------------------------------
import cv2
import os

# ------- RUN --------------------------------------------------------------------------
watch_cascade = cv2.CascadeClassifier('cascade/cascade4/cascade.xml')
list_img=os.listdir('imgs/positive_imgs')

for img_name in list_img:

    # Frame preparation
    img = cv2.imread('imgs/positive_imgs/'+img_name)
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    watches = watch_cascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=1)

    # Draw a rectangle around the objects
    for (x, y, w, h) in watches:
        cv2.rectangle(img, (x - 4, y + h), (x + w + 5, y + h + 16), (255, 0, 0), cv2.FILLED)
        cv2.putText(img, 'Drone', (x - 4, y + h + 13), cv2.FONT_ITALIC, 0.42, (255, 255, 255), 1)
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    cv2.imshow('img', img)
    #cv2.imwrite(img_name+'.png',img)
    k = cv2.waitKey(0) & 0xff
    if k == 27:
        break

cv2.destroyAllWindows()