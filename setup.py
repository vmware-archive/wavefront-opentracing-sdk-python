#!/usr/bin/env python3
# coding: utf-8
"""Wavefront Python SDK.

This is a Wavefront Python SDK.
"""

import os

import setuptools

with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                       'README.md')) as fd:
    LONG_DESCRIPTION = fd.read()


setuptools.setup(
    name='wavefront-opentracing-sdk-python',
    version='2.1.0',
    author='Wavefront by VMware',
    author_email='chitimba@wavefront.com',
    url='https://github.com/wavefrontHQ/wavefront-opentracing-sdk-python',
    license='Apache-2.0',
    description='Wavefront Opentracing Python SDK',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    keywords=[
        'OpenTracing',
        'OpenTracing SDK',
        'Wavefront',
        'Wavefront SDK',
        ],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    include_package_data=True,
    packages=setuptools.find_packages(exclude=('*.tests', '*.tests.*',
                                               'tests.*', 'tests')),
    install_requires=[
        'opentracing>=2.0',
        'wavefront-pyformance>=1.0',
        'wavefront-sdk-python>=1.6',
        ],
    test_require=[
        'freezegun>=0.3.11',
        'mock>=2.0',
        ],
)
