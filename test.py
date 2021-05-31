import platform
import cv2
import numpy as np

img_path = "dut.jpg"
wnd_title = "IPT Demo"

# 读取图像
img = cv2.imread(img_path)

# 读取图像大小 (height, width, depth)
img_height, img_width, _ = img.shape
print("原始图片大小：", img_width, img_height)

cv2.namedWindow(wnd_title, cv2.WINDOW_NORMAL)

# macOS 中 imshow() 会自动按照图像的原始比例显示；而 Windows 中需要手动调整显示窗口的大小；
# 未测试 Linux 下的情况
if platform.system() == "Windows":
    # 读取屏幕大小 (positionX, positionY, width, height)
    cv2.setWindowProperty(
        wnd_title, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    _, _, screen_width, screen_height = cv2.getWindowImageRect(wnd_title)
    print("屏幕分辨率：", screen_width, screen_height)

    # 按照图片比例设置显示窗口大小
    cv2.setWindowProperty(
        wnd_title, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
    wnd_height = screen_height - 100
    wnd_width = int(img_width * wnd_height / img_height)
    print("调整后显示窗口大小：", wnd_width, wnd_height)
    cv2.resizeWindow(wnd_title, wnd_width, wnd_height)

# 显示图像
cv2.imshow(wnd_title, img)
cv2.waitKey(0)

# 转灰度图像
img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
# 高斯滤波
img = cv2.GaussianBlur(img, (3, 3), sigmaX=2, sigmaY=2)
cv2.imshow(wnd_title, img)
cv2.waitKey(0)

# Canny 边缘检测
img = cv2.Canny(img, 20, 60)
cv2.imshow(wnd_title, img)
cv2.waitKey(0)

# 膨胀，连接边缘
img = cv2.dilate(img, np.ones((3, 3), np.uint8), iterations=3)
cv2.imshow(wnd_title, img)
cv2.waitKey(0)

# 提取轮廓
contours, hierarchy = cv2.findContours(
    img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
img = cv2.drawContours(img, contours, -1, (0, 0, 255), 5)
cv2.imshow(wnd_title, img)
cv2.waitKey(0)

cv2.destroyAllWindows()
