# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


def _setup():
    setup(
        name='squirrel',
        version='0.0.1',
        description='active users data manager',
        author='Jinliu Liu',
        author_email='liujinliu@lbesec.com',
        url='',
        install_requires=['tornado', 'boto3', 'futures',
                          'MySQL-python'],
        packages=find_packages('src'),
        package_dir={'': 'src'},
        entry_points={
            'console_scripts': [
                'squirrel-start=squirrel.main:main',
                ]
            },
        classifiers=[
            'Development Status :: 4 - Beta Development Status',
            'Environment :: Console',
            'Topic :: Utilities',
        ],
    )


def main():
    _setup()


if __name__ == '__main__':
    main()
