import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="nosauth",
    version="0.1.1",
    description="Library that lets you obtain auth token so you can login to NosTale official servers",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/morsisko/NosTale-Auth",
    author="morsisko",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 5 - Production/Stable",
    ],
    packages=["nosauth"],
    install_requires=["requests"],
    package_data={"nosauth": ["cert.pem"]},
    include_package_data=True,
)
