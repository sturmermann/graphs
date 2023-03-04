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

def main():
    global parser
    args = parser.parse_args()
    filename = args.filename
    image = cv.imread(filename, cv.IMREAD_GRAYSCALE)
    if image is None:
        print("Error: no such file or directory")
        return -1
    #image = cv.resize(image, (1980, 1080))
    image = preprocessing(image)
    
    


if __name__ == "__main__":
    args()
    main()