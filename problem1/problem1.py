import sys
import cv2
import numpy as np
import math

def show_image(name, image):
    cv2.imshow(name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def save_image(name, image):
    cv2.imwrite(name+".jpg", image)

def get_circle(blur_image, col_img):

    circles = cv2.HoughCircles(blur_image, cv2.HOUGH_GRADIENT, 1, 20, param1=20, param2=50, minRadius=20, maxRadius=150)
    if circles is None:
        return col_img

    circles = np.uint16(np.around(circles))[0]

    #sort the list according to radius in reverse order, so 0th pos will have the biggest circle in the image
    cx, cy, r = sorted(circles, key=lambda x: x[2], reverse=True)[0]
    # draw the outer circle
    cv2.circle(col_img, (cx, cy), r,(0,255,0),2)
    # draw the center of the circle
    cv2.circle(col_img, (cx, cy),2,(0,0,255),3)

    print("cx: {}, cy: {}, r:{}".format(cx, cy, r))

    #to find if input coord is within the find circle,
    #find eucledian distance of circle center coords and input coords
    #if eucledian distance is smaller than radius, it lies within the circle radius
    eucledian_dist = math.sqrt((int(cx)-int(input_coord[0]))**2 + (int(cy)-int(input_coord[1]))**2)
    print("Eucledian distance", eucledian_dist)

    if eucledian_dist < int(r):
        global point_status
        point_status = "Inside"

    return col_img


def main():
    #read the image in gray scale
    col_img = cv2.imread(image_path)
    image = cv2.cvtColor(col_img, cv2.COLOR_BGR2GRAY)

    #blur the image to get smoother edges, helps in detecting the contours
    blur = cv2.bilateralFilter(image, 9, 151, 151)
    final_img = get_circle(blur, col_img)

    save_image("final_image", final_img)

if __name__ == "__main__":
    arguments = sys.argv
    image_path = arguments[1]
    pixel_coord = arguments[2]
    point_status = "Outside"
    input_coord = tuple(pixel_coord.split(","))
    
    main()

    print(point_status)