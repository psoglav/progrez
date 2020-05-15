from setuptools import setup, find_packages

setup(
    name="progrez",
    version="0.1",
    packages=find_packages(),
    scripts=["./core/color.py", "./core/progrez.py", "./core/typewriter.py"],

    author="psoglav",
    author_email="psoglav.ih8u@gmail.com",
    description="The dynamic, async and beautiful progress bar.",
    keywords="progress bar loader async",
    url="https://github.com/psoglav/progrez",
    classifiers=[
        "License :: OSI Approved :: Python Software Foundation License"
    ]
)
