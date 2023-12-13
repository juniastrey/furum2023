import os
import subprocess
import sys
import time

import cursor
from pynput import keyboard

import pdfgen

FRAMERATE = 24
WIDTH = 93
HEIGHT = 15
REPEAT = 2


def flush_input():
    # Adapted from: https://rosettacode.org/wiki/Keyboard_input/Flush_the_keyboard_buffer#Python
    try:
        import termios

        termios.tcflush(sys.stdin, termios.TCIOFLUSH)
    except ImportError:
        import msvcrt

        while msvcrt.kbhit():
            msvcrt.getch()


try:
    IS_DEVTERM = (
        b"devterm_printer"
        in subprocess.run(["lpstat", "-p"], capture_output=True).stdout
    )
except:
    IS_DEVTERM = False


def print_file(media, filename):
    if IS_DEVTERM:
        os.system(
            f"lp -d devterm_printer -o media={media} -o fit-to-page -o BlankSpace=True {filename}"
        )
    elif sys.platform == "win32":
        os.startfile(filename, "print")
    else:
        os.system(f"lp -o fit-to-page {filename}")


cursor.hide()

videos = []
for filename in sorted(os.listdir("videos")):
    if not filename.endswith(".txt"):
        continue
    with open("videos/" + filename, encoding="utf-8") as f:
        videos.append(f.read().split("\n\n\n"))

seconds_per_frame = 1 / FRAMERATE

auto = True
current = 0
count = 0
while True:
    with keyboard.Events() as events:
        enable_listener = True
        while enable_listener:
            for frame in videos[current]:
                start = time.time()
                print("\033[H" + frame[:-6], end="")
                event = events.get(max(0, seconds_per_frame - (time.time() - start)))
                if event is None or not isinstance(event, keyboard.Events.Release):
                    continue
                if event.key == keyboard.Key.esc:
                    cursor.show()
                    flush_input()
                    sys.exit()
                elif event.key == keyboard.Key.space:
                    current = (current + 1) % len(videos)
                    count = -1
                    break
                elif isinstance(event.key, keyboard.KeyCode) and isinstance(
                    event.key.char, str
                ):
                    if event.key.char.isdigit():
                        index = int(event.key.char)
                        if 0 < index <= len(videos):
                            auto = False
                            current = index - 1
                            count = -1
                            break
                    elif event.key.char.lower() == "a":
                        auto = True
                    elif event.key.char.lower() == "p":
                        print_file("X48MMY210MM", "thermal.pdf")
                    elif event.key.char.lower() == "c":
                        enable_listener = False
                        break
            count += 1
            if auto and count >= REPEAT:
                current = (current + 1) % len(videos)
                count = 0
    # If reached here, listener is disabled for user input.
    print("\033[39m\033[2J")
    cursor.show()
    flush_input()
    msg = input("Enter message: ")
    if msg.strip() != "":
        pdfgen.create_pdf(msg)
        print_file("X48MMY105MM", pdfgen.OUTPUT_FILENAME)
    cursor.hide()
