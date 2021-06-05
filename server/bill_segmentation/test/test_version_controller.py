# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from bill_segmentation.models.version_dto import VersionDto  # noqa: E501
from bill_segmentation.test import BaseTestCase


class TestVersionController(BaseTestCase):
    """VersionController integration test stubs"""

    def test_get_version(self):
        """Test case for get_version

        获取 API 版本号
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/bill-segmentation/version',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
