import cv2

# Use 0 for default camera (this will use /dev/video0)
cap = cv2.VideoCapture(1)

# Check if the camera opened successfully
if not cap.isOpened():
    print("❌ Cannot open camera")
    exit()

print("✅ Camera opened successfully. Press 'q' to exit.")

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    print(frame)
    # If frame is read correctly ret is True
    if not ret:
        print("❌ Can't receive frame (stream end?). Exiting ...")
        break

    # Display the resulting frame
    _,image=cv2.imencode(".jpg",frame)
    print(image)
    # Press 'q' to quit the window
    if cv2.waitKey(1) == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

