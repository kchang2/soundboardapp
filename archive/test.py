import numpy as np
import cv2
import time

for i in xrange(-10, 100):
    cap = cv2.VideoCapture(i)
    print i, cap.isOpened()
    cap.release()
# while(True):
#     # Capture frame-by-frame
#     ret, frame = cap.read()

#     # Our operations on the frame come here
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     # Display the resulting frame
#     cv2.imshow('frame',gray)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()