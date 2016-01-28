from setuptools import setup, find_packages

NAME = 'qsardb'
VERSION = '0.0.1dev'
AUTHOR = 'Rich Lewis'
AUTHOR_EMAIL = 'rl403@cam.ac.uk'
DESCRIPTION = 'Package for handling QSAR data'
LICENSE = 'MIT License'
KEYWORDS = 'cheminformatics, qsar, database'
URL = 'http://github.com/richlewis42/qsardb'
PACKAGES = find_packages(exclude=['tests'])
PACKAGE_DATA = {
    '': ['requirements.txt', 'LICENSE'],
    'qsar.data.chembl': ['queries/*.sql']
}

with open('README.md') as f:
    LONG_DESCRIPTION = f.read()

CLASSIFIERS = [
    "Development Status :: 3 - Alpha",
    "License :: OSI Aproved :: MIT License"
]

if __name__ == '__main__':
    setup(
        name=NAME,
        version=VERSION,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        description=DESCRIPTION,
        license=LICENSE,
        keywords=KEYWORDS,
        url=URL,
        packages=PACKAGES,
        long_description=LONG_DESCRIPTION,
        classifiers=CLASSIFIERS,
        package_data=PACKAGE_DATA,
        include_package_data=True
    )
