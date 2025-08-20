import os
import cv2
import matplotlib.pyplot as plt
import numpy as np

# Define save folder path and ensure it exists
save_folder = r"C:\projects\ai_quality_app\features\transforms_img"
os.makedirs(save_folder, exist_ok=True)


def detect_binary(img, background="black",  thresh_value=130):
    """
    Detect Binary image from the input image using a threshold.
    """

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)                              # convert the image to grayscle
    if background == "white":                                                   # Invert the colors if the background is white
        gray = cv2.bitwise_not(gray)

    # Save grayscale image
    gray_save_path = os.path.join(save_folder, "gray_inverted.png")
    cv2.imwrite(gray_save_path, gray)                                           # Save the gray image for debugging

    #create a binary threshold image
    _, binary = cv2.threshold(gray, thresh_value, 255, cv2.THRESH_BINARY)
    # binary = cv2.adaptiveThreshold(gray, 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,3, 2) 

    binary_save_path = os.path.join(save_folder, "binary.png")
    cv2.imwrite(binary_save_path, binary)                                        # Save the binary image for debugging

    return binary

    #find the contours from the thresholded image
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def detect_edges_and_contours(image, blur_kernel=(3, 3), canny_thresh1=50, canny_thresh2=150):

    image = image.copy()
    
    # Step 1: Blur to remove noise
    blurred = cv2.GaussianBlur(image, blur_kernel, 0)

    # Step 2: Canny edge detection
    edges = cv2.Canny(blurred, canny_thresh1, canny_thresh2)

    edge_save_path = os.path.join(save_folder, "edges.png")
    cv2.imwrite(edge_save_path, edges)             #Save the edges image for debugging

    # Step 3: Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def detect_edges_and_dilate(image, blur_kernel=(3, 3), canny_thresh1=50, canny_thresh2=150):
    image = image.copy()
    
    # Step 1: Blur to remove noise
    blurred = cv2.GaussianBlur(image, blur_kernel, 0)

    # Step 2: Canny edge detection
    edges = cv2.Canny(blurred, canny_thresh1, canny_thresh2)

    # Save original edges
    edge_save_path = os.path.join(save_folder, "edges.png")
    cv2.imwrite(edge_save_path, edges)

    # Step 3: Morphological operations to connect edges
    kernel = np.ones((3, 3), np.uint8)
    edges_dilated = cv2.dilate(edges, kernel, iterations=1)
    edges_closed = cv2.morphologyEx(edges_dilated, cv2.MORPH_CLOSE, kernel)

    # Save closed edges
    closed_edge_save_path = os.path.join(save_folder, "edges_closed.png")
    cv2.imwrite(closed_edge_save_path, edges_closed)

    # Step 4: Find contours on closed edges
    contours, _ = cv2.findContours(edges_closed, cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE)
    
    return contours



    # #retreive the biggest contour determined by area
    # biggest_contour = max(contours, key = cv2.contourArea) 

    # # #draw all contours
    # cv2.drawContours(image, contours, -1, (0, 255, 0), 1) # to check all contour
    # cv2.drawContours(image, biggest_contour, -1, (0, 0, 255), 3) # to check all contours
    
    # rect  = cv2. minAreaRect(biggest_contour) 
    # (center_x, center_y), (width, height), angle = rect


    # #convert the rect object to box points  
    # box = cv2.boxPoints(rect).astype('int')    # min area rect will have angle , this line of code rotate at that angle and find new cordinates [int is used to draw rectangle ]
    # cv2.drawContours(image,[box], 0, (255,0,0), 2)

    # return image

def draw_fitted_line(image, vx, vy, x0, y0, color=(0, 255, 0), thickness=2):
    height, width = image.shape[:2]

    # Extend the line to the image edges (x from 0 to width)
    left_y = int((-x0 * vy / vx) + y0)
    right_y = int(((width - x0) * vy / vx) + y0)

    pt1 = (0, left_y)
    pt2 = (width - 1, right_y)

    cv2.line(image, pt1, pt2, color, thickness)
    return image



# # --- Load image ---
# img = cv2.imread(r"c:\Users\melroy.pereira1\OneDrive - Autoliv\Documents\Autoliv\IMG_3825.jpg")

# # --- Detect contours ---
# contours = detect_contour_threshold(img, background="white")
# # contours =  detect_edges_and_contours(img, blur_kernel=(3, 3), canny_thresh1=30, canny_thresh2=100)
# print(len(contours), "contours found")

# # --- Draw all contours (optional, visualization) ---
# img = cv2.drawContours(img, contours, -1, (0,0,255), 10)
# # cv2.imwrite(f"{save_path_prefix}_contour.png", img)   

# #sort the contours in decreasing order
# # sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)

# # for i, cont in enumerate(sorted_contours[:1],1):  # t[:3] top 3

# #     #draw the contours
# #     cv2.drawContours(img, cont, -1, (0,255,0), 10)
# biggest_contour = max(contours, key = cv2.contourArea) 

# #calculate the minimum area bounding rect
# rect  = cv2. minAreaRect(biggest_contour)
# length = cv2.arcLength(biggest_contour, closed=True)
# print(f"Length of the biggest contour: {length:.2f}")

# # # Fit line to the contour
# # [vx, vy, x0, y0] = cv2.fitLine(biggest_contour, cv2.DIST_L2, 0, 0.01, 0.01)

# # # Draw fitted line
# # debug_img = draw_fitted_line(img, vx, vy, x0, y0)

# # cv2.imwrite("fitted_line_output.png", debug_img)


# #convert the rect object to box points  
# box = cv2.boxPoints(rect).astype('int')    # min area rect will have angle , this line of code rotate at that angle and find new cordinates [int is used to draw rectangle ]
# #draw a rectangle around the object
# cv2.drawContours(img,[box], 0, (255,0,0),10)

# # cv2.imwrite(f"{save_path_prefix}_final.png", img)  
# # # --- Sort contours by area (largest last) ---
# # contours_sorted = sorted(contours, key=cv2.contourArea)

# # # --- Draw top 20 largest contours (optional, visualization) ---
# # for i in range(min(100, len(contours_sorted))):
# #     cv2.drawContours(img, contours_sorted[i], -1, (0, 0, 255), 2)

# # # --- Get the largest contour ---
# # biggest_contour = contours_sorted[-1]

# # # --- Get min area rectangle ---
# # rect = cv2.minAreaRect(biggest_contour)
# # (center_x, center_y), (width, height), angle = rect

# # print(f"Center: ({center_x:.2f}, {center_y:.2f}), Width: {width:.2f}, Height: {height:.2f}, Angle: {angle:.2f}")

# # # --- Convert rect to box points and draw it ---
# # box = cv2.boxPoints(rect)
# # box = box.astype(int)
# # cv2.drawContours(img, [box], 0, (255, 0, 0), 4)

# # # --- Save final result ---
# # save_path_prefix = "result"
# # cv2.imwrite(f"{save_path_prefix}_contours.png", img)