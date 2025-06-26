import cv2
import numpy as np

def identify_object(contour, frame):
    area = cv2.contourArea(contour)
    if area < 1000:
        return None

    x, y, w, h = cv2.boundingRect(contour)
    aspect_ratio = float(w)/h
    approx = cv2.approxPolyDP(contour, 0.03*cv2.arcLength(contour, True), True)

    # Extract ROI to check color
    mask = np.zeros(frame.shape[:2], dtype=np.uint8)
    cv2.drawContours(mask, [contour], -1, 255, -1)
    mean_color = cv2.mean(frame, mask=mask)
    b, g, r = mean_color[:3]

    # Balloon (Red)
    if len(approx) > 6 and r > 100 and r > g + 40 and r > b + 40:
        return "Balloon"

    # Bright Yellow Sticky Note (Square)
    if len(approx) == 4 and 0.9 < aspect_ratio < 1.1:
        if r > 200 and g > 200 and b < 100:
            return "Sticky Note"

    # Water Bottle (Tall & Slim)
    if aspect_ratio < 0.6 and h > 1.5 * w:
        return "Water Bottle"

    return None

# Camera setup
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    blurred = cv2.GaussianBlur(frame, (5, 5), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        obj = identify_object(cnt, frame)
        if obj:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
            cv2.putText(frame, obj, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)

    cv2.imshow("Better Object Detection", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
