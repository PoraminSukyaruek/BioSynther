from setuptools import setup, find_packages

setup(
    name="biosynther",
    version="1.0.0",
    description="AI-Driven Synthetic Biology Platform for Designing Novel Biological Systems",
    author="mwasifanwar",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21.0",
        "tensorflow>=2.8.0",
        "scikit-learn>=1.0.0",
        "networkx>=2.6.0",
        "biopython>=1.79",
        "matplotlib>=3.5.0",
        "seaborn>=0.11.0",
    ],
    python_requires=">=3.8",
)