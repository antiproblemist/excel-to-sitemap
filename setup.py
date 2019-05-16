from setuptools import setup
  
version = '0.1.1'

setup(
    name = "xl2sitemap",
    packages = ["xl2sitemap"],
    entry_points = {
        "console_scripts": ['xl2sitemap = xl2sitemap.xl2sitemap:main']
        },
    version = version,
    description = "Generate heavy sitemap files using excel sheets",
    long_description = "Generate sitemap files with excel sheet as the input",
    author = "Shahzeb Qureshi",
    author_email = "shahzeb_iam@outlook.com",
    url = "https://github.com/antiproblemist/xl2sitemap",
    include_package_data = True,
    package_data={
        '': ['LICENSE'],
    },
    install_requires=['pandas>=0.24.2', 'tqdm>=4.32.1', 'tqdm>=4.32.1', 'numpy>=1.16.3', 'xlrd>=1.2.0'
],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        ],
    )