from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

version = '0.1.2'

setup(
    name = "xl2sitemap",
    packages = ["xl2sitemap"],
    entry_points = {
        "console_scripts": ['xl2sitemap = xl2sitemap.xl2sitemap:main']
        },
    version = version,
    description = "Generate heavy sitemap files using excel sheets",
    long_description = long_description,
    long_description_content_type='text/markdown',
    author = "Shahzeb Qureshi",
    author_email = "shahzeb_iam@outlook.com",
    url = "https://github.com/antiproblemist/excel-to-sitemap",
    include_package_data = True,
    package_data={
        '': ['LICENSE', 'README.md'],
    },
    install_requires=['pandas>=0.24.2', 'tqdm>=4.32.1', 'numpy>=1.16.3', 'xlrd>=1.2.0'],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        ],
    )