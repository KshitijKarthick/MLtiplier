#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name="ml_worker",
    description='ML Worker',
    author="Kshitij Karthick",
    author_email="kshitij.karthick@gmail.com",
    packages=find_packages(),
    data_files=[(".", ["requirements.txt"])],
)
