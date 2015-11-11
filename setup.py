import os
from setuptools import setup

setup(
    name = "deepx-website",
    version = "0.0.1",
    author = "Sharad Vikram and Zack Lipton",
    author_email = "sharad.vikram@gmail.com",
    description = "",
    license = "MIT",
    keywords = "",
    url = "",
    packages=[
        'deepx_web'
    ],
    entry_points={
        'console_scripts': [
            'start_server=deepx_web.main:main',
        ],
    },
    classifiers=[
    ],
)
