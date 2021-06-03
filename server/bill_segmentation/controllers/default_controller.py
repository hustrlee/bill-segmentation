import connexion
import six

from bill_segmentation.models.version_dto import VersionDto  # noqa: E501
from bill_segmentation import util
from flask import url_for


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
    return url_for("static", filename="foo.jpeg", _external=True)
