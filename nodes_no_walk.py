import threading
import keyboard
import pyautogui
import time
import argparse

#TODO
# optional argument to implement random delay to wait node replenish

def stop_loop():
    global running
    running = False
    print("You pressed 'q', the loop will now stop.")

def map_nodes(num_nodes):
    nodes = []
    for i in range(1, num_nodes+1):
        print(f'Position the mouse on node {i} and press Enter.')
        keyboard.wait('enter')
        node_position = pyautogui.position()
        print('Node position:', node_position)
        time.sleep(0.5)
        nodes.append(node_position)
    return nodes

def run_extraction_loop(nodes, interval):
    global running
    running = True
    while running:
        for node in nodes:
            if not running:
                break
            pyautogui.click(node)
            time.sleep(interval)

def monitor_key_press():
    keyboard.wait('q')
    stop_loop()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", help="Number of nodes to map", type=int, required=True)
    parser.add_argument("--i", help="Interval on which the node is gathered", type=float, required=True)
    args = parser.parse_args()

    nodes = map_nodes(args.n)
    print('Nodes interaction interval:', args.i)
    print('Starting extraction loop...')
    time.sleep(2.5)

    # Starting the keyboard monitoring in a separate thread
    threading.Thread(target=monitor_key_press, daemon=True).start()

    run_extraction_loop(nodes, args.i)

if __name__ == '__main__':
    main()
