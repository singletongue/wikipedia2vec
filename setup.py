# -*- coding: utf-8 -*-
# License: Apache License 2.0
import numpy
from Cython.Build import cythonize
from setuptools import setup, find_packages


setup(
    name='wikipedia2vec',
    version='1.0.5',
    description='A tool for learning vector representations of words and entities from Wikipedia',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Studio Ousia',
    author_email='ikuya@ousia.jp',
    url='http://wikipedia2vec.github.io/',
    packages=find_packages(exclude=('tests*',)),
    ext_modules=cythonize(
        [
            "wikipedia2vec/*.pyx",
            "wikipedia2vec/utils/*.pyx",
            "wikipedia2vec/utils/tokenizer/*.pyx",
            "wikipedia2vec/utils/sentence_detector/*.pyx",
        ],
        language='c++',
    ),
    include_dirs=[numpy.get_include()],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'wikipedia2vec=wikipedia2vec.cli:cli',
        ]
    },
    keywords=['wikipedia', 'embedding', 'wikipedia2vec'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'click',
        'jieba',
        'joblib',
        'lmdb',
        'marisa-trie',
        'mwparserfromhell',
        'numpy',
        'scipy',
        'six',
        'tqdm',
    ],
    setup_requires=['numpy'],
    tests_require=['nose'],
    test_suite='nose.collector',
)
