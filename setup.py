#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup
from setuptools import find_packages


with open('README.md', 'r', encoding='utf8') as f:
    readme = f.read()


def main():
    setup(
        name='yamldataclassconfig',
        version='0.0a1',
        description='This project helps you to import config file writen by YAML to Python data class.',
        long_description=readme,
        long_description_content_type='text/markdown',
        author='Yukihiko Shinoda',
        author_email='yuk.hik.future@gmail.com',
        packages=find_packages(exclude=("tests*",)),
        install_requires=[
            'dataclasses-json',
            'pyyaml',
        ],
        url="https://github.com/yukihiko-shinoda/yaml-dataclass-config",
        keywords="yaml dataclass config",
    )


if __name__ == '__main__':
    main()
