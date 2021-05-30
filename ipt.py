import cv2
import platform
import numpy as np

if __name__ == "__main__":
    imgPath = "dut.jpg"
    wndTitle = "IPT Demo"

    # 读取图像
    img = cv2.imread(imgPath)

    # 读取图像大小 (height, width, depth)
    imgHeight, imgWidth, _ = img.shape
    print("原始图片大小：", imgWidth, imgHeight)

    cv2.namedWindow(wndTitle, cv2.WINDOW_NORMAL)

    # macOS 中 imshow() 会自动按照图像的原始比例显示；而 Windows 中需要手动调整显示窗口的大小；
    # 未测试 Linux 下的情况
    if platform.system() == "Windows":
        # 读取屏幕大小 (positionX, positionY, width, height)
        cv2.setWindowProperty(
            wndTitle, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        _, _, screenWidth, screenHeight = cv2.getWindowImageRect(wndTitle)
        print("屏幕分辨率：", screenWidth, screenHeight)

        # 按照图片比例设置显示窗口大小
        cv2.setWindowProperty(
            wndTitle, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
        wndHeight = screenHeight - 100
        wndWidth = int(imgWidth * wndHeight / imgHeight)
        print("调整后显示窗口大小：", wndWidth, wndHeight)
        cv2.resizeWindow(wndTitle, wndWidth, wndHeight)

    # 显示图像
    cv2.imshow(wndTitle, img)

    # 绘制 4 边形的 ROI 区域
    # 使用鼠标左键依次确定 4 个顶点；点第 5 下鼠标左键完成选取；鼠标右键取消上一个顶点

    roiPts = []  # 用于存放 4 个顶点

    def define_roi(event, x, y, flags, param):
        global roiPts

        def draw_roi():
            global roiPts, img
            imgMask = img.copy()  # 保留原始图像，在 imgMask 上绘制 ROI 区域

            # 绘制所有的点，及连线
            for i in range(len(roiPts)):
                cv2.circle(imgMask, roiPts[i], 12, (0, 0, 255), -1)
                if i > 0:
                    cv2.line(imgMask, roiPts[i-1], roiPts[i], (0, 0, 255), 2)
                    if i == 3:  # 最后一个顶点，需要增加起点到终点的连线
                        cv2.line(imgMask, roiPts[0], roiPts[i], (0, 0, 255), 2)
            cv2.imshow(wndTitle, imgMask)

        if event == cv2.EVENT_LBUTTONDOWN:
            if len(roiPts) < 4:  # 不足 4 个顶点，则将该点加入到顶点数组，并绘制 ROI 区域
                roiPts.append([x, y])
                draw_roi()

        if event == cv2.EVENT_RBUTTONDOWN:
            if len(roiPts) > 0:  # 至少有 1 个顶点，则删除最后一个顶点，并绘制 ROI 区域
                roiPts.pop()
                draw_roi()

    # 监控鼠标事件，定义 ROI 区域
    cv2.setMouseCallback(wndTitle, define_roi)

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
            print("ROI 顶点：", roiPts)
            # 计算四边形的质心
            centroid = [0.0, 0.0]
            for i in range(0, 3):
                centroid[0] += roiPts[i][0]
                centroid[1] += roiPts[i][1]
            centroid[0] = centroid[0] / 4
            centroid[1] = centroid[1] / 4
            print("ROI 质心：", centroid)

            # 通过比较各点到质心的角度进行排序
            def phase_angle(point):
                return cv2.fastAtan2(
                    point[1] - centroid[1], point[0] - centroid[0])
            sorted_roi_pts = sorted(roiPts, key=phase_angle, reverse=True)
            print("排序后的 ROI 顶点：", sorted_roi_pts)

            # 将 ROI 部分透视变换到 2100x2970 幅面（A4 长宽比）
            pts1 = np.float32(sorted_roi_pts)
            pts2 = np.float32([[2100, 0], [0, 0], [0, 2970], [2100, 2970]])
            M = cv2.getPerspectiveTransform(pts1, pts2)
            roi_img = cv2.warpPerspective(img, M, [2100, 2970])
            cv2.imshow(wndTitle + " Result", roi_img)

    cv2.destroyAllWindows()
