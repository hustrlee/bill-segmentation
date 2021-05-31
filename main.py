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

# 绘制 4 边形的 ROI 区域
# 使用鼠标左键依次确定 4 个顶点；鼠标右键取消上一个顶点

roi_pts = []  # 用于存放 4 个顶点

# 自动获取顶点

# 监听鼠标事件，进行描点


def define_roi(event, x, y, flags, param):
    global roi_pts

    def draw_roi():
        imgMask = img.copy()  # 保留原始图像，在 imgMask 上绘制 ROI 区域

        # 绘制所有的点，及连线
        for i in range(len(roi_pts)):
            cv2.circle(imgMask, roi_pts[i], 12, (0, 0, 255), -1)
            if i > 0:
                cv2.line(imgMask, roi_pts[i-1], roi_pts[i], (0, 0, 255), 2)
                if i == 3:  # 最后一个顶点，需要增加起点到终点的连线
                    cv2.line(imgMask, roi_pts[0], roi_pts[i], (0, 0, 255), 2)
        cv2.imshow(wnd_title, imgMask)

    if event == cv2.EVENT_LBUTTONDOWN:
        if len(roi_pts) < 4:  # 不足 4 个顶点，则将该点加入到顶点数组，并绘制 ROI 区域
            roi_pts.append([x, y])
            draw_roi()

    if event == cv2.EVENT_RBUTTONDOWN:
        if len(roi_pts) > 0:  # 至少有 1 个顶点，则删除最后一个顶点，并绘制 ROI 区域
            roi_pts.pop()
            draw_roi()


# 监控鼠标事件，定义 ROI 区域
cv2.setMouseCallback(wnd_title, define_roi)

# 等待按键：
# ESC：退出
# Enter：确定 ROI 区域
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break
    if key == 13:
        # 对 ROI 区域进行透视变换，并显示
        # 将四边形的顶点按逆时针排序：（右上、左上，左下，右下）
        print("ROI 顶点：", roi_pts)
        # 计算四边形的质心
        centroid = [0.0, 0.0]
        for i in range(0, 3):
            centroid[0] += roi_pts[i][0]
            centroid[1] += roi_pts[i][1]
        centroid[0] = centroid[0] / 4
        centroid[1] = centroid[1] / 4
        print("ROI 质心：", centroid)

        # 通过比较各点到质心的角度进行排序
        def phase_angle(point):
            return cv2.fastAtan2(
                point[1] - centroid[1], point[0] - centroid[0])
        sorted_roi_pts = sorted(roi_pts, key=phase_angle, reverse=True)
        print("排序后的 ROI 顶点：", sorted_roi_pts)

        # 将 ROI 部分透视变换到 2100x2970 幅面（A4 长宽比）
        pts1 = np.float32(sorted_roi_pts)
        pts2 = np.float32([[2100, 0], [0, 0], [0, 2970], [2100, 2970]])
        M = cv2.getPerspectiveTransform(pts1, pts2)
        roi_img = cv2.warpPerspective(img, M, [2100, 2970])

        # Windows 平台下手动调整显示窗口大小；macOS 平台无需调整
        resWndTitle = wnd_title + " Result"
        if platform.system() == "Windows":
            cv2.namedWindow(resWndTitle, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(resWndTitle, wnd_width, wnd_height)
        cv2.imshow(resWndTitle, roi_img)

cv2.destroyAllWindows()
