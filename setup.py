"""
@Author: ziwenxie
@Date:   2017-03-04 20:00:30
"""

from setuptools import setup, find_packages

setup(
    name='netease-dl',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests>=2.10.0',
        'pycrypto>=2.6.1'
        'click>=5.1'
        'PrettyTable>=0.7.2'
    ],

    entry_points='''
        [console_scripts]
        netease-dl=netease.start:cli
    ''',

    license='MIT',
    author='ziwenxie',
    author_email='ziwenxiecat@gmail.com',
    url='https://github.com/ziwenxie/netease-dl',
    description='A command tool to download NetEase-Music\'s songs.',
    keywords=['music', 'netease', 'download', 'command tool'],
)
