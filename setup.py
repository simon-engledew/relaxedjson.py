from setuptools import setup, find_packages

setup(
    name="relaxedjson",
    version="1.0.0",
    author="Simon Engledew",
    author_email="simon.engledew@gmail.com",
    description=(
        "A relaxed JSON parser that accepts keys without double quotes."
    ),
    url="http://github.com/simon-engledew/relaxedjson",
    install_requires=['parsec'],
    license="MIT",
    keywords="relaxed json parser combinator parsec",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)