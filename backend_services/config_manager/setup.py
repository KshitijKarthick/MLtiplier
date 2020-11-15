#!/usr/bin/env python
import inspect
import os

from setuptools import find_packages, setup

__location__ = os.path.join(
    os.getcwd(), os.path.dirname(inspect.getfile(inspect.currentframe()))
)


def get_install_requirements(path):
    content = open(os.path.join(__location__, path)).read()
    requires = [req for req in content.split("\\n") if req != ""]
    return requires


setup(
    name="config_manager",
    description="Config Manager",
    author="Kshitij Karthick",
    author_email="kshitij.karthick@gmail.com",
    packages=find_packages(),
    data_files=[(".", ["requirements.txt"])],
    install_requires=get_install_requirements("requirements.txt"),
)
