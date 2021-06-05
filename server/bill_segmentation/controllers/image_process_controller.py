import os

import connexion
import six

from bill_segmentation.models.error_handle_dto import ErrorHandleDto  # noqa: E501
from bill_segmentation.models.img_on_server_dto import ImgOnServerDto  # noqa: E501
from bill_segmentation.models.roi_pts_dto import RoiPtsDto  # noqa: E501
from bill_segmentation import util

from bill_segmentation.bill_api.specification import get_perspective_param


def warp_perspective(bill_type_id, img_id, roi_pts_dto=None):  # noqa: E501
    """对图像进行透视矫正

     # noqa: E501

    :param bill_type_id: 票据类型 ID，用于唯一确定一个票据类型
    :type bill_type_id: str
    :param img_id: 票据图像 ID，用于唯一确定一个图像
    :type img_id: str
    :param roi_pts_dto: 
    :type roi_pts_dto: dict | bytes

    :rtype: ImgOnServerDto
    """
    if connexion.request.is_json:
        roi_pts_dto = RoiPtsDto.from_dict(connexion.request.get_json())  # noqa: E501

    # 验证图片是否存在

    # 读取票据的矫正点参数
    perspective_param = get_perspective_param(bill_type_id)
    if not perspective_param:
        return ErrorHandleDto(message="不支持的票据类型"), 400

    return 'do some magic!'


def warp_segmentation(bill_type_id, img_id):  # noqa: E501
    """分割指定图像

     # noqa: E501

    :param bill_type_id: 票据类型 ID，用于唯一确定一个票据类型
    :type bill_type_id: str
    :param img_id: 票据图像 ID，用于唯一确定一个图像
    :type img_id: str

    :rtype: List[ImgOnServerDto]
    """
    return 'do some magic!'
