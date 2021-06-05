import cv2
import numpy as np


def wrap_perspective_cv(img_id, roi_pts):

    # 读取图像
    img = cv2.imread("./bill_segmentation/static/" + img_id)

    # 将 roi_pts 转换成二维数组
    roi_pts_list = []
    for pt in roi_pts:
        roi_pts_list.append([pt.x, pt.y])

    # 将四边形的顶点按逆时针排序：（右上、左上，左下，右下）
    # 计算四边形的质心
    centroid = [0.0, 0.0]
    for i in range(0, 3):
        centroid[0] += roi_pts_list[i][0]
        centroid[1] += roi_pts_list[i][1]
    centroid[0] = centroid[0] / 4
    centroid[1] = centroid[1] / 4
    # print("ROI 质心：", centroid)

    # 通过比较各点到质心的角度进行排序
    def phase_angle(point):
        return cv2.fastAtan2(
            point[1] - centroid[1], point[0] - centroid[0])
    sorted_roi_pts = sorted(roi_pts_list, key=phase_angle, reverse=True)
    sorted_roi_pts = np.array(sorted_roi_pts)
    # print("排序后的 ROI 顶点：", sorted_roi_pts)

    # 如果高比宽要大，则旋转 90 度
    if np.linalg.norm(sorted_roi_pts[0] - sorted_roi_pts[1]) < np.linalg.norm(sorted_roi_pts[1] - sorted_roi_pts[2]):
        sorted_roi_pts = np.roll(np.array(sorted_roi_pts), 2)
        # print("旋转后的 ROI 顶点：", sorted_roi_pts)

    pts1 = np.float32(sorted_roi_pts)
    # pts2 = np.float32([[1640, 0], [0, 0], [0, 1000], [1640, 1000]])
    pts2 = np.float32([[1466, 192], [168, 192], [168, 898], [1466, 898]])
    M = cv2.getPerspectiveTransform(pts1, pts2)
    roi_img = cv2.warpPerspective(img, M, (1640, 1000))

    cv2.imwrite("./bill_segmentation/static/" +
                img_id + ".perspective.jpg", roi_img)

    return img_id + ".perspective.jpg"
