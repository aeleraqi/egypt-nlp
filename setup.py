# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="egypt-nlp",
    version="2.0.0",
    author="Egypt NLP Team",
    author_email="contact@egypt-nlp.com",
    description="مكتبة Python لاستخراج الكيانات الجغرافية المصرية مع معالجة الأخطاء الكتابية",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/egypt-nlp",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Natural Language :: Arabic",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        # لا توجد متطلبات خارجية - المكتبة تستخدم المكتبات القياسية فقط
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
        ],
    },
    keywords=[
        "nlp",
        "arabic",
        "egypt",
        "ner",
        "named entity recognition",
        "geographic",
        "location extraction",
        "مصر",
        "عربي",
        "معالجة اللغة الطبيعية",
    ],
    project_urls={
        "Bug Reports": "https://github.com/yourusername/egypt-nlp/issues",
        "Source": "https://github.com/yourusername/egypt-nlp",
        "Documentation": "https://github.com/yourusername/egypt-nlp/blob/main/README.md",
    },
    include_package_data=True,
    zip_safe=False,
)
