import cv2 as cv
import numpy as np

def preprocessingMain(img):
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img = cv.resize(img, (1020, 980))
    h,w=img.shape
    bg=np.array([ [img[0,0], img[0,-1]],[img[-1,0],img[-1,-1]] ])
    bg=cv.resize(bg, (w, h))
    img=cv.absdiff(img,bg)
    bw=cv.threshold(img, 40, 255, cv.THRESH_BINARY_INV)[1]
    retval, labels, stats, centroids=cv.connectedComponentsWithStats(bw)
    idx=np.nonzero(stats[:,4]<5000) # select by area
    bw=bw-255*np.isin(labels, idx)
    bw=cv.bitwise_not(np.uint8(bw))
    cv.imwrite("debugPics/0imgAfterPreprocessing.png", bw)
    return bw

def alternativeGaussianPreprocessing(img):
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img = cv.resize(img, (1020, 980))
    img = cv.GaussianBlur(img,(11, 11),0)
    img = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY_INV,11,2)
    cv.imwrite("debugPics/0imgAfterPreprocessing.png", img)
    return img

def alternativeOtsuPreprocessing(img):
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img = cv.resize(img, (1020, 980))
    #img = cv.GaussianBlur(img,(5,5),0)
    hist,img = cv.threshold(img,0,255,cv.THRESH_BINARY_INV+cv.THRESH_OTSU)
    cv.imwrite("debugPics/0imgAfterPreprocessing.png", img)
    return img

def binarizationTests(imgs):
    num = 0
    for i in imgs:
        img = cv.imread(i)
        cv.imwrite(f"debugPics/img{num}AfterPreprocessingGaussian.png", alternativeGaussianPreprocessing(img) )
        cv.imwrite(f"debugPics/img{num}AfterPreprocessingOtsu.png",  alternativeOtsuPreprocessing(img) )
        cv.imwrite(f"debugPics/img{num}AfterPreprocessingMain.png", preprocessingMain(img) )
        num+=1
