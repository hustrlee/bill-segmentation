import os

import connexion
from flask.json import JSONEncoder
import six
from flask import url_for, jsonify
from werkzeug.utils import secure_filename

from bill_segmentation.models.upload_respond_dto import UploadRespondDto  # noqa: E501
from bill_segmentation.models.version_dto import VersionDto  # noqa: E501
from bill_segmentation import util


def get_version():  # noqa: E501
    """获取 API 版本号

     # noqa: E501


    :rtype: VersionDto
    """
    return 'do some magic!'


def upload_post(file=None):  # noqa: E501
    """上载文件

     # noqa: E501

    :param file: 
    :type file: str

    :rtype: None
    """

    # 检查上传文件的后缀名是否合法，并保存文件到 static 目录

    ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "bmp"}

    def allowed_file(filename):
        return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save("bill_segmentation/static/" + filename)

    return jsonify(uploadImgUrl=url_for("static", filename=secure_filename(file.filename), _external=True), segmentationUrls=[])
