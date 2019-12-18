# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio Digital Library Framework."""

import os

from setuptools import find_packages, setup

readme = open('README.rst').read()

INVENIO_VERSION = '3.2.0a9'

tests_require = [
    'check-manifest>=0.25',
    'invenio[tests]~={0}'.format(INVENIO_VERSION)
]

extras_require = {
    'deploy': [
        'flask-celeryext==0.3.1',       # required as a workaround
        'invenio[base,auth,metadata,postgresql,elasticsearch6]~={0}'.format(INVENIO_VERSION),
        'invenio-oarepo~=1.1',
        'invenio-oarepo-ui~=1.0',
    ],
    'deploy-es7': [
        'flask-celeryext==0.3.1',       # required as a workaround
        'invenio[base,auth,metadata,postgresql,elasticsearch7]~={0}'.format(INVENIO_VERSION),
        'invenio-oarepo~=1.1',
        'invenio-oarepo-ui>=1.0.0',
    ],
    'openid': [
        'invenio-openid-connect>=1.0.0,<1.1.0',
    ],
    'multisum': [
        'invenio-files-multisum-storage>=1.0.0,<1.1.0',
        'invenio-oarepo-files-rest>=1.0.0',
    ],
    'files': [
        'invenio-files-rest>=1.0.0,<1.1.0',
        'invenio-records-files>=1.1.0,<1.2.0'
    ],
    'acls': [
        'invenio-explicit-acls>=4.4.0',
    ],
    'links': [
        'invenio-records-links>=1.0.0',
    ],
    'models': [
        'invenio-oarepo-dc>=1.1.0',
        'invenio-oarepo-invenio-model>=1.1.0',
        'invenio-oarepo-multilingual>=1.0.0',
    ],
    'includes': [
        'invenio-oarepo-mapping-includes>=1.1.0',
    ],
    'taxonomies': [
        'flask-taxonomies>=6.2.1'
    ],
    'tests': [
        'invenio[tests]~={0}'.format(INVENIO_VERSION),
        'check-manifest~=0.25',
        'isort~=4.3',
    ],
    'draft': [
        'oarepo-invenio-records-draft>=1.2.2,<2.0.0'
    ],
    'iiif': [
        'invenio-iiif>=1.0.0,<1.1.0'
    ]
}

setup_requires = [
    'pytest-runner>=3.0.0,<5',
]

install_requires = [
]

packages = find_packages()

# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('oarepo', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

split_version = version.split('.')
iversion = '.'.join(split_version[:3])

if 'a' in split_version[-1]:
    iversion = iversion + 'a' + split_version[-1].split('a')[1]
elif 'b' in split_version[-1]:
    iversion = iversion + 'b' + split_version[-1].split('a')[1]

assert iversion == INVENIO_VERSION

setup(
    name='oarepo',
    version=version,
    description=__doc__,
    long_description=readme,
    keywords='oarepo invenio',
    license='MIT',
    author='UCT Prague, CESNET z.s.p.o., NTK',
    author_email='miroslav.simek@vscht.cz',
    url='https://github.com/oarepo/oarepo',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={},
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 5 - Production/Stable',
    ],
)
