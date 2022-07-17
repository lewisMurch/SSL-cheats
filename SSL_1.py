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
    myScreenshot2.save(r'C:\Users\lewis\Desktop\SSL\SSL 1\imageMINI.jpg')
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

    initial_vel = 9.8324553054 * power_read
    initial_vel_y = initial_vel * np.sin(np.radians(angle_read))
    sqrt_for_time = (initial_vel_y*initial_vel_y) + (2*pos3b*-379.106)


    time_of_flight1 = (-initial_vel_y - np.sqrt(sqrt_for_time))/-379.106

    if time_of_flight1 < 0:
        time_of_flight1 = (-initial_vel_y + np.sqrt(sqrt_for_time))/-379.106
    else:
        pass

    initial_vel_x = initial_vel * np.cos(np.radians(angle_read))
    global y_list1; 
    global x_list1; 
    i=0.0
    y_list1 = []; 
    x_list1 = [];

    while i < time_of_flight1:
        y_position_in_flight = -((initial_vel_y * i) + (0.5 * -379.106 * i * i)) + pos1b
        y_list1.append(y_position_in_flight)

        if pos1a > pos2a:
            x_position_in_flight = (initial_vel_x * -i) + pos1a
        else:
            x_position_in_flight = -(initial_vel_x * -i) + pos1a

        x_list1.append(x_position_in_flight)


        i += 0.05

    y_list1 = np.array(y_list1); 
    x_list1 = np.array(x_list1);
    #print(x_list1); print(y_list1)
    draw_graph()




def draw_graph():

    myScreenshot = pyautogui.screenshot()
    myScreenshot.save(r'C:\Users\lewis\Desktop\SSL\SSL 1\image.jpg')
    img = cv2.imread("image.jpg")

    xx = x_list1
    yy = y_list1





    z = np.polyfit(xx, yy, 2)
    draw_x = xx
    draw_y = np.polyval(z, draw_x)   # evaluate the polynomial
    draw_points = (np.asarray([draw_x, draw_y]).T).astype(np.int32)   # needs to be int32 and transposed
    cv2.polylines(img, [draw_points], False, (0,255,0), 6)  # args: image, points, closed, color, thickness
    cv2.imshow("Angle of shot", img)
    cv2.waitKey(1)
    maths_stuff()




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

























