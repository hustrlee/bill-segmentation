import os

import cv2
import numpy as np


def warp_perspective_cv(filename, perspective_param, roi_pts):
    """执行透视矫正

    :param filename: 图像文件名
    :type filename: str
    :param perspective_param: 矫正参数
    :type perspective_param: dict
    :param roi_pts: 矫正源矩阵
    :type roi_pts: roi_pts_dto_pts

    :rtype: str
    """

    # 读取图像
    img = cv2.imread(filename)

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

    # 通过比较各点到质心的角度进行排序
    def phase_angle(point):
        return cv2.fastAtan2(point[1] - centroid[1], point[0] - centroid[0])

    sorted_roi_pts = np.array(
        sorted(roi_pts_list, key=phase_angle, reverse=True))

    # 如果顶点构成的 4 边形高度大于宽度，则逆时针旋转 90 度
    if np.linalg.norm(sorted_roi_pts[0] - sorted_roi_pts[1]) < np.linalg.norm(sorted_roi_pts[1] - sorted_roi_pts[2]):
        sorted_roi_pts = np.roll(np.array(sorted_roi_pts), 2)

    pts1 = np.float32(sorted_roi_pts)
    pts2 = np.float32(perspective_param["dst"])
    M = cv2.getPerspectiveTransform(pts1, pts2)
    roi_img = cv2.warpPerspective(img, M, perspective_param["dsize"])

    dst_filename = os.path.splitext(filename)[0] + ".perspective.jpg"
    cv2.imwrite(dst_filename, roi_img)

    # 返回矫正后的文件名（包含路径）
    return dst_filename


def warp_segmentation_cv(filename, segmentation_param):
    """执行图片分割

    :param filename: 图像文件名
    :type filename: str
    :param segmentation_param: 分割参数
    :type segmentation_param: dict

    :rtype: list
    """

    # 读取图像
    img = cv2.imread(filename)

    # 分离 filename，便于后面组合 seg_filename
    file_root, file_ext = os.path.splitext(filename)

    # segmentation_param 的第一个值是票据标准幅面尺寸，按此尺寸 resize 图像
    if not img.shape[0:2] == (segmentation_param[0]["rect"][3], segmentation_param[0]["rect"][2]):
        img = cv2.resize(img, segmentation_param[0]["rect"][2:])

    seg_files = []

    # 遍历 segmentation_param 的后续参数，切割图片，并保存
    for param in segmentation_param[1:]:
        left = param["rect"][0]
        right = left + param["rect"][2]
        top = param["rect"][1]
        bottom = top + param["rect"][3]
        seg_img = img[top:bottom, left:right]
        seg_filename = file_root + "." + param["name"] + "." + file_ext
        cv2.imwrite(seg_filename, seg_img)
        seg_files.append({"name": param["name"], "img_url": seg_filename})

    return seg_files
