import cv2
import time
import numpy as np

#To save the output in a file output.avi
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_file = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

#Starting the webcam
cap = cv2.VideoCapture(0)

#Allowing the webcam to start by making the code sleep for 2 seconds
time.sleep(2)
bg = 0

#Capturing background for 60 frames
for i in range(60):
    ret, bg = cap.read()
#Flipping the background
bg = np.flip(bg, axis=1)

#Reading the captured frame until the camera is open
while (cap.isOpened()):
    ret, img = cap.read()
    if not ret:
        break
    #Flipping the image for consistency
    img = np.flip(img, axis=1)

    #converting the colour from bgr to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #generating mask to detect red colour
    lower_red = np.array([0, 120, 50])
    upper_red = np.array([10, 255, 255])
    mask_1 = cv2.inRange(hsv, lower_red, upper_red)

    lower_red = np.array([170, 120 ,70])
    upper_red = np.array([180, 255, 255])
    mask_2 = cv2.inRange(hsv, lower_red, upper_red)

    mask_1 = mask_1 + mask_2
    cv2.imshow("mask_1", mask_1)

    #open and expand the img where there is mask 1
    mask_1 = cv2.morphologyEx(mask_1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))

    #selecting only the path that does not have mask 1 and saving in mask 2
    mask_2 = cv2.bitwise_not(mask_1)

    # keeping only the part of the imgs without the red colour
    res_1 = cv2.bitwise_and(img, img, mask = mask_2)

    # keeping only the part of the imgs with the red color
    res_2 = cv2.bitwise_and(bg, bg, mask = mask_1)



    #Generating the final output
    final_output = cv2.addWeighted(res_1, 1, res_2, 1, 0)
    output_file.write(final_output)
    
    #Displaying the output to the user
    cv2.imshow("magic", final_output)
    cv2.waitKey(1)


cap.release()
out.release()
cv2.destroyAllWindows()

