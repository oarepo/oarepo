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

extras_require = {
    'tests': [
        'alembic==1.8.1',
        'amqp==5.1.1',
        'aniso8601==9.0.1',
        'appdirs==1.4.4',
        'appnope==0.1.3',
        'arrow==1.2.3',
        'asttokens==2.1.0',
        'async-timeout==4.0.2',
        'atomicwrites==1.4.1',
        'attrs==22.1.0',
        'babel==2.11.0',
        'babel-edtf==1.0.0',
        'backcall==0.2.0',
        'base32-lib==1.0.2',
        'beautifulsoup4==4.11.1',
        'billiard==3.6.4.0',
        'bleach==5.0.1',
        'blinker==1.5',
        'boto3==1.26.8',
        'botocore==1.29.8',
        'build==0.9.0',
        'cachelib==0.9.0',
        'cchardet==2.1.7',
        'celery==5.1.2',
        'certifi==2022.9.24',
        'cffi==1.15.1',
        'charset-normalizer==2.1.1',
        'check-manifest==0.48',
        'click==7.1.2',
        'click-default-group==1.2.2',
        'click-didyoumean==0.3.0',
        'click-plugins==1.1.1',
        'click-repl==0.2.0',
        'colorama==0.4.6',
        'coverage==5.5',
        'cryptography==38.0.3',
        'decorator==5.1.1',
        'defusedxml==0.7.1',
        'deprecated==1.2.13',
        'dnspython==2.2.1',
        'docker-services-cli==0.4.2',
        'dojson==1.4.0',
        'edtf==4.0.1',
        'elasticsearch==7.13.4',
        'elasticsearch-dsl==7.4.0',
        'email-validator==1.3.0',
        'entrypoints==0.4',
        'executing==1.2.0',
        'fastjsonschema==2.16.2',
        'flask==1.1.4',
        'flask-admin==1.6.0',
        'flask-alembic==2.0.1',
        'flask-babelex==0.9.4',
        'flask-breadcrumbs==0.5.1',
        'flask-caching==2.0.1',
        'flask-celeryext==0.4.3',
        'flask-collect-invenio==1.4.0',
        'flask-cors==3.0.10',
        'flask-iiif==0.6.3',
        'flask-kvsession-invenio==0.6.3',
        'flask-limiter==1.1.0',
        'flask-login==0.4.1',
        'flask-mail==0.9.1',
        'flask-menu==0.7.2',
        'flask-oauthlib==0.9.6',
        'flask-principal==0.4.0',
        'flask-resources==0.8.4',
        'flask-restful==0.3.9',
        'flask-security==3.0.0',
        'flask-shell-ipython==0.4.1',
        'flask-sqlalchemy==2.5.1',
        'flask-talisman==0.8.1',
        'flask-webpackext==1.0.2',
        'flask-wtf==0.15.1',
        'fs==2.4.16',
        'ftfy==6.1.1',
        'future==0.18.2',
        'geojson==2.5.0',
        'idna==3.4',
        'idutils==1.1.13',
        'importlib-metadata==4.13.0',
        'importlib-resources==5.10.0',
        'infinity==1.5',
        'iniconfig==1.1.1',
        'intervals==0.9.2',
        'invenio==3.5.0a4',
        'invenio-access==1.4.2',
        'invenio-accounts==1.4.11',
        'invenio-admin==1.3.2',
        'invenio-app==1.3.4',
        'invenio-assets==1.2.7',
        'invenio-base==1.2.13',
        'invenio-cache==1.1.1',
        'invenio-celery==1.2.5',
        'invenio-config==1.0.3',
        'invenio-db==1.0.14',
        'invenio-files-rest==1.3.3',
        'invenio-formatter==1.1.3',
        'invenio-i18n==1.3.2',
        'invenio-iiif==1.2.0',
        'invenio-indexer==1.2.7',
        'invenio-jsonschemas==1.1.4',
        'invenio-logging==1.3.2',
        'invenio-mail==1.0.2',
        'invenio-oaiserver==1.4.2',
        'invenio-oauth2server==1.3.7',
        'invenio-oauthclient==1.5.4',
        'invenio-pidstore==1.2.3',
        'invenio-previewer==1.3.7',
        'invenio-records==1.6.1',
        'invenio-records-files==1.2.1',
        'invenio-records-permissions==0.13.2',
        'invenio-records-resources==0.19.4',
        'invenio-records-rest==1.9.0',
        'invenio-records-ui==1.2.0',
        'invenio-rest==1.2.8',
        'invenio-search==1.4.2',
        'invenio-search-ui==2.0.11',
        'invenio-theme==1.3.31',
        'ipython==8.6.0',
        'isbnlib==3.10.12',
        'isort==5.10.1',
        'itsdangerous==1.1.0',
        'jedi==0.18.1',
        'jinja2==2.11.3',
        'jmespath==1.0.1',
        'jsmin==3.0.1',
        'jsonpatch==1.32',
        'jsonpointer==2.3',
        'jsonref==1.0.1',
        'jsonresolver==0.3.2',
        'jsonschema==3.2.0',
        'jupyter-client==7.4.5',
        'jupyter-core==5.0.0',
        'jupyterlab-pygments==0.2.2',
        'kombu==5.2.4',
        'limits==1.6',
        'luqum==0.12.0',
        'lxml==4.9.1',
        'mako==1.2.3',
        'markupsafe==2.0.1',
        'marshmallow==3.19.0',
        'marshmallow-oneofschema==3.0.1',
        'marshmallow-utils==0.5.7',
        'matplotlib-inline==0.1.6',
        'maxminddb==2.2.0',
        'maxminddb-geolite2==2018.703',
        'mistune==0.8.4',
        'msgpack==1.0.4',
        'nbclient==0.5.13',
        'nbconvert==6.4.5',
        'nbformat==5.7.0',
        'nest-asyncio==1.5.6',
        'node-semver==0.1.1',
        'oauthlib==2.1.0',
        'packaging==21.3',
        'pandocfilters==1.5.0',
        'parso==0.8.3',
        'passlib==1.7.4',
        'pep517==0.13.0',
        'pexpect==4.8.0',
        'pickleshare==0.7.5',
        'pillow==9.3.0',
        'platformdirs==2.5.3',
        'pluggy==0.13.1',
        'ply==3.11',
        'prompt-toolkit==3.0.32',
        'psycopg2-binary==2.9.5',
        'ptyprocess==0.7.0',
        'pure-eval==0.2.2',
        'py==1.11.0',
        'pycodestyle==2.9.1',
        'pycountry==22.3.5',
        'pycparser==2.21',
        'pydocstyle==6.1.1',
        'pygments==2.13.0',
        'pyjwt==2.6.0',
        'pynpm==0.1.2',
        'pyparsing==3.0.9',
        'pyrsistent==0.19.2',
        'pytest==6.2.5',
        'pytest-cov==4.0.0',
        'pytest-flask==1.2.0',
        'pytest-invenio[docs]==1.4.15',
        'pytest-isort==3.1.0',
        'pytest-pycodestyle==2.2.1',
        'pytest-pydocstyle==2.2.1',
        'python-dateutil==2.8.2',
        'pytz==2022.6',
        'pywebpack==1.2.0',
        'pyzmq==24.0.1',
        'redis==4.3.4',
        'requests==2.28.1',
        'requests-oauthlib==1.1.0',
        's3-client-lib==0.1.9.post1',
        's3transfer==0.6.0',
        'selenium==3.141.0',
        'sentry-sdk==1.10.1',
        'setuptools==65.5.1',
        'simplejson==3.17.6',
        'simplekv==0.14.1',
        'six==1.16.0',
        'snowballstemmer==2.2.0',
        'soupsieve==2.3.2.post1',
        'speaklater==1.3',
        'sqlalchemy==1.3.24',
        'sqlalchemy-continuum==1.3.13',
        'sqlalchemy-utils==0.38.3',
        'stack-data==0.6.0',
        'testpath==0.6.0',
        'toml==0.10.2',
        'tomli==2.0.1',
        'tornado==6.2',
        'traitlets==5.5.0',
        'ua-parser==0.16.1',
        'uritemplate==4.1.1',
        'uritools==4.0.0',
        'urllib3==1.26.12',
        'validators==0.20.0',
        'vine==5.0.0',
        'wand==0.6.10',
        'wcwidth==0.2.5',
        'webargs==5.5.3',
        'webencodings==0.5.1',
        'werkzeug==1.0.1',
        'wrapt==1.14.1',
        'wtforms==2.3.3',
        'wtforms-alchemy==0.18.0',
        'wtforms-components==0.10.5',
        'xmltodict==0.12.0',
        'zipp==3.10.0',
    ]
}

setup_requires = [
    'pytest-runner>=3.0.0,<5',
]

install_requires = [
    'alembic==1.8.1',
    'amqp==5.1.1',
    'aniso8601==9.0.1',
    'appdirs==1.4.4',
    'appnope==0.1.3',
    'arrow==1.2.3',
    'asttokens==2.1.0',
    'async-timeout==4.0.2',
    'attrs==22.1.0',
    'babel==2.11.0',
    'babel-edtf==1.0.0',
    'backcall==0.2.0',
    'base32-lib==1.0.2',
    'beautifulsoup4==4.11.1',
    'billiard==3.6.4.0',
    'bleach==5.0.1',
    'blinker==1.5',
    'boto3==1.26.8',
    'botocore==1.29.8',
    'cachelib==0.9.0',
    'cchardet==2.1.7',
    'celery==5.1.2',
    'certifi==2022.9.24',
    'cffi==1.15.1',
    'charset-normalizer==2.1.1',
    'click==7.1.2',
    'click-default-group==1.2.2',
    'click-didyoumean==0.3.0',
    'click-plugins==1.1.1',
    'click-repl==0.2.0',
    'colorama==0.4.6',
    'cryptography==38.0.3',
    'decorator==5.1.1',
    'defusedxml==0.7.1',
    'deprecated==1.2.13',
    'dnspython==2.2.1',
    'dojson==1.4.0',
    'edtf==4.0.1',
    'elasticsearch==7.13.4',
    'elasticsearch-dsl==7.4.0',
    'email-validator==1.3.0',
    'entrypoints==0.4',
    'executing==1.2.0',
    'fastjsonschema==2.16.2',
    'flask==1.1.4',
    'flask-admin==1.6.0',
    'flask-alembic==2.0.1',
    'flask-babelex==0.9.4',
    'flask-breadcrumbs==0.5.1',
    'flask-caching==2.0.1',
    'flask-celeryext==0.4.3',
    'flask-collect-invenio==1.4.0',
    'flask-cors==3.0.10',
    'flask-iiif==0.6.3',
    'flask-kvsession-invenio==0.6.3',
    'flask-limiter==1.1.0',
    'flask-login==0.4.1',
    'flask-mail==0.9.1',
    'flask-menu==0.7.2',
    'flask-oauthlib==0.9.6',
    'flask-principal==0.4.0',
    'flask-resources==0.8.4',
    'flask-restful==0.3.9',
    'flask-security==3.0.0',
    'flask-shell-ipython==0.4.1',
    'flask-sqlalchemy==2.5.1',
    'flask-talisman==0.8.1',
    'flask-webpackext==1.0.2',
    'flask-wtf==0.15.1',
    'fs==2.4.16',
    'ftfy==6.1.1',
    'future==0.18.2',
    'geojson==2.5.0',
    'idna==3.4',
    'idutils==1.1.13',
    'importlib-metadata==4.13.0',
    'importlib-resources==5.10.0',
    'infinity==1.5',
    'intervals==0.9.2',
    'invenio==3.5.0a4',
    'invenio-access==1.4.2',
    'invenio-accounts==1.4.11',
    'invenio-admin==1.3.2',
    'invenio-app==1.3.4',
    'invenio-assets==1.2.7',
    'invenio-base==1.2.13',
    'invenio-cache==1.1.1',
    'invenio-celery==1.2.5',
    'invenio-config==1.0.3',
    'invenio-db==1.0.14',
    'invenio-files-rest==1.3.3',
    'invenio-formatter==1.1.3',
    'invenio-i18n==1.3.2',
    'invenio-iiif==1.2.0',
    'invenio-indexer==1.2.7',
    'invenio-jsonschemas==1.1.4',
    'invenio-logging==1.3.2',
    'invenio-mail==1.0.2',
    'invenio-oaiserver==1.4.2',
    'invenio-oauth2server==1.3.7',
    'invenio-oauthclient==1.5.4',
    'invenio-pidstore==1.2.3',
    'invenio-previewer==1.3.7',
    'invenio-records==1.6.1',
    'invenio-records-files==1.2.1',
    'invenio-records-permissions==0.13.2',
    'invenio-records-resources==0.19.4',
    'invenio-records-rest==1.9.0',
    'invenio-records-ui==1.2.0',
    'invenio-rest==1.2.8',
    'invenio-search==1.4.2',
    'invenio-search-ui==2.0.11',
    'invenio-theme==1.3.31',
    'ipython==8.6.0',
    'isbnlib==3.10.12',
    'itsdangerous==1.1.0',
    'jedi==0.18.1',
    'jinja2==2.11.3',
    'jmespath==1.0.1',
    'jsmin==3.0.1',
    'jsonpatch==1.32',
    'jsonpointer==2.3',
    'jsonref==1.0.1',
    'jsonresolver==0.3.2',
    'jsonschema==3.2.0',
    'jupyter-client==7.4.5',
    'jupyter-core==5.0.0',
    'jupyterlab-pygments==0.2.2',
    'kombu==5.2.4',
    'limits==1.6',
    'luqum==0.12.0',
    'lxml==4.9.1',
    'mako==1.2.3',
    'markupsafe==2.0.1',
    'marshmallow==3.19.0',
    'marshmallow-oneofschema==3.0.1',
    'marshmallow-utils==0.5.7',
    'matplotlib-inline==0.1.6',
    'maxminddb==2.2.0',
    'maxminddb-geolite2==2018.703',
    'mistune==0.8.4',
    'msgpack==1.0.4',
    'nbclient==0.5.13',
    'nbconvert==6.4.5',
    'nbformat==5.7.0',
    'nest-asyncio==1.5.6',
    'node-semver==0.1.1',
    'oauthlib==2.1.0',
    'packaging==21.3',
    'pandocfilters==1.5.0',
    'parso==0.8.3',
    'passlib==1.7.4',
    'pexpect==4.8.0',
    'pickleshare==0.7.5',
    'pillow==9.3.0',
    'platformdirs==2.5.3',
    'pluggy==0.13.1',
    'ply==3.11',
    'prompt-toolkit==3.0.32',
    'psycopg2-binary==2.9.5',
    'ptyprocess==0.7.0',
    'pure-eval==0.2.2',
    'py==1.11.0',
    'pycountry==22.3.5',
    'pycparser==2.21',
    'pygments==2.13.0',
    'pyjwt==2.6.0',
    'pynpm==0.1.2',
    'pyparsing==3.0.9',
    'pyrsistent==0.19.2',
    'python-dateutil==2.8.2',
    'pytz==2022.6',
    'pywebpack==1.2.0',
    'pyzmq==24.0.1',
    'redis==4.3.4',
    'requests==2.28.1',
    'requests-oauthlib==1.1.0',
    's3-client-lib==0.1.9.post1',
    's3transfer==0.6.0',
    'sentry-sdk==1.10.1',
    'setuptools==65.5.1',
    'simplejson==3.17.6',
    'simplekv==0.14.1',
    'six==1.16.0',
    'soupsieve==2.3.2.post1',
    'speaklater==1.3',
    'sqlalchemy==1.3.24',
    'sqlalchemy-continuum==1.3.13',
    'sqlalchemy-utils==0.38.3',
    'stack-data==0.6.0',
    'testpath==0.6.0',
    'tornado==6.2',
    'traitlets==5.5.0',
    'ua-parser==0.16.1',
    'uritemplate==4.1.1',
    'uritools==4.0.0',
    'urllib3==1.26.12',
    'validators==0.20.0',
    'vine==5.0.0',
    'wand==0.6.10',
    'wcwidth==0.2.5',
    'webargs==5.5.3',
    'webencodings==0.5.1',
    'werkzeug==1.0.1',
    'wrapt==1.14.1',
    'wtforms==2.3.3',
    'wtforms-alchemy==0.18.0',
    'wtforms-components==0.10.5',
    'xmltodict==0.12.0',
    'zipp==3.10.0',
]

packages = find_packages()

# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('oarepo', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

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
