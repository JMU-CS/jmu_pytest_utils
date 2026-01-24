"""Setup script for jmu_pytest_utils."""

from setuptools import setup, find_packages

setup(
    name="jmu_pytest_utils",
    version="1.7.2",
    description="pytest plugin for Gradescope autograders",
    author="Chris Mayfield",
    author_email="mayfiecs@jmu.edu",
    url="https://github.com/JMU-CS/jmu_pytest_utils",
    packages=find_packages(),
    classifiers=[
        "Framework :: Pytest",
    ],
    license="MIT",
    package_data={"jmu_pytest_utils": ["template/*"]},
    install_requires=[
        "darglint",
        "flake8-docstrings",
        "pep8-naming",
        "pytest-cov",
        "pytest-timeout",
        "pytz",
        "ruff",
    ],
    entry_points={
        "console_scripts": [
            "jmu_pytest_utils = jmu_pytest_utils.builder:main",
        ],
        "pytest11": [
            "jmu_pytest_utils = jmu_pytest_utils.plugin",
        ],
    },
    python_requires=">=3.10",
)
