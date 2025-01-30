import cv2
import numpy as np

def verification_function(robot, image, data_test):
    
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    

    lower_red1 = np.array([10, 125, 220])
    upper_red1 = np.array([160, 250, 255])  
    lower_red2 = np.array([30, 160, 237])
    upper_red2 = np.array([180, 235, 255])  
    
    # Create masks and combine them
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)
    
    # Morphological operations to reduce noise
    mask = cv2.erode(mask, None, iterations=4)
    mask = cv2.dilate(mask, None, iterations=2)
    
    # Find contours in the mask
    cnts, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
   
    marker_count = 0
    detected_positions = []
    
    # Process contours
    for c in cnts:
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        if radius>15:
            marker_count += 1
            detected_positions.append((int(x), int(y)))
    
   
    data_test.current_positions = detected_positions
    data_test.mqtt_messages.append(f"Detected {marker_count} markers")
    
   
    text_message = f"Detected {marker_count} verification markers"
    
    
    success = marker_count >= 2
    description = ("Verification successful: Minimum 2 markers detected" if success 
                   else "Verification failed: Insufficient markers detected")
    
    return data_test, text_message, Result(success, description)


class Result:
    def __init__(self, success, description):
        self.success = success
        self.description = description
