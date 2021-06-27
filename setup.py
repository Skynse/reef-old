from setuptools import setup, find_packages

version = "1.0.1"

with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")

setup(
    name="reef",
    packages=find_packages(),
    entry_points={"console_scripts": ["reef=reef.cli:main"]},
    version=version,
    description="Network Analysis tool.",
    long_description=long_descr,
    author="Skynse",
    include_package_data=True,
    author_email="prodbyskynse@gmail.com",
)
