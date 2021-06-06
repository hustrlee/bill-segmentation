import os

import connexion
from flask.helpers import url_for
import six

from bill_segmentation.models.error_handle_dto import ErrorHandleDto  # noqa: E501
from bill_segmentation.models.img_on_server_dto import ImgOnServerDto  # noqa: E501
from bill_segmentation.models.roi_pts_dto import RoiPtsDto  # noqa: E501
from bill_segmentation import util

from bill_segmentation.image_api.util import get_img_filename
from bill_segmentation.bill_api.specification import get_perspective_param
from bill_segmentation.bill_api.specification import get_segmentation_param
from bill_segmentation.image_api.transform import warp_perspective_cv
from bill_segmentation.image_api.transform import warp_segmentation_cv


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
    filename = get_img_filename(img_id)
    if not filename:
        return ErrorHandleDto(message="要求矫正的图像不存在，请检查 imgId 是否正确"), 400

    # 读取票据的矫正参数
    perspective_param = get_perspective_param(bill_type_id)
    if not perspective_param:
        return ErrorHandleDto(message="不支持的票据类型，请检查 billTypeId 是否正确"), 400

    res = warp_perspective_cv(filename, perspective_param, roi_pts_dto.pts)

    # 模拟生成 img_id
    _, res_filename = os.path.split(res)
    res_img_id, _ = os.path.splitext(res_filename)

    return ImgOnServerDto(img_id=res_img_id, img_url=url_for("static", filename=res_filename, _external=True))


def warp_segmentation(bill_type_id, img_id):  # noqa: E501
    """分割指定图像

     # noqa: E501

    :param bill_type_id: 票据类型 ID，用于唯一确定一个票据类型
    :type bill_type_id: str
    :param img_id: 票据图像 ID，用于唯一确定一个图像
    :type img_id: str

    :rtype: List[ImgOnServerDto]
    """

    # 验证图片是否存在
    filename = get_img_filename(img_id)
    if not filename:
        return ErrorHandleDto(message="要求分割的图像不存在，请检查 imgId 是否正确"), 400

    # 读取票据的分割参数
    segmentation_param = get_segmentation_param(bill_type_id)
    if not segmentation_param:
        return ErrorHandleDto(message="不支持的票据类型，请检查 billTypeId 是否正确"), 400

    res = warp_segmentation_cv(filename, segmentation_param)

    # 生成发布 img_url
    for item in res:
        _, item_filename = os.path.split(item["img_url"])
        item["img_url"] = url_for(
            "static", filename=item_filename, _external=True)

    # # 模拟生成 img_id
    # for item in res:
    #     _, item_filename = os.path.split(item["img_url"])
    #     item_img_id, _ = os.path.splitext(item_filename)
    #     item["img_id"] = item_img_id

    return res
