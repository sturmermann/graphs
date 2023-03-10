import argparse
import cv2 as cv
import numpy as np 
import matplotlib.pyplot as plt
import preprocessing as prp
import segmentation as sgn
import postprocessing as psp
import consoleStuff


def debug():
    prp.binarizationTests(["TestCases/1.png", "TestCases/2.png", "TestCases/3.png", "TestCases/4.png", "TestCases/5.png"])

def main():
    parser = consoleStuff.argsMain()
    args = parser.parse_args()
    filename = args.filename
    image = cv.imread(filename)
    if image is None:
        print("Error: no such file or directory")
        return -1
    image = prp.preprocessingMain(image)  
    matrix = sgn.segmentationMain(image)
    print(matrix)
    psp.postprocessingMain(matrix)
    return 1


if __name__ == "__main__":
    main()
