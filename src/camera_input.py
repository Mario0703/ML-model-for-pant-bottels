import cv2
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera is not open")

while True:
    ret, frame = cap.read()    
    
