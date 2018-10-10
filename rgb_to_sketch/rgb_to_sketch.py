# -*- coding: utf-8 -*-

import cv2
import matplotlib.pyplot as plt

def rgb_to_sketch_v2(src_image_name):

    # 加载灰度图
    img_gray = cv2.imread(src_image_name, cv2.IMREAD_GRAYSCALE)

    # 高斯模糊
    img_blur = cv2.GaussianBlur(img_gray, (21, 21), 0, 0)

    #
    img_blend = cv2.divide(img_gray, img_blur, scale=256)

    img_result = cv2.cvtColor(img_blend, cv2.COLOR_GRAY2BGR)

    return img_result


if __name__ == "__main__":
    image = rgb_to_sketch_v2('squirrel.jpeg')

    cv2.imwrite('squirrel_sketch.jpeg', image)

    # plt.imshow(image)
    # plt.show()

    # cv2.imshow('素描', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
