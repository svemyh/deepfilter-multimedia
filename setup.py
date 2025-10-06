"""Setup configuration for deepfilter-multimedia."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="deepfilter-multimedia",
    version="0.1.0",
    author="Sveinung Myhre",
    author_email="",
    description="Noise reduction for audio and video files using DeepFilterNet",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/deepfilter-multimedia",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",
        "Topic :: Multimedia :: Video",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "deepfilternet>=0.5.0",
        "torch>=1.9.0",
        "torchaudio>=0.9.0",
    ],
    entry_points={
        "console_scripts": [
            "dfm=deepfilter_multimedia.cli:main",
        ],
    },
    keywords="audio video noise-reduction deepfilternet speech-enhancement",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/deepfilter-multimedia/issues",
        "Source": "https://github.com/yourusername/deepfilter-multimedia",
        "DeepFilterNet": "https://github.com/Rikorose/DeepFilterNet",
    },
)
