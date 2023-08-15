from setuptools import setup, find_packages

setup(
    name="tokflow",
    version="1.3.1",
    author="Tom Misawa",
    author_email="riversun.org@gmail.com",
    description="LLM utility of streaming token realtime replacement processing",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/riversun/TokFlow",
    packages=find_packages(exclude=["tests.*", "tests", "examples.*", "examples"]),
    tests_require=["pytest"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    license="GPLv3 or Commercial",
    python_requires=">=3.8",
    install_requires=[
    ]
)
