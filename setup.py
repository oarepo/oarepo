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

INVENIO_VERSION = '3.2.0'

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
    'pytest==5.2.1',
    'Flask==1.1.2',
])

setup_requires = [
    'pytest-runner>=3.0.0,<5',
]

install_requires = [
  'alembic==1.4.2',
  'amqp==2.6.0',
  'arrow==0.15.7',
  'atomicwrites==1.3.0',
  'attrs==19.3.0',
  'Babel==2.8.0',
  'backcall==0.2.0',
  'billiard==3.6.3.0',
  'bleach==3.1.5',
  'blinker==1.4',
  'celery==4.4.6',
  'certifi==2019.9.11',
  'click==7.1.2',
  'decorator==4.4.2',
  'elasticsearch==7.8.0',
  'elasticsearch-dsl==7.2.1',
  'Flask==1.1.2',
  'Flask-Admin==1.5.6',
  'Flask-Alembic==2.0.1',
  'Flask-Assets==2.0',
  'Flask-BabelEx==0.9.4',
  'Flask-Breadcrumbs==0.5.1',
  'Flask-Caching==1.9.0',
  'Flask-CeleryExt==0.3.4',
  'Flask-Collect==1.2.2',
  'Flask-Cors==3.0.8',
  'Flask-Limiter==1.1.0',
  'Flask-Login==0.4.1',
  'Flask-Mail==0.9.1',
  'Flask-Menu==0.7.2',
  'Flask-Principal==0.4.0',
  'flask-shell-ipython==0.4.1',
  'Flask-SQLAlchemy==2.4.4',
  'flask-talisman==0.5.0',
  'flask-webpackext==1.0.2',
  'future==0.18.2',
  'invenio==3.2.2',
  'invenio-admin==1.1.3',
  'invenio-app==1.2.6',
  'invenio-assets==1.1.5',
  'invenio-base==1.2.3',
  'invenio-cache==1.0.0',
  'invenio-celery==1.1.3',
  'invenio-config==1.0.3',
  'invenio-db==1.0.5',
  'invenio-formatter==1.0.3',
  'invenio-i18n==1.1.1',
  'invenio-logging==1.2.1',
  'invenio-mail==1.0.2',
  'invenio-rest==1.1.3',
  'invenio-search==1.2.4',
  'invenio-theme==1.1.4',
  'ipython==7.16.1',
  'ipython-genutils==0.2.0',
  'itsdangerous==1.1.0',
  'jedi==0.17.2',
  'Jinja2==2.11.2',
  'jsmin==2.2.2',
  'kombu==4.6.11',
  'limits==1.5.1',
  'Mako==1.1.3',
  'MarkupSafe==1.1.1',
  'marshmallow==3.7.1',
  'mock==3.0.5',
  'more-itertools==7.2.0',
  'msgpack==1.0.0',
  'node-semver==0.1.1',
  'nose==1.3.7',
  'numpy==1.17.2',
  'packaging==19.2',
  'parso==0.7.0',
  'pexpect==4.8.0',
  'pickleshare==0.7.5',
  'pipenv==2018.11.26',
  'pluggy==0.13.0',
  'prompt-toolkit==3.0.5',
  'psycopg2-binary==2.8.5',
  'ptyprocess==0.6.0',
  'py==1.9.0',
  'Pygments==2.6.1',
  'pynpm==0.1.2',
  'pyparsing==2.4.2',
#  'pytest==5.2.1',
  'python-dateutil==2.8.1',
  'python-editor==1.0.4',
  'pytz==2020.1',
  'pywebpack==1.1.0',
  'redis==3.5.3',
  'requirements-builder==0.4.2',
  'six==1.12.0',
  'speaklater==1.3',
  'SQLAlchemy==1.3.18',
  'SQLAlchemy-Continuum==1.3.11',
  'SQLAlchemy-Utils==0.35.0',
  'traitlets==4.3.3',
  'uritools==3.0.0',
  'urllib3==1.25.9',
  'vine==1.3.0',
  'virtualenv==16.7.5',
  'virtualenv-clone==0.5.3',
  'wcwidth==0.1.7',
  'webargs==5.5.3',
  'webassets==2.0',
  'webencodings==0.5.1',
  'Werkzeug==0.16.1',
  'WTForms==2.3.1',
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
