from pynput.keyboard import (
    Key,
    Listener as KeyboardListener,
    Controller as KeyboardController,
)
from pynput.mouse import (
    Button,
    Listener as MouseListener,
    Controller as MouseController,
)
from random import randrange
import time
import sys
import threading

if __name__ == "__main__":
    m = MouseController()
    run = True
    whitelisted_keys = [Key.tab, Key.alt_l, Key.cmd]

    def on_press(key):
        global run
        if key not in whitelisted_keys and run == True:
            run = False

    kblistener = KeyboardListener(on_press=on_press)

    kblistener.start()

    def loopThread():
        print("Starting anti-afk movements in 3 seconds", flush=True)
        print("Stop by pressing any key besides Alt, Tab and Win", flush=True)
        time.sleep(3)
        while run == True:
            time.sleep(randrange(2000) / 1000.0)
            randx = randrange(-100, 100)
            randy = randrange(-100, 100)
            holdTime = randrange(2000) / 1000.0 + 1
            print("X: ", randx, " Y: ", randy, "Holdtime: ", holdTime, flush=True)
            m.move(randx, randy)
            m.press(Button.left)
            time.sleep(holdTime)
            m.release(Button.left)
            time.sleep(0.5)
            m.move(-randx, -randy)

        print("Exiting application", flush=True)
        time.sleep(1)

    threading.Thread(target=loopThread).start()
