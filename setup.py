from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="moy-nalog-py",
    version="0.2.1",
    author="senylar",
    author_email="senyvlar@gmail.com",
    description="Python клиент для работы с API сервиса Мой налог",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/senylar/MoyNalogPy",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests",
        "pydantic"
    ],
)