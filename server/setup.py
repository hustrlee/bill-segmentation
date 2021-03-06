# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "bill_segmentation"
VERSION = "0.1.0"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "connexion>=2.0.2",
    "swagger-ui-bundle>=0.0.2",
    "python_dateutil>=2.6.0"
]

setup(
    name=NAME,
    version=VERSION,
    description="票据分割 API",
    author_email="",
    url="",
    keywords=["OpenAPI", "票据分割 API"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['openapi/openapi.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['bill_segmentation=bill_segmentation.__main__:main']},
    long_description="""\
    按照票据模版，归一化并自动分割医疗票据
    """
)
