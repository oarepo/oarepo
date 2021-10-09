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
        'alembic==1.7.4',
        'amqp==5.0.6',
        'angular-gettext-babel==0.3',
        'aniso8601==9.0.1',
        'appnope==0.1.2',
        'arrow==1.2.0',
        'atomicwrites==1.4.0',
        'attrs==21.2.0',
        'autosemver==0.5.5',
        'babel==2.9.1',
        'babel-edtf==1.0.0',
        'backcall==0.2.0',
        'base32-lib==1.0.2',
        'billiard==3.6.4.0',
        'bleach==4.1.0',
        'blinker==1.4',
        'boto3==1.18.58',
        'botocore==1.21.58',
        'build==0.7.0',
        'cachelib==0.4.1',
        'cchardet==2.1.7',
        'celery==5.0.5',
        'certifi==2021.10.8',
        'cffi==1.14.6',
        'charset-normalizer==2.0.6',
        'check-manifest==0.47',
        'click==7.1.2',
        'click-default-group==1.2.2',
        'click-didyoumean==0.3.0',
        'click-plugins==1.1.1',
        'click-repl==0.2.0',
        'colorama==0.4.4',
        'coverage==4.5.4',
        'cryptography==35.0.0',
        'decorator==5.1.0',
        'defusedxml==0.7.1',
        'dnspython==2.1.0',
        'docker-services-cli==0.3.1',
        'dojson==1.4.0',
        'dulwich==0.19.16',
        'edtf==4.0.1',
        'elasticsearch==7.15.0',
        'elasticsearch-dsl==7.4.0',
        'email-validator==1.1.3',
        'entrypoints==0.3',
        'execnet==1.9.0',
        'flask==1.1.4',
        'flask-admin==1.5.8',
        'flask-alembic==2.0.1',
        'flask-assets==2.0',
        'flask-babelex==0.9.4',
        'flask-breadcrumbs==0.5.1',
        'flask-caching==1.10.1',
        'flask-celeryext==0.3.4',
        'flask-collect==1.2.2',
        'flask-cors==3.0.10',
        'flask-iiif==0.6.1',
        'flask-kvsession-invenio==0.6.3',
        'flask-limiter==1.1.0',
        'flask-login==0.4.1',
        'flask-mail==0.9.1',
        'flask-menu==0.7.2',
        'flask-oauthlib==0.9.6',
        'flask-principal==0.4.0',
        'flask-restful==0.3.9',
        'flask-security==3.0.0',
        'flask-shell-ipython==0.4.1',
        'flask-sqlalchemy==2.4.4',
        'flask-talisman==0.5.0',
        'flask-webpackext==1.0.2',
        'flask-wtf==0.15.1',
        'fs==0.5.4',
        'ftfy==4.4.3',
        'future==0.18.2',
        'geojson==2.5.0',
        'html5lib==1.1',
        'idna==3.2',
        'idutils==1.1.9',
        'importlib-metadata==4.8.1',
        'importlib-resources==5.2.2',
        'infinity==1.5',
        'intervals==0.9.2',
        'invenio==3.3.0',
        'invenio-access==1.4.2',
        'invenio-accounts==1.4.2',
        'invenio-admin==1.2.1',
        'invenio-app==1.2.7',
        'invenio-assets==1.1.5',
        'invenio-base==1.2.4',
        'invenio-cache==1.1.0',
        'invenio-celery==1.2.2',
        'invenio-config==1.0.3',
        'invenio-db==1.0.9',
        'invenio-files-rest==1.2.0',
        'invenio-formatter==1.0.3',
        'invenio-i18n==1.2.0',
        'invenio-iiif==1.1.1',
        'invenio-indexer==1.1.2',
        'invenio-jsonschemas==1.1.3',
        'invenio-logging==1.3.0',
        'invenio-mail==1.0.2',
        'invenio-oaiserver==1.2.1',
        'invenio-oauth2server==1.3.1',
        'invenio-oauthclient==1.4.0',
        'invenio-pidstore==1.2.2',
        'invenio-previewer==1.2.2',
        'invenio-records==1.3.2',
        'invenio-records-files==1.2.1',
        'invenio-records-rest==1.7.2',
        'invenio-records-ui==1.1.0',
        'invenio-rest==1.2.3',
        'invenio-search==1.3.1',
        'invenio-search-ui==1.2.0',
        'invenio-theme==1.1.4',
        'ipython==7.28.0',
        'ipython-genutils==0.2.0',
        'isbnid-fork==0.5.2',
        'isort==5.9.3',
        'itsdangerous==1.1.0',
        'jedi==0.18.0',
        'jinja2==2.11.3',
        'jmespath==0.10.0',
        'jsmin==3.0.0',
        'jsonpatch==1.32',
        'jsonpointer==2.1',
        'jsonref==0.2',
        'jsonresolver==0.3.1',
        'jsonschema==4.0.1',
        'jupyter-client==7.0.6',
        'jupyter-core==4.8.1',
        'kombu==5.1.0',
        'limits==1.5.1',
        'lxml==4.6.3',
        'mako==1.1.5',
        'markupsafe==2.0.1',
        'marshmallow==3.13.0',
        'marshmallow-oneofschema==3.0.1',
        'marshmallow-utils==0.4.0',
        'matplotlib-inline==0.1.3',
        'maxminddb==2.2.0',
        'maxminddb-geolite2==2018.703',
        'mistune==0.8.4',
        'more-itertools==8.10.0',
        'msgpack==1.0.2',
        'nbconvert==5.6.1',
        'nbformat==5.1.3',
        'nest-asyncio==1.5.1',
        'node-semver==0.1.1',
        'oauthlib==2.1.0',
        'packaging==21.0',
        'pandocfilters==1.5.0',
        'parso==0.8.2',
        'passlib==1.7.4',
        'pep517==0.11.0',
        'pep8==1.7.1',
        'pexpect==4.8.0',
        'pickleshare==0.7.5',
        'pillow==8.3.2',
        'pluggy==0.13.1',
        'prompt-toolkit==3.0.20',
        'psycopg2-binary==2.9.1',
        'ptyprocess==0.7.0',
        'py==1.10.0',
        'pycountry==20.7.3',
        'pycparser==2.20',
        'pydocstyle==6.1.1',
        'pygments==2.10.0',
        'pyjwt==2.2.0',
        'pynpm==0.1.2',
        'pyparsing==2.4.7',
        'pyrsistent==0.18.0',
        'pytest==4.6.11',
        'pytest-cache==1.0',
        'pytest-cov==2.10.1',
        'pytest-flask==0.15.1',
        'pytest-invenio[docs]==1.3.4',
        'pytest-pep8==1.0.6',
        'python-dateutil==2.8.2',
        'pytz==2021.3',
        'pywebpack==1.2.0',
        'pyzmq==22.3.0',
        'redis==3.5.3',
        'requests==2.26.0',
        'requests-oauthlib==1.1.0',
        's3-client-lib==0.1.9',
        's3transfer==0.5.0',
        'selenium==3.141.0',
        'sentry-sdk==1.4.3',
        'simplejson==3.17.5',
        'simplekv==0.14.1',
        'six==1.16.0',
        'snowballstemmer==2.1.0',
        'speaklater==1.3',
        'sqlalchemy==1.3.24',
        'sqlalchemy-continuum==1.3.11',
        'sqlalchemy-utils==0.35.0',
        'testpath==0.5.0',
        'toml==0.10.2',
        'tomli==1.2.1',
        'tornado==5.1.1',
        'traitlets==5.1.0',
        'ua-parser==0.10.0',
        'uritemplate==3.0.1',
        'uritools==3.0.2',
        'urllib3==1.26.7',
        'validators==0.18.2',
        'vine==5.0.0',
        'wand==0.6.7',
        'wcwidth==0.2.5',
        'webargs==5.5.3',
        'webassets==2.0',
        'webencodings==0.5.1',
        'werkzeug==1.0.1',
        'wtforms==2.3.3',
        'wtforms-alchemy==0.17.0',
        'wtforms-components==0.10.5',
        'zipp==3.6.0',
    ]
}

setup_requires = [
    'pytest-runner>=3.0.0,<5',
]

install_requires = [
    'alembic==1.7.4',
    'amqp==5.0.6',
    'angular-gettext-babel==0.3',
    'aniso8601==9.0.1',
    'appnope==0.1.2',
    'arrow==1.2.0',
    'attrs==21.2.0',
    'autosemver==0.5.5',
    'babel==2.9.1',
    'babel-edtf==1.0.0',
    'backcall==0.2.0',
    'base32-lib==1.0.2',
    'billiard==3.6.4.0',
    'bleach==4.1.0',
    'blinker==1.4',
    'boto3==1.18.58',
    'botocore==1.21.58',
    'cachelib==0.4.1',
    'cchardet==2.1.7',
    'celery==5.0.5',
    'certifi==2021.10.8',
    'cffi==1.14.6',
    'charset-normalizer==2.0.6',
    'click==7.1.2',
    'click-default-group==1.2.2',
    'click-didyoumean==0.3.0',
    'click-plugins==1.1.1',
    'click-repl==0.2.0',
    'colorama==0.4.4',
    'cryptography==35.0.0',
    'decorator==5.1.0',
    'defusedxml==0.7.1',
    'dnspython==2.1.0',
    'dojson==1.4.0',
    'dulwich==0.19.16',
    'edtf==4.0.1',
    'elasticsearch==7.15.0',
    'elasticsearch-dsl==7.4.0',
    'email-validator==1.1.3',
    'entrypoints==0.3',
    'flask==1.1.4',
    'flask-admin==1.5.8',
    'flask-alembic==2.0.1',
    'flask-assets==2.0',
    'flask-babelex==0.9.4',
    'flask-breadcrumbs==0.5.1',
    'flask-caching==1.10.1',
    'flask-celeryext==0.3.4',
    'flask-collect==1.2.2',
    'flask-cors==3.0.10',
    'flask-iiif==0.6.1',
    'flask-kvsession-invenio==0.6.3',
    'flask-limiter==1.1.0',
    'flask-login==0.4.1',
    'flask-mail==0.9.1',
    'flask-menu==0.7.2',
    'flask-oauthlib==0.9.6',
    'flask-principal==0.4.0',
    'flask-restful==0.3.9',
    'flask-security==3.0.0',
    'flask-shell-ipython==0.4.1',
    'flask-sqlalchemy==2.4.4',
    'flask-talisman==0.5.0',
    'flask-webpackext==1.0.2',
    'flask-wtf==0.15.1',
    'fs==0.5.4',
    'ftfy==4.4.3',
    'future==0.18.2',
    'geojson==2.5.0',
    'html5lib==1.1',
    'idna==3.2',
    'idutils==1.1.9',
    'importlib-metadata==4.8.1',
    'importlib-resources==5.2.2',
    'infinity==1.5',
    'intervals==0.9.2',
    'invenio==3.3.0',
    'invenio-access==1.4.2',
    'invenio-accounts==1.4.2',
    'invenio-admin==1.2.1',
    'invenio-app==1.2.7',
    'invenio-assets==1.1.5',
    'invenio-base==1.2.4',
    'invenio-cache==1.1.0',
    'invenio-celery==1.2.2',
    'invenio-config==1.0.3',
    'invenio-db==1.0.9',
    'invenio-files-rest==1.2.0',
    'invenio-formatter==1.0.3',
    'invenio-i18n==1.2.0',
    'invenio-iiif==1.1.1',
    'invenio-indexer==1.1.2',
    'invenio-jsonschemas==1.1.3',
    'invenio-logging==1.3.0',
    'invenio-mail==1.0.2',
    'invenio-oaiserver==1.2.1',
    'invenio-oauth2server==1.3.1',
    'invenio-oauthclient==1.4.0',
    'invenio-pidstore==1.2.2',
    'invenio-previewer==1.2.2',
    'invenio-records==1.3.2',
    'invenio-records-files==1.2.1',
    'invenio-records-rest==1.7.2',
    'invenio-records-ui==1.1.0',
    'invenio-rest==1.2.3',
    'invenio-search==1.3.1',
    'invenio-search-ui==1.2.0',
    'invenio-theme==1.1.4',
    'ipython==7.28.0',
    'ipython-genutils==0.2.0',
    'isbnid-fork==0.5.2',
    'itsdangerous==1.1.0',
    'jedi==0.18.0',
    'jinja2==2.11.3',
    'jmespath==0.10.0',
    'jsmin==3.0.0',
    'jsonpatch==1.32',
    'jsonpointer==2.1',
    'jsonref==0.2',
    'jsonresolver==0.3.1',
    'jsonschema==4.0.1',
    'jupyter-client==7.0.6',
    'jupyter-core==4.8.1',
    'kombu==5.1.0',
    'limits==1.5.1',
    'lxml==4.6.3',
    'mako==1.1.5',
    'markupsafe==2.0.1',
    'marshmallow==3.13.0',
    'marshmallow-oneofschema==3.0.1',
    'marshmallow-utils==0.4.0',
    'matplotlib-inline==0.1.3',
    'maxminddb==2.2.0',
    'maxminddb-geolite2==2018.703',
    'mistune==0.8.4',
    'msgpack==1.0.2',
    'nbconvert==5.6.1',
    'nbformat==5.1.3',
    'nest-asyncio==1.5.1',
    'node-semver==0.1.1',
    'oauthlib==2.1.0',
    'packaging==21.0',
    'pandocfilters==1.5.0',
    'parso==0.8.2',
    'passlib==1.7.4',
    'pexpect==4.8.0',
    'pickleshare==0.7.5',
    'pillow==8.3.2',
    'pluggy==0.13.1',
    'prompt-toolkit==3.0.20',
    'psycopg2-binary==2.9.1',
    'ptyprocess==0.7.0',
    'py==1.10.0',
    'pycountry==20.7.3',
    'pycparser==2.20',
    'pygments==2.10.0',
    'pyjwt==2.2.0',
    'pynpm==0.1.2',
    'pyparsing==2.4.7',
    'pyrsistent==0.18.0',
    'python-dateutil==2.8.2',
    'pytz==2021.3',
    'pywebpack==1.2.0',
    'pyzmq==22.3.0',
    'redis==3.5.3',
    'requests==2.26.0',
    'requests-oauthlib==1.1.0',
    's3-client-lib==0.1.9',
    's3transfer==0.5.0',
    'sentry-sdk==1.4.3',
    'simplejson==3.17.5',
    'simplekv==0.14.1',
    'six==1.16.0',
    'speaklater==1.3',
    'sqlalchemy==1.3.24',
    'sqlalchemy-continuum==1.3.11',
    'sqlalchemy-utils==0.35.0',
    'testpath==0.5.0',
    'tornado==5.1.1',
    'traitlets==5.1.0',
    'ua-parser==0.10.0',
    'uritemplate==3.0.1',
    'uritools==3.0.2',
    'urllib3==1.26.7',
    'validators==0.18.2',
    'vine==5.0.0',
    'wand==0.6.7',
    'wcwidth==0.2.5',
    'webargs==5.5.3',
    'webassets==2.0',
    'webencodings==0.5.1',
    'werkzeug==1.0.1',
    'wtforms==2.3.3',
    'wtforms-alchemy==0.17.0',
    'wtforms-components==0.10.5',
    'zipp==3.6.0',
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
