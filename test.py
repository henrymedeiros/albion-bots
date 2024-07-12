import random
import pyautogui
import time
import keyboard


from main import detect_green_bar
from main import control_cursor_within_bounds
from loguru import logger

start_point=(1819,822)
w,h = 40, 150
fishing_point = None

#TODO
# better logging
# organize codebase
# Add a way to detect if the fishing minigame has ended

def start_fishing():
    pyautogui.moveTo(fishing_point)
    pyautogui.mouseDown()
    time.sleep(random.uniform(0.4, 0.6)) # hold mouse
    pyautogui.mouseUp()
    time.sleep(2)



print('Script has started. Position the mouse on a body of water and wait.')
print('HELP: Press Q to quit.')

time.sleep(2.5)

fishing_point = pyautogui.position()

print('Fishing point: ', fishing_point)

start_fishing()

running = True

while running:
    #print('Taking screenshot...')
    if keyboard.is_pressed('q'):
        running = False
        print('Quitting...')
        raise KeyboardInterrupt
    screenshot = pyautogui.screenshot('albion-volume.png', region=(start_point[0], start_point[1], w, h))
    is_fishing = detect_green_bar('albion-volume.png')
    if is_fishing:
        print("Start Fishing Minigame!")
        pyautogui.click(fishing_point)
        time.sleep(0.5)
        pyautogui.mouseDown()
        time.sleep(random.uniform(0.4, 0.7)) # hold mouse to prevent cursor from moving left too fast
        result = control_cursor_within_bounds(cursor_template_path='fishing_cursor.png', left_edge=580, right_edge=735, threshold=0.85)
        if result == None:
            print("Fishing minigame ended. Trying to fish again...")
            time.sleep(2)
            start_fishing()
            

    time.sleep(0.1)  # Adjust the delay as needed