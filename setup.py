from setuptools import setup, find_packages

setup(
    name="relaxedjson",
    version="1.0.1",
    author="Simon Engledew",
    author_email="simon.engledew@gmail.com",
    description=(
        "A relaxed JSON parser that accepts keys without double quotes."
    ),
    extras_require={
        'tests': [
            'nose'
        ]
    },
    url="http://github.com/simon-engledew/relaxedjson",
    install_requires=['parsec'],
    license="MIT",
    keywords=[
        "relaxed json",
        "relaxed",
        "json",
        "parser",
        "javascript",
        "combinator",
        "parsec",
    ],
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)