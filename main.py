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
    #alpha = 1 # Contrast control (1.0-3.0)
    #beta = 0 # Brightness control (0-100)
    #img = cv.convertScaleAbs(img, alpha=alpha, beta=beta)
    #cv.imwrite("imgFirst.jpg", img)
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img = cv.resize(img, (1020, 980))
    img = cv.GaussianBlur(img,(21,21),0)
    imgPd = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,11,2)
    cv.imwrite("imgPd.jpg", imgPd)
    return imgPd

def segmentation(img):
    kernel = np.ones((3,3),np.uint8)
    #segmentatedNode = cv.erode(img,kernel,iterations = 5)
    segmentatedNode = cv.dilate(img,kernel,iterations = 1)
    cv.imwrite("segmentatedNode.jpg", segmentatedNode)
    contours, hierarchy = cv.findContours(segmentatedNode, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    #simple = cv.cvtColor(segmentatedNode, cv.COLOR_BGR2RGB)
    #cv.drawContours(simple, contours, -1, (10,0,255), 5)
    #cv.imwrite("segmentatedNodeCounters.jpg", simple)
    nodes = []
    #segmentatedNode = cv.cvtColor(segmentatedNode, cv.COLOR_BGR2RGB)
    segmentatedEdge = img
    num = 0
    for cnt in contours:
        (x,y),radius = cv.minEnclosingCircle(cnt)
        center = (int(x), int(y))
        radius = int(radius)
        nodes.append([center, radius])       
        cv.circle(segmentatedNode, center, radius, (255,255,255), -1)
        cv.circle(segmentatedEdge, center, radius+5, (0,0,0), -1)
        cv.putText(segmentatedEdge, str(num), center, cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        num+=1
    cv.imwrite("segmentatedNode2.jpg", segmentatedNode)
    print(nodes)
    cv.imwrite("segmentatedEdge.png", segmentatedEdge)
    matrix = []
    for i in range(len(nodes)):
        matrix.append([])
        for j in range(len(nodes)):
            matrix[i].append(0)
    #print(matrix)
    lines = cv.HoughLinesP(
            segmentatedEdge, # Input edge image
            2, # Distance resolution in pixels
            np.pi/360, # Angle resolution in radians
            threshold=100, # Min number of votes for valid line
            minLineLength=25, # Min allowed length of line
            maxLineGap=50 # Max allowed gap between line for joining them
            )
    edges = []
    for points in lines:
        x1,y1,x2,y2=points[0]
        edges.append([(x1,y1), (x2,y2)])
        segmentatedEdge = cv.cvtColor(segmentatedEdge, cv.COLOR_BGR2RGB)
        cv.line(segmentatedEdge,(x1,y1),(x2,y2),(0,255,0),2)
        cv.imwrite("111.png", segmentatedEdge)
    #print(edges)

    for edge in edges:
        startPoint = -1
        endPoint = -1
        #print(f"{edge} \n")
        for i in range(0, len(nodes)):
            center_x = nodes[i][0][0]
            center_y = nodes[i][0][1]
            start_x = edge[0][0] - center_x
            start_y = edge[0][1] - center_y
            #print(i, center_x, center_y, edge[0][0], edge[0][1], start_x, start_y, start_x*start_x + start_y*start_y, nodes[i][1])
            if start_x**2 + start_y**2 <= (nodes[i][1]+30)**2:
                startPoint = i
                break
        for i in range(0, len(nodes)):
            center_x = nodes[i][0][0]
            center_y = nodes[i][0][1]
            end_x = edge[1][0] - center_x
            end_y = edge[1][1] - center_y
            if end_x**2 + end_y**2 <= (nodes[i][1]+30)**2:
                endPoint = i
                break
        #print(endPoint, startPoint)
        # if endPoint == 0 or startPoint == 0:
        #     cv.line(segmentatedEdge,(edge[0][0], edge[0][1]),(edge[1][0],edge[][1]),(0,255,0),2)
        if endPoint == -1 or startPoint == -1:
            continue
        matrix[startPoint][endPoint] = 1
        matrix[endPoint][startPoint] = 1
    print(matrix)

def main():
    global parser
    args = parser.parse_args()
    filename = args.filename
    image = cv.imread(filename)
    if image is None:
        print("Error: no such file or directory")
        return -1
    image = preprocessing(image)
    image = segmentation(image)
    

if __name__ == "__main__":
    args()
    main()
