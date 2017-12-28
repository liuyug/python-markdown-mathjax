#!/usr/bin/env python
# -*- encoding:utf-8 -*-

from setuptools import setup


with open('README.rst') as f:
    long_description = f.read()


setup(
    name='MathJaxExtension',
    version='1.0',
    author='Yugang LIU',
    author_email='liuyug@gmail.com',
    url='https://github.com/liuyug/python-markdown-mathjax.git',
    license='MIT',
    description='MathJax extension for python-markdown',
    long_description=long_description,
    py_modules=['mdx_mathjax'],
    install_requires=['Markdown>=2.5'],
)