import keyboard
import pyautogui
import time
import argparse

def map_nodes(num_nodes):
    nodes = []
    for i in range(1, num_nodes+1):
        print(f'Position the mouse on the {i} node and press Enter.')
        keyboard.wait('enter')
        node_position = pyautogui.position()
        print('Node position: ', node_position)
        time.sleep(.5)
        nodes.append(node_position)
    return nodes

def run_extraction_loop(nodes, interval):
    try:
        while True:
            for node in nodes:
                if keyboard.is_pressed('q'):
                    print("You pressed 'q', the loop will now stop.")
                    break
                pyautogui.click(node)
                time.sleep(interval)
            if keyboard.is_pressed('q'):
                print("You pressed 'q', the loop will now stop.")
                break
    except KeyboardInterrupt:
        print("Loop interrupted by user.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", help="Number of nodes to map", type=int, required=True)
    parser.add_argument("--i", help="Interval on which the node is gathered", type=float, required=True)
    args = parser.parse_args()

    nodes = map_nodes(args.n)
    print('Nodes interaction interval: ', args.i)
    print('Starting extraction loop...')
    time.sleep(2.5)

    run_extraction_loop(nodes, args.i)
if __name__ == '__main__':
    main()
