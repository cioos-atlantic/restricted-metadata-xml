import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="restricted-metadata-xml",
    version="1.0",
    description="Package for adding metadata on restricted keywords and EOVs to an xml/yml",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Jared McLellan",
    author_email="jared.mclellan@cioosatlantic.ca",
    url="https://github.com/cioos-siooc/restricted-metadata-xml",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: CC-BY 4.0",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
    ]
)