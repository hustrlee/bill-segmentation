import os


def get_img_filename(img_id):
    """查找 img_id 对应的图像文件

    :param img_id: 图像 ID
    :type img_id: str

    :rtype: str
    """

    # 模拟查找图像文件，规则是：filename = <img_id>.jpg
    filename = "bill_segmentation/static/" + img_id + ".jpg"
    if os.path.exists(filename):
        return filename

    return None
