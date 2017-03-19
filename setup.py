# -*- coding: utf-8 -*-

"""
@Author: ziwenxie
@Date:   2017-03-04 20:00:30
"""
from setuptools import setup, find_packages


setup(
    name='netease-dl',
    version='1.0.2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests>=2.10.0',
        'pycrypto>=2.6.1',
        'click>=5.1',
        'PrettyTable>=0.7.2',
    ],

    entry_points='''
        [console_scripts]
        netease-dl=netease.start:cli
    ''',

    license='MIT',
    author='ziwenxie',
    author_email='ziwenxiecat@gmail.com',
    url='https://github.com/ziwenxie/netease-dl',
    description='一个基于命令行的网易云音乐下载器',
    keywords=['music', 'netease', 'download', 'command tool'],
)
