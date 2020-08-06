import cv2
import pytesseract
from image_parser import parse_img
import os
import threading

current_directory = os.path.dirname(__file__)


def recognize_image(image_name="sud2.jpg"):
    parse_img(image_name)

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
    numbers = {'1', '2', '3', '4', '5', '6', '7', '8', '9'}
    arr = [[0] * 9 for i in range(9)]

    def digit_recognization(x, y):

        name = os.path.join(current_directory, 'digit_repository', f'({x, y}).jpg')

        img = cv2.imread(name)

        text = pytesseract.image_to_string(img, config='--psm 6')
        if text == '':
            arr[y][x] = 0
        elif text in numbers:

            arr[y][x] = int(text)

    thread_list = []
    for x in range(9):
        for y in range(9):
            t = threading.Thread(target=digit_recognization, args=(x, y))
            t.start()
            thread_list.append(t)

    for thread in thread_list:
        thread.join()

    return arr
