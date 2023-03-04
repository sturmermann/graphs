import argparse
import cv2 as cv
import numpy as np 
import matplotlib.pyplot as plt

def args():
    global parser
    parser = argparse.ArgumentParser(
                    prog = 'Optical Graph Recognition',
                    description = 'University project of Hermann \
                    Nestermann that allows recognite graphs from visual to matrix',
                    epilog = '_/ bottom of help \_')
    parser.add_argument('filename', help = "Filename, nothing more")

def preprocessing(img):
    blur = cv.GaussianBlur(img,(5,5),0)
    ret,imgPd = cv.threshold(blur,0,255,cv.THRESH_BINARY_INV+cv.THRESH_OTSU)    
    cv.imwrite("imgPd.jpg", imgPd)
    return imgPd

def segmentation(img):
    kernel = np.ones((5,5),np.uint8)
    segmentatedNode = cv.erode(img,kernel,iterations = 10)
    segmentatedNode = cv.dilate(segmentatedNode,kernel,iterations =10)
    cv.imwrite("segmentatedNode.jpg", segmentatedNode)
    contours, hierarchy = cv.findContours(segmentatedNode, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    #simple = cv.cvtColor(segmentatedNode, cv.COLOR_BGR2RGB)
    #cv.drawContours(simple, contours, -1, (10,0,255), 5)
    #cv.imwrite("segmentatedNodeCounters.jpg", simple)
    nodes = []
    #segmentatedNode = cv.cvtColor(segmentatedNode, cv.COLOR_BGR2RGB)
    segmentatedEdge = img
    for cnt in contours:
        (x,y),radius = cv.minEnclosingCircle(cnt)
        center = (int(x), int(y))
        radius = int(radius)
        nodes.append([center, radius])       
        cv.circle(segmentatedEdge, center, radius, (0,0,0), -1)
    print(nodes)
    cv.imwrite("segmentatedEdge.png", segmentatedEdge)

def main():
    global parser
    args = parser.parse_args()
    filename = args.filename
    image = cv.imread(filename)
    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    if image is None:
        print("Error: no such file or directory")
        return -1
    image = cv.resize(image, (1020, 980))
    image = preprocessing(image)
    image = segmentation(image)
    
    


if __name__ == "__main__":
    args()
    main()
