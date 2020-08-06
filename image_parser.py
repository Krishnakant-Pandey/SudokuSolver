import cv2
import os

current_directory = os.path.dirname(__file__)


def parse_img(image_name="sud2.jpg"):
    img = cv2.imread(image_name, 1)
    img = cv2.resize(img, (600, 600))

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, th1 = cv2.threshold(img_gray, 80, 155, cv2.THRESH_BINARY)
    th2 = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,
                                int((img_gray.shape[0]) / 9) - 1, 2)

    bfilt = cv2.bilateralFilter(th2, 9, 75, 75)
    filtered = cv2.medianBlur(bfilt, 3)
    canny = cv2.Canny(filtered, 100, 200)

    ext_contours, _ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    ext_contours = sorted(ext_contours, key=cv2.contourArea, reverse=True)

    sudoku_contour = ext_contours[0]

    def get_bottom_right(contour):
        max_total = 0
        loc = 0
        for index, pt in enumerate(contour):
            total = pt[0][0] + pt[0][1]
            if total > max_total:
                loc = index
                max_total = total
        x, y = contour[loc][0]
        return x, y

    def get_top_left(contour):
        min_total = 19000
        loc = 0
        for index, pt in enumerate(contour):
            total = pt[0][0] + pt[0][1]
            if total < min_total:
                loc = index
                min_total = total
        x, y = contour[loc][0]
        return x, y

    def get_top_right(contour):
        max_total = 0
        loc = 0
        for index, pt in enumerate(contour):
            total = pt[0][0] - pt[0][1]
            if total > max_total:
                loc = index
                max_total = total
        x, y = contour[loc][0]
        return x, y

    def get_bottom_left(contour):
        max_total = 0
        loc = 0
        for index, pt in enumerate(contour):
            total = pt[0][1] - pt[0][0]
            if total > max_total:
                loc = index
                max_total = total
        x, y = contour[loc][0]
        return x, y

    top_left = get_top_left(sudoku_contour)
    bottom_right = get_bottom_right(sudoku_contour)
    top_right = get_top_right(sudoku_contour)
    bottom_left = get_bottom_left(sudoku_contour)

    # use the following to verify if the program identified the sudoku grid from the img
    image = cv2.rectangle(img, bottom_left, top_right, (0, 0, 255), 3)
    cv2.imshow(" ", image)
    cv2.imshow(" ", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.drawContours(img, ext_contours[0], -1, (0, 0, 255), 2)

    crop_img = filtered[top_left[1]: bottom_left[1], top_left[0]: top_right[0]]
    crop_img = cv2.resize(crop_img, (720, 720))

    for x in range(9):
        for y in range(9):
            a, b = 80 * x, 80 * y
            crop_image = crop_img[b: b + 80, a:a + 80]
            name = os.path.join(current_directory, 'digit_repository', f'({x, y}).jpg')

            crop_image = cv2.bilateralFilter(crop_image, 9, 75, 75)
            crop_image = cv2.medianBlur(crop_image, 3)
            crop_image = crop_image[10:70, 10:70]

            cv2.imwrite(name, crop_image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
