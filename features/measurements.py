import cv2
import numpy as np
from .contour import detect_binary


def measure_contour(contours, image):
    
    biggest_contour = max(contours, key=cv2.contourArea)

    rect = cv2.minAreaRect(biggest_contour)
    (center_x, center_y), (width, height), angle = rect

    # Convert the rect object to box points
    box = cv2.boxPoints(rect).astype('int')  
    cv2.drawContours(image, [box], 0, (255, 0, 0), 2)

    return width, height


def scaled_distance(p1, p2, mm_per_px_x, mm_per_px_y):
    """
    Compute the real-world distance between two points when X and Y
    have different mm-per-pixel scaling.
    """
    dx_mm = (p2[0] - p1[0]) * mm_per_px_x
    dy_mm = (p2[1] - p1[1]) * mm_per_px_y
    return np.sqrt(dx_mm**2 + dy_mm**2)


def draw_measurement(image, width_mm, height_mm):
    """
    Draw the measurement on the image.
    """
    text = f"Width: {width_mm:.2f} mm, Height: {height_mm:.2f} mm"
    cv2.putText(image, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    return image


def measure_locking_bar(img, mm_per_px_x=0.047700, mm_per_px_y=0.047610):                 
    # NOTE: need to make sure i select locking bar biggest may not be correct way to identify locking bar Also if contour is not deteted we should handle that too
    """
    Detect locking bar and measure its length in mm.
    Returns:
        processed_image, measurement_value_mm
    """
    # 1. Preprocess image to binary
    binary = detect_binary(img, background="black",  thresh_value=140)

    # 2. Find contours
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
   
    # 3. Select largest contour
    biggest_cnt = max(contours, key=cv2.contourArea)

    # 4. Minimum area rectangle
    rect = cv2.minAreaRect(biggest_cnt)
    box = cv2.boxPoints(rect).astype(np.float32)

    # 5. Calculate both side lengths in mm
    side1_mm = scaled_distance(box[0], box[1], mm_per_px_x, mm_per_px_y)
    side2_mm = scaled_distance(box[1], box[2], mm_per_px_x, mm_per_px_y)

    # 6. Select the larger dimension as measurement
    dimension_mm = max(side1_mm, side2_mm)
    dimension_mm = round(dimension_mm, 4)
    # 7. Draw contours and rectangle
    cv2.drawContours(img, [biggest_cnt], -1, (0, 0, 255), 3)  # Red contour
    cv2.drawContours(img, [box.astype(int)], 0, (255, 0, 0), 2)  # Blue min area rect

    return img, dimension_mm


