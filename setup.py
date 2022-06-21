from os import name
from setuptools import setup, find_packages
import pathlib

#home directory
HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
name="logio",
    version="1.0.0",
    description="Logio is an Unsupervised Machine learning framework for well log visualization, and well-well depth correlation using logs.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/aifenaike/Logio",
    author=['Ifenaike Alexander', 'Awojinrin Gbenga',"Ayodabo Tomisin", 'Ikpabi Prince', 'Omotosho Temitope', 'Adeyemi Abdullateef']
    author_email=["alexander.ifenaike@gmail.com"],
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Oprerating System :: OS Independent",
    ],
    packages = ["logio"],
    include_package_data=True,
    install_requires=["pandas","seaborn",
                     "matplotlib","lasio",
                     "openpyxl","scipy",
                     "numpy","numba","networkx"])
