import cv2
import numpy as np

# Define HSV color ranges for common balloon colors
color_ranges = {
    'red': [(0, 100, 100), (10, 255, 255)],
    'green': [(40, 70, 70), (80, 255, 255)],
    'blue': [(100, 150, 0), (140, 255, 255)],
    'yellow': [(20, 100, 100), (30, 255, 255)]
}

# Start webcam
cap = cv2.VideoCapture(0)  # 0 = default webcam

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the image (mirror view)
    frame = cv2.flip(frame, 1)

    # Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Loop through each color
    for color, (lower, upper) in color_ranges.items():
        lower_np = np.array(lower)
        upper_np = np.array(upper)

        # Create mask
        mask = cv2.inRange(hsv, lower_np, upper_np)

        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 800:  # ignore small blobs
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
                cv2.putText(frame, color, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    # Show the webcam feed
    cv2.imshow('Balloon Color Detection', frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
