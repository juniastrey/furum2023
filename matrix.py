import random
import sys
import time

import colorama

RESET = "\033[H"

WIDTH = 93
HEIGHT = 15

FPS = 24
seconds_per_frame = 1 / FPS

FAST_PERIOD = 2
SLOW_PERIOD = FAST_PERIOD * 2
STREAK = 2 * FPS
COLORS = [colorama.Fore.BLACK, colorama.Fore.GREEN, colorama.Fore.LIGHTGREEN_EX]

CHARS = [
    # Adapted from: https://rosettacode.org/wiki/Matrix_digital_rain#Rust
    'ｰ', 'ｱ', 'ｲ', 'ｳ', 'ｴ', 'ｵ', 'ｶ', 'ｷ', 'ｸ', 'ｹ', 'ｺ', 'ｻ', 'ｼ', 'ｽ', 'ｾ', 'ｿ', 'ﾀ', 'ﾁ', 'ﾂ', 'ﾃ', 'ﾄ', 'ﾅ', 'ﾆ',
    'ﾇ', 'ﾈ', 'ﾉ', 'ﾊ', 'ﾋ', 'ﾌ', 'ﾍ', 'ﾎ', 'ﾏ', 'ﾐ', 'ﾑ', 'ﾒ', 'ﾓ', 'ﾔ', 'ﾕ', 'ﾖ', 'ﾗ', 'ﾘ', 'ﾙ', 'ﾚ', 'ﾛ', 'ﾜ', 'ﾝ',
]

CHARS = CHARS[: (len(CHARS) // HEIGHT) * HEIGHT]

DURATION = (WIDTH // len(CHARS) + 1) * len(CHARS)

timeline = [None] * DURATION
for col in range(WIDTH):
    while True:
        t = random.randrange(DURATION)
        if timeline[t] is None:
            break
    timeline[t] = col

ycoords = [None] * WIDTH
timeleft = [None] * WIDTH
indices = [None] * WIDTH

screen_timeleft = [
    [random.randrange(SLOW_PERIOD) for _ in range(WIDTH)] for _ in range(HEIGHT)
]
screen_indices = [
    [random.randrange(len(CHARS)) for _ in range(WIDTH)] for _ in range(HEIGHT)
]
screen_brightness = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]

frames = []
for i in range(5):
    for t in range(DURATION):
        screen = [
            [f"{colorama.Fore.RESET} " for _ in range(WIDTH)] for _ in range(HEIGHT)
        ]
        event = timeline[t]
        if event is not None:
            ycoords[event] = 0
            timeleft[event] = FAST_PERIOD
            indices[event] = random.randrange(len(CHARS))
        for col in range(WIDTH):
            for row in range(HEIGHT):
                if screen_timeleft[row][col] == 0:
                    screen_indices[row][col] = (screen_indices[row][col] + 1) % len(
                        CHARS
                    )
                    screen_timeleft[row][col] = SLOW_PERIOD
                else:
                    screen_timeleft[row][col] -= 1
                if screen_brightness[row][col] > 0:
                    screen_brightness[row][col] -= 1
                    brightness = int((screen_brightness[row][col] / STREAK) * 256)
                    screen[row][
                        col
                    ] = f"\033[38;2;{brightness};{brightness};{brightness}m{CHARS[screen_indices[row][col]]}"
            if timeleft[col] is None:
                continue
            if timeleft[col] == 0:
                ycoords[col] += 1
                if ycoords[col] >= HEIGHT:
                    ycoords[col] = None
                    timeleft[col] = None
                    indices[col] = None
                    continue
                else:
                    timeleft[col] = FAST_PERIOD
                    indices[col] = (indices[col] + 1) % len(CHARS)
            else:
                timeleft[col] -= 1
            row = ycoords[col]
            screen[row][col] = f"\033[38;2;255;255;255m{CHARS[indices[col]]}"
            screen_brightness[row][col] = STREAK

        if i == 4:
            frames.append(RESET + "\n".join(["".join(row) for row in screen]))

if __name__ == "__main__":
    if len(sys.argv) == 1:
        while True:
            for frame in frames:
                print(RESET + frame, end="")
                time.sleep(seconds_per_frame)
    else:
        with open(sys.argv[1], "w", encoding="utf-8") as f:
            f.write("\n\n\n".join(frames))
