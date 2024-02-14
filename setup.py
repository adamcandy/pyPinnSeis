#!/usr/bin/env python3

import setuptools

with open("Readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pinnseis",
    version="0.0.1",
    author="Adam Candy",
    author_email="adam@candylab.org",
    description="Project created with the boilerplate machine, for pyPinnSeis.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://candylab.org",
    license="LGPLv3",
    packages=setuptools.find_packages(),
    scripts=["bin/pinnseis"],
    include_package_data=True,
    install_requires=[
        'numpy',
        'scipy',
        'matplotlib',
        'tensorflow',
        'SALib'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
