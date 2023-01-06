#!/usr/bin/env python3
# Author: Matthew Blair
# Date: Jan 2023
# PROJECT STATUS: VERY INCOMPLETE
#````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````
import pyautogui
import secrets
import time
from datetime import datetime, date
from math import ceil, radians, sin, cos
#`````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````
# VERY SPECIFIC PIXEL POSITIONS FOR WINDOWS GUI ELEMENTS (at 2560x1440 resolution)
# TODO: Try to generalize getting these for other resolutions, maybe other Windows versions and OS's
SCREEN_RESOLUTION = (2560, 1440)
FULLSCREEN_CENTER = (SCREEN_RESOLUTION[0] / 2, SCREEN_RESOLUTION[1] / 2)

SEARCH_BOX_X = 85
SEARCH_BOX_Y = 1413
TOP_RESULT_Y = 924

PAINT_FULLSCREEN_BUTTON_ORIGINAL = (1851, 76)
PAINT_WINDOW_ORIGINAL_CENTER = (1737, 705)

PAINT_BRUSH_BUTTON = (738, 75)

BRUSHES = {}

BRUSH_SIZES = {'1px': (738, 160), '3px': (738, 220), '5px': (738, 265), '8px': (738, 315)}

COLORS = {"BLACK": (884, 66), " GRAY_50": (933, 66), "DARK_RED": (959, 66), "RED": (982, 66), " ORANGE": (1007, 66),
          "YELLOW": (1032, 66), "GREEN": (1057, 66), "TURQUOISE": (1080, 66), "INDIGO": (1105, 66),
          "PURPLE": (1132, 66), "WHITE": (884, 95),
          "GRAY_25": (933, 95), "BROWN": (959, 95), "ROSE": (982, 95), "GOLD": (1007, 95), "LIGHT_YELLOW": (1032, 95),
          "LIME": (1057, 95), "LIGHT_TURQUOISE": (1080, 95), "BLUE_GRAY": (1105, 95), "LAVENDER": (1132, 95)}
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def move_north(x, y, amount):
    return x, y + amount


def move_south(x, y, amount):
    return x, y - amount


def move_east(x, y, amount):
    return x + amount, y


def move_west(x, y, amount):
    return x - amount, y


def move_southwest(x, y, amount):
    return x - amount, y - amount


def move_southeast(x, y, amount):
    return x + amount, y - amount


def move_northwest(x, y, amount):
    return x - amount, y + amount


def move_northeast(x, y, amount):
    return x + amount, y + amount


def limit_travel(new_x: int, new_y: int):
    if new_y < 0:
        new_y = 0
    elif new_y > SCREEN_RESOLUTION[1]:
        new_y = SCREEN_RESOLUTION[1]
    if new_x < 0:
        new_x = 0
    elif new_x > SCREEN_RESOLUTION[0]:
        new_x = SCREEN_RESOLUTION[0]
    return new_x, new_y


def move_random_direction(amount_max: int, duration_max: int):
  """Drags the cursor in ONE random cardinal or intercardinal direction from center screen (in 2-space)
  :param amount_max: upper limit for how far the cursor can move or be dragged in a single movement
  :param duration_max: upper limit for how long it takes for cursor to move the selected amount"""
    current_x, current_y = pyautogui.position()
    direction = secrets.choice(['N', 'S', 'E', 'W', 'NE', 'NW', 'SE', 'SW'])
    amount = secrets.choice([i for i in range(0, amount_max)])
    duration = secrets.choice([i for i in range(0, ceil(duration_max))])
    # print(pyautogui.position())
    match direction:
        case 'N':
            new_x, new_y = move_north(current_x, current_y, amount)
            new_x, new_y = limit_travel(new_x, new_y)
            pyautogui.dragTo(new_x, new_y, duration=duration, button='left')
            return new_x, new_y
        case 'S':
            new_x, new_y = move_south(current_x, current_y, amount)
            new_x, new_y = limit_travel(new_x, new_y)
            pyautogui.dragTo(new_x, new_y, duration=duration, button='left')
            return new_x, new_y
        case 'W':
            new_x, new_y = move_west(current_x, current_y, amount)
            new_x, new_y = limit_travel(new_x, new_y)
            pyautogui.dragTo(new_x, new_y, duration=duration, button='left')
            return new_x, new_y
        case 'E':
            new_x, new_y = move_east(current_x, current_y, amount)
            new_x, new_y = limit_travel(new_x, new_y)
            pyautogui.dragTo(new_x, new_y, duration=duration, button='left')
            return new_x, new_y
        case 'SE':
            new_x, new_y = move_southeast(current_x, current_y, amount)
            new_x, new_y = limit_travel(new_x, new_y)
            pyautogui.dragTo(new_x, new_y, duration=duration, button='left')
            return new_x, new_y
        case 'SW':
            new_x, new_y = move_southwest(current_x, current_y, amount)
            new_x, new_y = limit_travel(new_x, new_y)
            pyautogui.dragTo(new_x, new_y, duration=duration, button='left')
            return new_x, new_y
        case 'NE':
            new_x, new_y = move_northeast(current_x, current_y, amount)
            new_x, new_y = limit_travel(new_x, new_y)
            pyautogui.dragTo(new_x, new_y, duration=duration, button='left')
            return new_x, new_y
        case 'NW':
            new_x, new_y = move_northwest(current_x, current_y, amount)
            new_x, new_y = limit_travel(new_x, new_y)
            pyautogui.dragTo(new_x, new_y, duration=duration, button='left')
            # print(pyautogui.position())
            return new_x, new_y


def open_paint():
    """Searches for Paint app in user's search box (see REQUIREMENTS in preamble), opens it, maximizes the window, then calibrates the cursor to center screen"""
    pyautogui.moveTo(x=SEARCH_BOX_X, y=SEARCH_BOX_Y)
    pyautogui.click(x=SEARCH_BOX_X, y=SEARCH_BOX_Y, clicks=1)
    pyautogui.typewrite(message="paint")
    pyautogui.moveTo(x=SEARCH_BOX_X, y=TOP_RESULT_Y)
    pyautogui.click(x=SEARCH_BOX_X, y=TOP_RESULT_Y, clicks=2)
    # maximize window
    pyautogui.moveTo(x=PAINT_FULLSCREEN_BUTTON_ORIGINAL[0], y=PAINT_FULLSCREEN_BUTTON_ORIGINAL[1])
    pyautogui.sleep(2)
    # click to close search result box and recenter
    pyautogui.click(x=PAINT_FULLSCREEN_BUTTON_ORIGINAL[0], y=PAINT_FULLSCREEN_BUTTON_ORIGINAL[1], clicks=1)
    pyautogui.sleep(2)
    # print(f"{pyautogui.position()}")
    # center cursor
    pyautogui.moveTo(FULLSCREEN_CENTER[0], FULLSCREEN_CENTER[1])
    # print(f"{pyautogui.position()}")


def change_color1():
    # pick random new color
    new_color_button_pos = secrets.choice([_ for i, _ in COLORS.items()])
    pyautogui.moveTo(new_color_button_pos[0], new_color_button_pos[1])
    # select the color
    pyautogui.click(new_color_button_pos[0], new_color_button_pos[1], clicks=1)

    
def change_brush():
    # locate brush button, click it, recenter cursor
    # TODO: make a dict w/ brush name keys, coord vals
    pass

  
def change_brush_size():
    # select random new brush size
    new_brush_size_button_pos = secrets.choice([_ for i, _ in BRUSH_SIZES.items()])
    pyautogui.moveTo(new_brush_size_button_pos[0], new_brush_size_button_pos[1])
    # select the color
    pyautogui.click(new_brush_size_button_pos[0], new_brush_size_button_pos[1], clicks=1)


def make_chaotic_art(num_movements: int, amount_max: int, duration_max: float):
  """Generates weird tree branch-like art, with slight color changing, largely dictated by pseudorandom numbers"""
    open_paint()
    i = 0
    while i < num_movements:
        new_x, new_y = move_random_direction(amount_max=amount_max, duration_max=duration_max)
        # TODO: Make color change frequency a parameter to provide in main()
        # very arbitrary hard coded frequency for color changing 
        if i % 3 == 0:
            change_color1()
            # return cursor previous end point
            pyautogui.moveTo(new_x, new_y)
        i += 1

        
def main():
  # run basic drawing script to make some chaotic, yet beautiful art in MS Paint
  # HARD REQUIERMENTS: 
  # OS: Windows 10
  # Sceen Res: 2560, 1440
  # taskbar location: Bottom
  # Enable: 'Show Search Box' in taskbar menu
  start = datetime.now()
  make_chaotic_art(100, 3, 80)
  end = datetime.now()
  print(f"Elapsed Time: {()}")


if __name__ == '__main__':
    main()
