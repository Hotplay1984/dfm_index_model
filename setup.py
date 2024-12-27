from setuptools import setup, find_packages

setup(
    name="dfm_index_model",
    version="0.1.0",
    description="Dynamic Factor Model for Macroeconomic Index Construction",
    author="Weiyao Sun",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "pandas>=1.5.0",
        "numpy>=1.20.0",
        "statsmodels>=0.13.0",
        "tsalchemy @ git+https://github.com/Hotplay1984/tsalchemy.git",
        "wd @ git+https://github.com/Hotplay1984/wd.git",
    ],
) 