from setuptools import setup, find_packages

setup(
    name='mkdocs-pagelist-plugin',
    version='0.2.1',
    description='A MkDocs plugin to list pages based on tags and folders',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords='mkdocs python markdown pagelist',
    url='https://github.com/alanpt/mkdocs-pagelist-plugin', 
    author='Alan Proctor-Thomson',
    author_email='alanpt@gmail.com',
    license='MIT',
    install_requires=[
        'mkdocs>=1.0'
    ],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'mkdocs.plugins': [
            'pagelist = mkdocs_pagelist_plugin:PageListPlugin'
        ]
    }
)
