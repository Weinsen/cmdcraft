#!/usr/bin/env python3
"""Setup cmdcraft library."""

import os
import re

from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), "README.rst")) as f:
    """Extract version from README.rst."""
    long_description = f.read()


def get_version(package):
    """Return package version as listed in `__version__` in `__init__.py`."""
    path = os.path.join(os.path.dirname(__file__), "src", package, "__init__.py")
    with open(path, "rb") as f:
        init_py = f.read().decode("utf-8")
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


setup(
    name="cmdcraft",
    author="A. M. Weinsen Jr.",
    version=get_version("cmdcraft"),
    url="https://github.com/weinsen/cmdcraft",
    description="",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={"cmdcraft": ["py.typed"]},
    install_requires=["prompt_toolkit"],
    python_requires=">=3.8.0",
    extras_require={
        "dev": ["ruff", "pytest"],
    },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python",
        "Topic :: Software Development",
    ],
)
