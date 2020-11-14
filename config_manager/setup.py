#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name="config_manager",
    description='Config Manager',
    author="Kshitij Karthick",
    author_email="kshitij.karthick@gmail.com",
    packages=find_packages(),
    data_files=[(".", ["requirements.txt"])],
)
