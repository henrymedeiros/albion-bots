import random
import cv2
import numpy as np
import pyautogui
import time
import keyboard

def detect_green_bar(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert to HSV (Hue, Saturation, Value) color space to detect green color
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define range for green color and create a mask
    lower_green = np.array([40, 40, 40])
    upper_green = np.array([70, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Assume the largest contour is the green bar
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)

        # Draw rectangle around the green bar
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Check if the green bar is large enough (adjust the threshold as needed)
        threshold_height = 21  # Example threshold
        if h >= threshold_height:
            print('Height: ', h)
            print("Large green bar detected!")
            return True
        
def locate_cursor(main_image, cursor_template, threshold=0.85, plot_cursor=False):
    # Convert images to grayscale
    main_gray = cv2.cvtColor(main_image, cv2.COLOR_BGR2GRAY)
    cursor_template_gray = cv2.cvtColor(cursor_template, cv2.COLOR_BGR2GRAY)

    # Use template matching to find the cursor
    result = cv2.matchTemplate(main_gray, cursor_template_gray, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= threshold)

    cursor_position = None
    for pt in zip(*loc[::-1]):
        cursor_position = pt
        break  # Only take the first match

    if plot_cursor and cursor_position:
        cursor_h, cursor_w = cursor_template.shape[:2]
        top_left = cursor_position
        bottom_right = (top_left[0] + cursor_w, top_left[1] + cursor_h)
        cv2.rectangle(main_image, top_left, bottom_right, (0, 0, 255), 2)
        cv2.imshow("Cursor Position", main_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return cursor_position, cursor_template.shape[:2]


def control_cursor_within_bounds(cursor_template_path, left_edge: int, right_edge: int, threshold=0.85):

    cursor_template = cv2.imread(cursor_template_path)
    if cursor_template is None:
        print(f"Failed to load cursor template from path: {cursor_template_path}")
        return
    
    margin = 50  # Margin to avoid edges

    while True:
        if keyboard.is_pressed('q'):
            print('Quitting...')
            raise KeyboardInterrupt
        screenshot = pyautogui.screenshot()
        main_image = np.array(screenshot)
        main_image = cv2.cvtColor(main_image, cv2.COLOR_RGB2BGR)

        # Locate cursor
        cursor_position, cursor_size = locate_cursor(main_image, cursor_template, threshold)

        if cursor_position:
            cursor_x = cursor_position[0] + cursor_size[1] // 2  # Center of the cursor

            # print(f"Cursor X: {cursor_x}") #debug

            # Control mouse to keep cursor within bounds
            if cursor_x > right_edge - margin:
                random_delay = random.uniform(0.4, 0.7)
                print(f'MOUSE NEAR RIGHT EDGE, REALEASING FOR {random_delay} SECONDS...')
                pyautogui.mouseUp()
            elif cursor_x < left_edge + margin:
                random_delay = random.uniform(0.6, 1.2)
                print(f'MOUSE NEAR LEFT EDGE, PRESSING FOR {random_delay} SECONDS...')
                pyautogui.mouseDown()
            else:
                print('DEFAULT PRESSING AND RELEASE STATE...')
                pyautogui.mouseUp()
                time.sleep(random.uniform(0.15, 0.25))
                pyautogui.mouseDown()
                time.sleep(random.uniform(0.5, 0.8))


        if not cursor_position:
            pyautogui.mouseUp()
            print("Cursor not found. Stopping the script.")
            return

        # Small delay to prevent too fast loops
        #time.sleep(0.01)
