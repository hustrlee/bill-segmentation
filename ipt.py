import cv2
import numpy as np

imgPath = "dut.jpg"
wndTitle = "IPT Demo"

# 读取图像
img = cv2.imread(imgPath)
# 读取图像大小 (height, width, depth)
imgSize = img.shape
print(imgSize)

# 读取屏幕大小 (positionX, positionY, width, height)
cv2.namedWindow(wndTitle, cv2.WINDOW_NORMAL)
cv2.setWindowProperty(wndTitle, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
screenSize = cv2.getWindowImageRect(wndTitle)
print(screenSize)

# 按照图片比例设置显示窗口大小
cv2.setWindowProperty(wndTitle, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
wndHeight = screenSize[3] - 100
wndWidth = int(imgSize[1] * wndHeight / imgSize[0])
print(wndWidth, wndHeight)
cv2.resizeWindow(wndTitle, wndWidth, wndHeight)

# 显示图像
cv2.imshow("IPT Demo", img)


# 按任意键退出
cv2.waitKey(0)
cv2.destroyAllWindows()
