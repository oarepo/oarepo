# -*- coding: utf-8 -*-
#
# This file is part of OArepo.
# Copyright (C) 2020 CESNET.
#
# OArepo is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""CESNET, UCT Prague and NTK wrapper around Invenio v3."""

import os

from setuptools import find_packages, setup

readme = open('README.md').read()

INVENIO_VERSION = '3.2.1'

extras_require = {
    'deploy': [
        'Flask-CeleryExt>=0.3.4',
        'marshmallow~=3.0',
        'invenio[base,auth,metadata,postgresql,elasticsearch6]~={0}'.format(INVENIO_VERSION),
        'invenio-oarepo~=1.1',
        'invenio-oarepo-ui~=1.0',
        'oarepo-micro-api>=1.0.0'
    ],
    'deploy-es7': [
        'Flask-CeleryExt>=0.3.4',
        'marshmallow~=3.0',
        'invenio[base,auth,metadata,postgresql,elasticsearch7]~={0}'.format(INVENIO_VERSION),
        'invenio-oarepo~=1.1',
        'invenio-oarepo-ui>=1.0.0',
        'oarepo-micro-api>=1.0.0'
    ],
    'heartbeat': [
        'oarepo-heartbeat>=1.0.0',
        'oarepo-heartbeat-common>=1.0.0',
    ],
    'openid': [
        'invenio-openid-connect>=1.1.0',
    ],
    'multisum': [
        'invenio-files-multisum-storage>=1.0.0,<1.1.0',
        'invenio-oarepo-files-rest>=1.0.0',
    ],
    'micro-api': [
        'oarepo-micro-api>=1.0.0'
    ],
    'files': [
        'invenio-files-rest>=1.0.0,<1.1.0',
        'invenio-records-files>=1.1.0,<=1.2.1'
    ],
    'acls': [
        'invenio-explicit-acls>=4.4.0',
    ],
    'links': [
        'invenio-records-links>=1.0.0',
    ],
    'models': [
        'marshmallow~=3.0',
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
    'draft': [
        'oarepo-invenio-records-draft~=4.0'
    ],
    'iiif': [
        'invenio-iiif>=1.0.0,<1.1.0'
    ],
    'references': [
        'oarepo-references~=1.4.0'
    ]
}


def add_tests(extra_test_reqs):
    def transform_req(req):
        if req.startswith('invenio['):
            req = 'invenio[tests,' + req[len('invenio['):]
        return req

    for r, _packages in list(extras_require.items()):
        if not r.startswith('deploy'):
            continue
        suffix = r[6:]
        tests = [
            transform_req(k) for k in _packages
        ]
        tests.extend(extra_test_reqs)
        extras_require['tests' + suffix] = tests


add_tests([
    'check-manifest~=0.25',
    'isort~=4.3',
    'Sphinx>=1.5.1',
])

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
    long_description_content_type='text/markdown',
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
    tests_require=extras_require['tests'],
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
