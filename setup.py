import setuptools

with open("README.md","r",encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="string-analysis-mkgloamglozer",
    version="0.0.8",
    author = "Mike Davies",
    author_email = "mikedaviespp@gmail.com",
    description="Program that conversts clustered string output into word clouds",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages = ['string_analysis'],
    include_package_data=True,
    install_requires = ['matplotlib', 'numpy', 'requests', 'goscripts', 'wordcloud'],
    python_requires =">=3.8"
)