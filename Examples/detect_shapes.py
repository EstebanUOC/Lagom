import cv2


import numpy as np

def detect_shapes(image_path):
    # Load image and preprocess
    image = cv2.imread(image_path)
    resized = cv2.resize(image, (640, 480))
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # Approximate the contour
        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # Get the coordinates for drawing
        x, y, w, h = cv2.boundingRect(approx)

        # Identify the shape based on number of vertices
        if len(approx) == 3:
            shape_name = "Triangle"
        elif len(approx) == 4:
            aspect_ratio = w / float(h)
            shape_name = "Square" if 0.95 < aspect_ratio < 1.05 else "Rectangle"
        elif len(approx) > 8:
            shape_name = "Circle"
        else:
            shape_name = "Polygon"

        # Draw contours and label
        cv2.drawContours(resized, [approx], -1, (0, 255, 0), 2)
        cv2.putText(resized, shape_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, (255, 0, 0), 2)

    # Show result
    cv2.imshow("Shape Detection", resized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
detect_shapes("shapes.png")  # Replace with your image path
