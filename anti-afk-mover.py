from enum import Enum
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
import configparser
import ctypes

if __name__ == "__main__":
    os.system("mode con: cols=70 lines=15")
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 128)

    configParser = configparser.ConfigParser()
    configParser.read("config.toml")

    config = configParser["DEFAULT"]

    startKey = config["startkey"].strip('"')
    exitKey = config["exitKey"].strip('"')

    class Path(Enum):
        HOME = 0
        RUNNING = 1

    def clearConsole():
        command = "clear"
        if os.name in ("nt", "dos"):  # If Machine is running on Windows, use cls
            command = "cls"
        os.system(command)

    def clearLines(lines: int):
        sys.stdout.write("\r\033[K")
        for _ in range(lines):
            sys.stdout.write("\033[A\r\033[K")
        sys.stdout.flush()

    def printCurrLine(string: str):
        sys.stdout.write("\r\033[K" + string)
        sys.stdout.flush()

    def appHeader():
        print("Anti AFK Mover", flush=True)
        print("Simulates input to avoid getting kicked for being AFK", flush=True)
        print("-------------------------", flush=True)

    def mainMenu():
        print(f"[{startKey}] - start/stop")
        exitKeys = ", ".join({"e", exitKey})
        print(f"[{exitKeys}] - exit")
        sys.stdout.flush()

    run = False

    path = Path.HOME

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

            sleep_time = randrange(
                int(config["minclicktime"]), int(config["maxclicktime"])
            )

            for x in range(sleep_time, 0, -1):
                if run == False:
                    return

                if run == True:
                    printCurrLine("> Running.. (Waiting for " + str(x) + " seconds)")

                time.sleep(1)
                if run == False:
                    return

    def on_press(key):
        global run
        global path
        try:
            if key.char == "e":
                print("\n> Exiting..", flush=True)
                run = False
                # Give time for thread to gracefully shut down
                time.sleep(2)
                return False

            elif key.char == startKey:
                if run == False:
                    path = Path.RUNNING
                    clearLines(3)
                    mainMenu()
                    sys.stdout.write("\r\033[K\n")
                    printCurrLine("> Running..")
                    run = True
                    threading.Thread(target=loopThread).start()
                else:
                    path = Path.HOME
                    run = False
                    clearLines(3)
                    mainMenu()
                    sys.stdout.write("\r\033[K\n")
                    printCurrLine("> Idle..")

        except AttributeError:
            return

    kblistener = KeyboardListener(on_press=on_press)
    kblistener.start()

    appHeader()
    mainMenu()
    print("")
    printCurrLine("> Idle..")

    kblistener.join()
