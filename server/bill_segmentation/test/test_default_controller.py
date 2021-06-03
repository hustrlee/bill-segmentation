# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from bill_segmentation.models.version_dto import VersionDto  # noqa: E501
from bill_segmentation.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

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

    @unittest.skip("multipart/form-data not supported by Connexion")
    def test_upload_post(self):
        """Test case for upload_post

        上载文件
        """
        headers = { 
            'Content-Type': 'multipart/form-data',
        }
        data = dict(file='/path/to/file')
        response = self.client.open(
            '/bill-segmentation/upload',
            method='POST',
            headers=headers,
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
