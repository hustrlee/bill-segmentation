import connexion
import six

from bill_segmentation.models.version_dto import VersionDto  # noqa: E501
from bill_segmentation import util


def get_version():  # noqa: E501
    """获取 API 版本号

     # noqa: E501


    :rtype: VersionDto
    """
    return {"version": "bill-segmentation-v0.9.0"}
