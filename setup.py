import setuptools

with open("README.md","r") as fd:
    long_description = fd.read()

with open("requirements.txt","r") as fh:
    requirements = fh.read().splitlines()

setuptools.setup(
    name="rssh",
    version="1.1",
    author="Arthur Oliveira",
    author_email="fantasmahacking7@gmail.com",
    description="A SSH(Secure Shell) server/client library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ReddyyZ/rssh",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)