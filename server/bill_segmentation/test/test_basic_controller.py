# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from bill_segmentation.models.error_handle_dto import ErrorHandleDto  # noqa: E501
from bill_segmentation.models.img_on_server_dto import ImgOnServerDto  # noqa: E501
from bill_segmentation.test import BaseTestCase


class TestBasicController(BaseTestCase):
    """BasicController integration test stubs"""

    @unittest.skip("multipart/form-data not supported by Connexion")
    def test_upload_image(self):
        """Test case for upload_image

        上载票据图像
        """
        headers = { 
            'Accept': 'application/json',
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
