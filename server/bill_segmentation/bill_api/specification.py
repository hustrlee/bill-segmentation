def get_perspective_param(bill_type_id):
    """查找 bill_type_id 对应票据的矫正参数

    :param bill_type_id: 票据类型 ID
    :type img_id: str

    :rtype: dict
    """

    # 模拟返回 bill_type_id = "sh-invoice" 对应的矫正参数
    # 矫正参数 dsize: 矫正后图像的大小，(width, height)
    # 矫正参数 dst: 矫正目标矩阵，[右上角, 左上角, 左下角, 右下角]

    if bill_type_id == "sh-invoice":
        return {"dsize": (1640, 1000), "dst": [[1466, 192], [168, 192], [168, 898], [1466, 898]]}

    return None
