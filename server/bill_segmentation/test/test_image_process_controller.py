# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from bill_segmentation.models.error_handle_dto import ErrorHandleDto  # noqa: E501
from bill_segmentation.models.img_on_server_dto import ImgOnServerDto  # noqa: E501
from bill_segmentation.models.roi_pts_dto import RoiPtsDto  # noqa: E501
from bill_segmentation.test import BaseTestCase


class TestImageProcessController(BaseTestCase):
    """ImageProcessController integration test stubs"""

    def test_warp_perspective(self):
        """Test case for warp_perspective

        对图像进行透视矫正
        """
        roi_pts_dto = {"pts":[{"x":0,"y":0},{"x":100,"y":0},{"x":100,"y":100},{"x":0,"y":100}]}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/bill-segmentation/warp-perspective/{bill_type_id}/{img_id}'.format(bill_type_id='bill_type_id_example', img_id='img_id_example'),
            method='POST',
            headers=headers,
            data=json.dumps(roi_pts_dto),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_warp_segmentation(self):
        """Test case for warp_segmentation

        分割指定图像
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/bill-segmentation/warp-segmentation/{bill_type_id}/{img_id}'.format(bill_type_id='bill_type_id_example', img_id='img_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
