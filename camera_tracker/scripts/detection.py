import cv2 
import keyboard
import numpy as np
import configparser
import os
import sys

#Create a configparser object to store/ load configurations
config = configparser.ConfigParser()

def empty(a):
    pass


def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver


def findContours(img,threshold):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)
    #imgCanny = cv2.Canny(imgBlur,100,200)
    thresh, binary = cv2.threshold(imgGray,threshold,255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(binary,cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    print("number of contours " + str(len(contours)))
    return contours


class CameraCalibraion:
    def __init__(self) -> None:
        #get scripts directory path
        self.config_path = os.path.dirname( sys.argv[0])+"/config.ini"
        
        #read config file to load preferences
        config.read(self.config_path)
        
    def colorCalibration(self)->None:

        #init cap device
        cap = cv2.VideoCapture(0)
        cv2.namedWindow("TrackBars")
        cv2.resizeWindow("TrackBars",640,240)

        #set init values for trackbars from the config file
        cv2.createTrackbar("Hue Min","TrackBars",int(config["Lower"]["hue"]),179,empty)
        cv2.createTrackbar("Hue Max","TrackBars",int(config["Upper"]["hue"]),179,empty)
        cv2.createTrackbar("Sat Min","TrackBars",int(config["Lower"]["saturation"]),255,empty)
        cv2.createTrackbar("Sat Max","TrackBars",int(config["Upper"]["saturation"]),255,empty)
        cv2.createTrackbar("Val Min","TrackBars",int(config["Lower"]["value"]),255,empty)
        cv2.createTrackbar("Val Max","TrackBars",int(config["Upper"]["value"]),255,empty)



        #capture video frame by frame
        while cap.isOpened():
            ret, img = cap.read()
            if ret == True:
                imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
                h_min = cv2.getTrackbarPos("Hue Min","TrackBars")
                h_max = cv2.getTrackbarPos("Hue Max","TrackBars")
                s_min = cv2.getTrackbarPos("Sat Min","TrackBars")
                s_max = cv2.getTrackbarPos("Sat Max","TrackBars")
                v_min = cv2.getTrackbarPos("Val Min","TrackBars")
                v_max = cv2.getTrackbarPos("Val Max","TrackBars")
                lower= np.array([h_min,s_min,v_min])
                upper= np.array([h_max,s_max,v_max])
                mask =cv2.inRange(imgHSV,lower,upper)
                imgResult = cv2.bitwise_and(img,img,mask=mask)


                imgStack=stackImages(0.6,([img,imgHSV],[mask,imgResult]))
                cv2.imshow("Stacked", imgStack)

                if cv2.waitKey(25) & 0xFF == ord('q'):

                    #save preferences to config file
                    config["Lower"]["hue"] = str(h_min)
                    config["Lower"]["saturation"] = str(s_min)
                    config["Lower"]["value"] = str(v_min)

                    config["Upper"]["hue"] = str(h_max)
                    config["Upper"]["saturation"] = str(s_max)
                    config["Upper"]["value"] = str(v_max)
                    with open(self.config_path,'w') as configFile:
                        config.write(configFile)
                    break
        cap.release()
        cv2.destroyAllWindows()



class ColorDetecion:
    def __init__(self) -> None:
        #get scripts directory path
        self.config_path = os.path.dirname( sys.argv[0])+"/config.ini"
        
        #read config file to load preferences
        config.read(self.config_path)
        
        
        #load preferences from config file
        self.lower_range = (int(config["Lower"]["hue"]), int(config["Lower"]["saturation"]), int(config["Lower"]["value"]))
        self.upper_range = (int(config["Upper"]["hue"]), int(config["Upper"]["saturation"]), int(config["Upper"]["value"]))
        print(self.lower_range)




    def detectColorInFrame(self, frame) -> tuple:
        #list of object centroids in the current frame
        #centroids = []
        best_area = 0
        center = (0, 0)
        whiteImage = np.full((frame.shape[0], frame.shape[1], 3), 255, np.uint8)

        #switch to csv color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        #create a mask for the detected color
        mask = cv2.inRange(hsv, self.lower_range, self.upper_range)
        imgSum = cv2.bitwise_and(whiteImage, whiteImage, mask=mask)

        #find contours based on the mask
        contours = findContours(imgSum, 60)

        #find the centroid for each contour
        for cnt in contours:
            M = cv2.moments(cnt)
            x, y, width, height = cv2.boundingRect(cnt)
            

            

            if width * height > best_area:
                best_area = width * height
                cntr_x = x + width/2
                cntr_y = y + height/2
                center = (cntr_x, cntr_y)
                cv2.rectangle(imgSum, (x, y), (x + width, y + height), (0, 255, 0), 2)

            

        return center,imgSum


    


class ObjectDetection:
    def __init__(self) -> None:
        pass


    



def main():
    calibration = CameraCalibraion()
    calibration.colorCalibration()
    colordetection = ColorDetecion()

    cap = cv2.VideoCapture(0)
    while cap.isOpened():
            ret, frame = cap.read()
            if ret == True:
                cntr, resframe = colordetection.detectColorInFrame(frame)
                print(cntr)
                cv2.imshow("tracked object",resframe)
                if cv2.waitKey(1) & 0xFF ==ord('q'):
                    break



if __name__ == "__main__":
    main()
