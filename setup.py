import setuptools

import doi_mgmt as meta

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name=meta.__title__,
    version=meta.__version__,
    author=meta.__author__,
    author_email=meta.__author_email__,
    description=meta.__description__,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/pypa/sampleproject',
    license=meta.__license__,
    project_urls={
        'Bug Tracker': 'https://github.com/pypa/sampleproject/issues',
    },
    install_requires=[
        'pydantic>=1.8.1,<1.9',
        'pyhumps>=1.6.1,<1.7'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)
