# coding: utf-8

"""
    Wavefront Python SDK
    <p>This is a Wavefront Python SDK</p>  # noqa: E501
"""

from setuptools import setup, find_packages  # noqa: H301

NAME = "wavefront-opentracing-sdk-python"
VERSION = "1.0.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

install_requires = ['opentracing>=2', 'wavefront-sdk-python>=1.1',
                    'wavefront-pyformance>=0.9.4']

test_requires = ['mock>=2', 'freezegun>=0.3.11']

setup(
    name=NAME,
    version=VERSION,
    description="Wavefront Opentracing Python SDK",
    author_email="songhao@vmware.com",
    url="https://github.com/wavefrontHQ/wavefront-opentracing-sdk-python",
    keywords=["Wavefront SDK", "Wavefront", "OpenTracing"],
    install_requires=install_requires,
    test_require=test_requires,
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    long_description="""\
    """
)
