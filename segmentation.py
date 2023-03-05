import cv2 as cv
import numpy as np 

def segmentationMain(img):
    nodes = segmentationNodes(img)
    edges = segmentationEdges(nodes, img)
    matrix = matrixCreate(len(nodes))
    answer = topologyAnalysis(nodes, edges, matrix)
    return answer


def topologyAnalysis(nodes, edges, matrix):
    for edge in edges:
        startPoint = -1
        endPoint = -1

        for i in range(0, len(nodes)):
            center_x = nodes[i][0][0]
            center_y = nodes[i][0][1]
            startPoint_x = edge[0][0] - center_x
            startPoint_y = edge[0][1] - center_y
            #print(i, center_x, center_y, edge[0][0], edge[0][1], start_x, start_y, start_x*start_x + start_y*start_y, nodes[i][1])
            if startPoint_x**2 + startPoint_y**2 <= (nodes[i][1]+30)**2:
                startPoint = i
                break
        
        for i in range(0, len(nodes)):
            center_x = nodes[i][0][0]
            center_y = nodes[i][0][1]
            endPoint_x = edge[1][0] - center_x
            endPoint_y = edge[1][1] - center_y
            if endPoint_x**2 + endPoint_y**2 <= (nodes[i][1]+30)**2:
                endPoint = i
                break

        #print(endPoint, startPoint)
        # if endPoint == 0 or startPoint == 0:
        #     cv.line(segmentatedEdge,(edge[0][0], edge[0][1]),(edge[1][0],edge[][1]),(0,255,0),2) 

        if endPoint == -1 or startPoint == -1:
            continue
        matrix[startPoint][endPoint] = 1
        matrix[endPoint][startPoint] = 1
    return matrix


def segmentationNodes(img):
    kernel = np.ones((3,3),np.uint8)
    segmentatedNode = img
    img2 = img
    segmentatedNode = cv.erode(segmentatedNode,kernel,iterations = 25)
    segmentatedNode = cv.dilate(segmentatedNode,kernel,iterations = 25)
    cv.imwrite("debugPics/1segmentatedNode.png", segmentatedNode)
    contours, hierarchy = cv.findContours(segmentatedNode, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    nodes = []
    num = 0
    for cnt in contours:
        (x,y),radius = cv.minEnclosingCircle(cnt)
        center = (int(x), int(y))
        radius = int(radius)
        nodes.append([center, radius])       
        cv.putText(img2, str(num), center, cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 3)
        num+=1
    #print(nodes)
    cv.imwrite("debugPics/2numbersImage.png", img2)
    return nodes


def segmentationEdges(nodes, img):
    segmentatedEdge = img
    for node in nodes:
        cv.circle(segmentatedEdge, node[0], node[1]+10, (0,0,0), -1)
    cv.imwrite("debugPics/3segmentatedEdge.png", segmentatedEdge)

    lines = cv.HoughLinesP(
            segmentatedEdge, # Input edge image
            2, # Distance resolution in pixels
            np.pi/360, # Angle resolution in radians
            threshold=100, # Min number of votes for valid line
            minLineLength=25, # Min allowed length of line
            maxLineGap=50 # Max allowed gap between line for joining them
            )
    edges = []
    segmentatedEdgeColour = cv.cvtColor(segmentatedEdge, cv.COLOR_BGR2RGB)
    for points in lines:
        x1,y1,x2,y2=points[0]
        edges.append([(x1,y1), (x2,y2)])
        cv.line(segmentatedEdgeColour,(x1,y1),(x2,y2),(0,255,0),2)
    cv.imwrite("debugPics/4linesDrawed.png", segmentatedEdgeColour)
    
    #print(edges)
    return edges


def matrixCreate(x):
    matrix = []
    for i in range(x):
        matrix.append([])
        for j in range(x):
            matrix[i].append(0)
    return matrix