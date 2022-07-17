from win32gui import FindWindow, GetWindowRect
import pyautogui
from pynput import keyboard
import numpy as np
import math
import cv2
import pyautogui
import matplotlib.pyplot as plt
import pygetwindow
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
win = pygetwindow.getWindowsWithTitle("ShellShock Live")[0]
win.size = (1920, 1080)
pyautogui.PAUSE = 0.03
angle_read = 0
power_read = 0

print("ready...")

def maths_stuff():

    get_window_size()
    global pos3a; global pos3b; global w; global h; 
    pos3a = abs(pos1a - pos2a) # x distance
    pos3b = pos1b - pos2b # y distance
    posRelA = pos3a / w #relative distance
    posRelB = pos3b / h #relative distance
    #print(posRelA, posRelB) #print relative distances
    myScreenshot2 = pyautogui.screenshot(region=(pos1a-60, pos1b+40, 120, 60))
    myScreenshot2.save(r'C:\Users\lewis\Desktop\SSL\SSL 2\SSL 2\imageMINI.jpg')
    imgg = cv2.imread("imageMINI.jpg")
    imgg_grey = cv2.cvtColor(imgg, cv2.COLOR_BGR2GRAY)
    (thresh, blackAndWhiteImage) = cv2.threshold(imgg_grey, 200, 255, cv2.THRESH_BINARY)     	
    #cv2.imshow('Black white image', blackAndWhiteImage)
    #cv2.waitKey()
    global text; global power_read; global angle_read
    text = pytesseract.image_to_string(blackAndWhiteImage, config='--psm 6 -c tessedit_char_whitelist=0123456789')
    #print(text)
    power_read = int(text[:2].strip())
    angle_read = int(text[len(text)-3:].strip())
    pre_sqrt1 = (379.106*np.power(pos3a, 2)) 
    pre_sqrt2 = (2 * np.power(np.cos(np.radians(angle_read)),2) * (np.tan(np.radians(angle_read)) * pos3a - pos3b))
    pre_sqrt3 = pre_sqrt1 / pre_sqrt2
    power_needed = 0.101704 * np.sqrt(abs(pre_sqrt3))
    print(np.rint(power_needed), "for angle", angle_read)
    power_needed = int(power_needed)
    #print("powerNeeded: ", power_needed)
    #print("powerRead: ", power_read)

    if pos1a > pos2a:
        pyautogui.keyDown("left")
        pyautogui.keyUp("left")
        myScreenshot2 = pyautogui.screenshot(region=(pos1a-60, pos1b+40, 120, 60))
        myScreenshot2.save(r'C:\Users\lewis\Desktop\SSL\SSL 2\SSL 2\imageMINI.jpg')
        imgg = cv2.imread("imageMINI.jpg")
        imgg_grey = cv2.cvtColor(imgg, cv2.COLOR_BGR2GRAY)
        (thresh, blackAndWhiteImage) = cv2.threshold(imgg_grey, 200, 255, cv2.THRESH_BINARY)
        text = pytesseract.image_to_string(blackAndWhiteImage, config='--psm 6 -c tessedit_char_whitelist=0123456789')
        angle_read2 = int(text[len(text)-3:].strip())
        pyautogui.keyDown("right")
        pyautogui.keyUp("right")

        if angle_read < angle_read2:
            diff2 = 2 * (90 - angle_read)
            for i in range(0, diff2):
                pyautogui.keyDown("left")
                pyautogui.keyUp("left")
    else:
        pyautogui.keyDown("left")
        pyautogui.keyUp("left")
        myScreenshot2 = pyautogui.screenshot(region=(pos1a-60, pos1b+40, 120, 60))
        myScreenshot2.save(r'C:\Users\lewis\Desktop\SSL\SSL 2\SSL 2\imageMINI.jpg')
        imgg = cv2.imread("imageMINI.jpg")
        imgg_grey = cv2.cvtColor(imgg, cv2.COLOR_BGR2GRAY)
        (thresh, blackAndWhiteImage) = cv2.threshold(imgg_grey, 200, 255, cv2.THRESH_BINARY)
        text = pytesseract.image_to_string(blackAndWhiteImage, config='--psm 6 -c tessedit_char_whitelist=0123456789')
        angle_read2 = int(text[len(text)-3:].strip())
        pyautogui.keyDown("right")
        pyautogui.keyUp("right")

        if angle_read > angle_read2:

            diff2 = 2 * (90 - angle_read)
            
            for i in range(0, diff2):
                pyautogui.keyDown("right")
                pyautogui.keyUp("right")

    if power_needed == power_read:
        print("fire! - already at the correct power")

    elif power_needed > power_read:
        diff = power_needed - power_read
        for i in range(0, diff+1):
            pyautogui.keyDown("up")
            pyautogui.keyUp("up")

    else:
        diff = power_read - power_needed
        for i in range(0, diff+1):
            pyautogui.keyDown("down")
            pyautogui.keyUp("down")

def get_window_size():
    global w; global h
    window_handle = FindWindow(None, "ShellShock Live")
    window_rect   = GetWindowRect(window_handle)
    pos1a = 0
    pos1b = 0
    pos2a = 0
    pos2b = 0
    pos3a = 0
    pos3b = 0

    x = window_rect[0]
    y = window_rect[1]
    w = window_rect[2] - x
    h = window_rect[3] - y

def on_press(key):
    try:

        if key.char == ('1'):

            print("Position 1 logged")
            global pos1a; global pos1b; 
            pos1a, pos1b = pyautogui.position()
            #print(pos1a, pos1b)
            
        elif key.char == ('2'):
            print("Position 2 logged")
            global pos2a; global pos2b; 
            pos2a, pos2b = pyautogui.position()
            #print(pos2a, pos2b)

        elif key.char == ('3'):
            maths_stuff()

        elif key.char == ('8'):
            quit()      
    except:
        pass

# Collect events until released
with keyboard.Listener(
        on_press=on_press)as listener:
    listener.join()
