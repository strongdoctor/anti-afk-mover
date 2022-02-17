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
import os
import json

if __name__ == "__main__":
    with open("config.json", "r") as f:
        config = json.load(f)

    def clearConsole():
        command = "clear"
        if os.name in ("nt", "dos"):  # If Machine is running on Windows, use cls
            command = "cls"
        os.system(command)

    def mainMenu():
        clearConsole()
        print("Anti AFK Mover", flush=True)
        print("Simulates input to avoid getting kicked for being AFK", flush=True)
        print("-------------------------", flush=True)
        print("[s] - start/stop", flush=True)
        print("[c] - configuration", flush=True)
        print("[e] - exit", flush=True)
        print("", flush=True)

    run = False

    def loopThread():
        global run
        m = MouseController()
        time.sleep(1)
        while run == True:
            randx = randrange(-100, 100)
            randy = randrange(-100, 100)

            if run == False:
                return

            m.move(randx, randy)
            m.press(Button.left)
            m.release(Button.left)

            if run == False:
                return

            time.sleep(0.5)

            if run == False:
                return

            m.move(-randx, -randy)

            sleep_time = randrange(config["minClickTime"], config["maxClickTime"])

            for x in range(sleep_time, 0, -1):
                if run == False:
                    return

                clearConsole()
                mainMenu()

                if run == True:
                    print(f"> Running.. (Waiting for {x} seconds)", flush=True)

                time.sleep(1)
                if run == False:
                    return

    def on_press(key):
        global run
        try:
            if key.char == "e":
                print("> Exiting..", flush=True)
                return False
            elif key.char == "c":
                mainMenu()
                print("> Not implemented yet :(", flush=True)
            elif key.char == "s":
                if run == False:
                    mainMenu()
                    print("> Running..", flush=True)
                    run = True
                    threading.Thread(target=loopThread).start()
                else:
                    run = False
                    mainMenu()
                    print("> Idle..", flush=True)

        except AttributeError:
            return

    kblistener = KeyboardListener(on_press=on_press)
    kblistener.start()

    mainMenu()
    print("> Idle..", flush=True)

    kblistener.join()
