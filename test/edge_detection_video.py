import cv2
import time
 
cv2.namedWindow("camera", 1)
 
video = 'http://192.168.44.88:4747/video'
 
capture = cv2.VideoCapture(video)
 
while True:
    sucess, img = capture.read()
    cv2.imshow("camera",img)
 
    if cv2.waitKey(1) == 27:
        break
 
capture.release()
cv2.destroyAllWindows()

# camera  = cv.VideoCapture('http://192.168.44.88:4747/video')

# while True:
#     ret, frame = camera.read()

#     if(ret):
#         print('empty')

#     cv.imshow('Camera', frame)

#     laplacian = cv.Laplacian(frame, cv.CV_64F)
#     laplacian = np.unit8(laplacian)
#     cv.imshow('Laplacian', laplacian)
    
#     if cv.waitKey(5) == ord('x'):
#         break

# camera.release()
# cv.destroyAllWindows()
