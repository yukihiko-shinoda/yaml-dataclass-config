#!/usr/bin/env python
"""This module implements build settings."""

from setuptools import setup
from setuptools import find_packages


def main():
    """This function implements build settings."""
    with open('README.md', 'r', encoding='utf8') as file:
        readme = file.read()

    setup(
        name='yamldataclassconfig',
        version='1.2.0',
        description='This project helps you to import config file writen by YAML to Python data class.',
        long_description=readme,
        long_description_content_type='text/markdown',
        author='Yukihiko Shinoda',
        author_email='yuk.hik.future@gmail.com',
        packages=find_packages(exclude=("tests*", "myproduct*", "yourproduct*")),
        package_data={"yamldataclassconfig": ["py.typed"]},
        install_requires=[
            'dataclasses-json',
            'pyyaml',
            'Deprecated',
        ],
        url="https://github.com/yukihiko-shinoda/yaml-dataclass-config",
        keywords="yaml dataclass dataclasses config",
    )


if __name__ == '__main__':
    main()
