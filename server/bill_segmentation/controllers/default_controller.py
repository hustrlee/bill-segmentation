import connexion
import six
from flask import url_for
from werkzeug.utils import secure_filename

from bill_segmentation.models.img_on_server_dto import ImgOnServerDto  # noqa: E501
from bill_segmentation.models.roi_pts_dto import RoiPtsDto  # noqa: E501
from bill_segmentation.models.version_dto import VersionDto  # noqa: E501
from bill_segmentation import util


def get_version():  # noqa: E501
    """获取 API 版本号

     # noqa: E501


    :rtype: VersionDto
    """
    return {"version": "bill-segmentation-v0.9.0"}


def upload_image(file=None):  # noqa: E501
    """上载文件

     # noqa: E501

    :param file: 
    :type file: str

    :rtype: ImgOnServerDto
    """

    # 检查上传文件的后缀名是否合法，并保存文件到 static 目录

    ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "bmp"}

    def allowed_file(filename):
        return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save("bill_segmentation/static/" + filename)
        return {"uploadImgUrl": url_for("static", filename=filename, _external=True),
                "uploadImgId": filename}
    return "不支持的图像格式。仅支持：.png、.jpg、.jpeg、.bmp 文件。", 400


def wrap_perspective(img_id, roi_pts_dto=None):  # noqa: E501
    """对指定图像进行透视矫正

     # noqa: E501

    :param img_id: 图像 ID
    :type img_id: str
    :param roi_pts_dto: 
    :type roi_pts_dto: dict | bytes

    :rtype: ImgOnServerDto
    """
    if connexion.request.is_json:
        roi_pts_dto = RoiPtsDto.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def wrap_segmentation(bill_type, img_id):  # noqa: E501
    """分割指定图像

     # noqa: E501

    :param bill_type: 票据类型 ID
    :type bill_type: str
    :param img_id: 图像 ID
    :type img_id: str

    :rtype: List[ImgOnServerDto]
    """
    return 'do some magic!'
