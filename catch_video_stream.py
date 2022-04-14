
import cv2

rtmp_addr = "rtmp://140.121.198.99:1935"

stream = cv2.VideoCapture(rtmp_addr)
# stream = cv2.VideoCapture(1)

stream.set(cv2.CAP_PROP_FPS, 150)
stream.set(cv2.CAP_PROP_BUFFERSIZE, 3)

while stream.isOpened():
    stream.grab()
    stream.grab()
    ret, img = stream.read()
    if not ret:
        print("\nCan't receive frame")
        break
    grayVideo = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow('streamed video', grayVideo)
    if cv2.waitKey(1) == ord('q'):
        break
stream.release()
cv2.destroyAllWindows()