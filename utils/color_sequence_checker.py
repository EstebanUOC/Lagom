import cv2
import numpy as np


def are_objects_in_correct_order(frame, color_ranges, target_positions, tolerance=200):
    """
    Checks if the objects of specified colors are near their target positions and in correct x-order.

    Parameters:
        - frame: OpenCV image frame (BGR)
        - color_ranges: dict of HSV ranges
        - target_positions: dict like {'yellow': (x1, y1), 'green': (x2, y2)}
        - tolerance: pixel tolerance for matching positions

    Returns:
        True if all objects are near targets and ordered by x-axis (left-to-right).
    """

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    positions = {}

    for color, (lower, upper) in color_ranges.items():
        if color not in target_positions:
            continue

        print(f"[DEBUG] Checking color: {color}")
        mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 800:
                x, y, w, h = cv2.boundingRect(cnt)
                center = (x + w // 2, y + h // 2)
                #print(f"[DEBUG] Found {color} object at {center} with area {area}")
                if color not in positions or area > positions[color][1]:
                    positions[color] = (center, area)

    ordered_colors = list(target_positions.keys())
    detected = []

    for color in ordered_colors:
        if color not in positions:
            print(f"[DEBUG] ❌ {color} not detected")
            return False

        (x, y), _ = positions[color]
        tx, ty = target_positions[color]

        print(f"[DEBUG] {color}: detected at ({x}, {y}), target is ({tx}, {ty})")
        if abs(x - tx) > tolerance or abs(y - ty) > tolerance:
            print(f"[DEBUG] ❌ {color} is out of tolerance")
            return False

        detected.append((color, x))

    print("[DEBUG] ✅ All objects are near their target positions")
    return True