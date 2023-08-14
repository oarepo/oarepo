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
        'alembic==1.10.2',
        'amqp==5.1.1',
        'angular-gettext-babel==0.3',
        'aniso8601==9.0.1',
        'appnope==0.1.3',
        'arrow==1.2.3',
        'asttokens==2.2.1',
        'async-generator==1.10',
        'async-timeout==4.0.2',
        'atomicwrites==1.4.1',
        'attrs==22.2.0',
        'babel==2.12.1',
        'babel-edtf==1.0.0',
        'backcall==0.2.0',
        'base32-lib==1.0.2',
        'billiard==3.6.4.0',
        'bleach==6.0.0',
        'blinker==1.5',
        'boto3==1.26.94',
        'botocore==1.29.94',
        'build==0.10.0',
        'cachelib==0.9.0',
        'cchardet==2.1.7',
        'celery==5.0.5',
        'certifi==2022.12.7',
        'cffi==1.15.1',
        'charset-normalizer==3.1.0',
        'check-manifest==0.49',
        'click==7.1.2',
        'click-default-group==1.2.2',
        'click-didyoumean==0.3.0',
        'click-plugins==1.1.1',
        'click-repl==0.2.0',
        'colorama==0.4.6',
        'coverage==4.5.4',
        'cryptography==39.0.2',
        'decorator==5.1.1',
        'defusedxml==0.7.1',
        'deprecated==1.2.13',
        'dnspython==2.3.0',
        'docker-services-cli==0.6.0',
        'dojson==1.4.0',
        'edtf==4.0.1',
        'elasticsearch==7.17.9',
        'elasticsearch-dsl==7.4.1',
        'email-validator==1.3.1',
        'entrypoints==0.4',
        'exceptiongroup==1.1.1',
        'execnet==1.9.0',
        'executing==1.2.0',
        'fastjsonschema==2.16.3',
        'flask==1.1.4',
        'flask-admin==1.6.1',
        'flask-alembic==2.0.1',
        'flask-assets==2.0',
        'flask-babelex==0.9.4',
        'flask-breadcrumbs==0.5.1',
        'flask-caching==2.0.2',
        'flask-celeryext==0.3.4',
        'flask-collect==1.2.2',
        'flask-cors==3.0.10',
        'flask-iiif==0.6.3',
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
        'flask-sqlalchemy==2.5.1',
        'flask-talisman==0.5.0',
        'flask-webpackext==1.0.2',
        'flask-wtf==0.15.1',
        'fs==0.5.4',
        'ftfy==4.4.3',
        'future==0.18.3',
        'geojson==2.5.0',
        'h11==0.14.0',
        'html5lib==1.1',
        'idna==3.4',
        'idutils==1.2.1',
        'importlib-metadata==6.0.0',
        'importlib-resources==5.12.0',
        'infinity==1.5',
        'intervals==0.9.2',
        'invenio==3.3.0',
        'invenio-access==1.4.2',
        'invenio-accounts==1.4.2',
        'invenio-admin==1.2.1',
        'invenio-app==1.2.7',
        'invenio-assets==1.1.6',
        'invenio-base==1.2.13',
        'invenio-cache==1.1.1',
        'invenio-celery==1.2.2',
        'invenio-config==1.0.3',
        'invenio-db==1.0.14',
        'invenio-files-rest==1.2.0',
        'invenio-formatter==1.0.3',
        'invenio-i18n==1.2.0',
        'invenio-iiif==1.1.1',
        'invenio-indexer==1.1.4',
        'invenio-jsonschemas==1.1.4',
        'invenio-logging==1.3.1',
        'invenio-mail==1.0.2',
        'invenio-oaiserver==1.2.1',
        'invenio-oauth2server==1.3.1',
        'invenio-oauthclient==1.4.0',
        'invenio-pidstore==1.2.4',
        'invenio-previewer==1.2.2',
        'invenio-records==1.3.2',
        'invenio-records-files==1.2.1',
        'invenio-records-rest==1.7.2',
        'invenio-records-ui==1.1.0',
        'invenio-rest==1.2.8',
        'invenio-search==1.3.1',
        'invenio-search-ui==1.2.0',
        'invenio-theme==1.1.5',
        'ipython==8.11.0',
        'isbnlib==3.10.13',
        'isort==5.12.0',
        'itsdangerous==1.1.0',
        'jedi==0.18.2',
        'jinja2==2.11.3',
        'jmespath==1.0.1',
        'jsmin==3.0.1',
        'jsonpatch==1.32',
        'jsonpointer==2.3',
        'jsonref==1.1.0',
        'jsonresolver==0.3.2',
        'jsonschema==3.2.0',
        'jupyter-client==7.2.0',
        'jupyter-core==5.3.0',
        'kombu==5.2.4',
        'limits==3.2.0',
        'lxml==4.9.2',
        'mako==1.2.4',
        'markupsafe==2.0.1',
        'marshmallow==3.19.0',
        'marshmallow-oneofschema==3.0.1',
        'marshmallow-utils==0.4.0',
        'matplotlib-inline==0.1.6',
        'maxminddb==2.2.0',
        'maxminddb-geolite2==2018.703',
        'mistune==0.8.4',
        'more-itertools==9.1.0',
        'msgpack==1.0.5',
        'nbconvert==5.6.1',
        'nbformat==5.7.3',
        'nest-asyncio==1.5.6',
        'node-semver==0.1.1',
        'oauthlib==2.1.0',
        'outcome==1.2.0',
        'packaging==23.0',
        'pandocfilters==1.5.0',
        'parso==0.8.3',
        'passlib==1.7.4',
        'pep8==1.7.1',
        'pexpect==4.8.0',
        'pickleshare==0.7.5',
        'pillow==9.4.0',
        'platformdirs==3.1.1',
        'pluggy==0.13.1',
        'prompt-toolkit==3.0.38',
        'psycopg2-binary==2.9.5',
        'ptyprocess==0.7.0',
        'pure-eval==0.2.2',
        'py==1.11.0',
        'pycountry==22.3.5',
        'pycparser==2.21',
        'pydocstyle==6.3.0',
        'pygments==2.14.0',
        'pyjwt==2.6.0',
        'pynpm==0.1.2',
        'pyparsing==3.0.9',
        'pyproject-hooks==1.0.0',
        'pyrsistent==0.19.3',
        'pysocks==1.7.1',
        'pytest==4.6.11',
        'pytest-cache==1.0',
        'pytest-cov==2.10.1',
        'pytest-flask==0.15.1',
        'pytest-invenio[docs]==1.3.4',
        'pytest-pep8==1.0.6',
        'python-dateutil==2.8.2',
        'pytz==2022.7.1',
        'pywebpack==1.2.0',
        'pyzmq==25.0.1',
        'redis==4.5.1',
        'requests==2.28.2',
        'requests-oauthlib==1.1.0',
        's3-client-lib==0.2.2',
        's3transfer==0.6.0',
        'selenium==4.8.2',
        'sentry-sdk==1.17.0',
        'setuptools==57.5.0',
        'simplejson==3.18.4',
        'simplekv==0.14.1',
        'six==1.16.0',
        'sniffio==1.3.0',
        'snowballstemmer==2.2.0',
        'sortedcontainers==2.4.0',
        'speaklater==1.3',
        'sqlalchemy==1.3.24',
        'sqlalchemy-continuum==1.3.14',
        'sqlalchemy-utils==0.35.0',
        'stack-data==0.6.2',
        'testpath==0.6.0',
        'tomli==2.0.1',
        'tornado==6.3.3',
        'traitlets==5.9.0',
        'trio==0.22.0',
        'trio-websocket==0.10.0',
        'typing-extensions==4.5.0',
        'ua-parser==0.16.1',
        'uritemplate==4.1.1',
        'uritools==4.0.1',
        'urllib3==1.26.15',
        'validators==0.20.0',
        'vine==5.0.0',
        'wand==0.6.11',
        'wcwidth==0.2.6',
        'webargs==5.5.3',
        'webassets==2.0',
        'webencodings==0.5.1',
        'werkzeug==1.0.1',
        'wrapt==1.15.0',
        'wsproto==1.2.0',
        'wtforms==2.3.3',
        'wtforms-alchemy==0.18.0',
        'wtforms-components==0.10.5',
        'zipp==3.15.0',
    ]
}

setup_requires = [
    'pytest-runner>=3.0.0,<5',
]

install_requires = [
    'alembic==1.10.2',
    'amqp==5.1.1',
    'angular-gettext-babel==0.3',
    'aniso8601==9.0.1',
    'appnope==0.1.3',
    'arrow==1.2.3',
    'asttokens==2.2.1',
    'async-timeout==4.0.2',
    'attrs==22.2.0',
    'babel==2.12.1',
    'babel-edtf==1.0.0',
    'backcall==0.2.0',
    'base32-lib==1.0.2',
    'billiard==3.6.4.0',
    'bleach==6.0.0',
    'blinker==1.5',
    'boto3==1.26.94',
    'botocore==1.29.94',
    'cachelib==0.9.0',
    'cchardet==2.1.7',
    'celery==5.0.5',
    'certifi==2022.12.7',
    'cffi==1.15.1',
    'charset-normalizer==3.1.0',
    'click==7.1.2',
    'click-default-group==1.2.2',
    'click-didyoumean==0.3.0',
    'click-plugins==1.1.1',
    'click-repl==0.2.0',
    'colorama==0.4.6',
    'cryptography==39.0.2',
    'decorator==5.1.1',
    'defusedxml==0.7.1',
    'deprecated==1.2.13',
    'dnspython==2.3.0',
    'dojson==1.4.0',
    'edtf==4.0.1',
    'elasticsearch==7.17.9',
    'elasticsearch-dsl==7.4.1',
    'email-validator==1.3.1',
    'entrypoints==0.4',
    'executing==1.2.0',
    'fastjsonschema==2.16.3',
    'flask==1.1.4',
    'flask-admin==1.6.1',
    'flask-alembic==2.0.1',
    'flask-assets==2.0',
    'flask-babelex==0.9.4',
    'flask-breadcrumbs==0.5.1',
    'flask-caching==2.0.2',
    'flask-celeryext==0.3.4',
    'flask-collect==1.2.2',
    'flask-cors==3.0.10',
    'flask-iiif==0.6.3',
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
    'flask-sqlalchemy==2.5.1',
    'flask-talisman==0.5.0',
    'flask-webpackext==1.0.2',
    'flask-wtf==0.15.1',
    'fs==0.5.4',
    'ftfy==4.4.3',
    'future==0.18.3',
    'geojson==2.5.0',
    'html5lib==1.1',
    'idna==3.4',
    'idutils==1.2.1',
    'importlib-metadata==6.0.0',
    'importlib-resources==5.12.0',
    'infinity==1.5',
    'intervals==0.9.2',
    'invenio==3.3.0',
    'invenio-access==1.4.2',
    'invenio-accounts==1.4.2',
    'invenio-admin==1.2.1',
    'invenio-app==1.2.7',
    'invenio-assets==1.1.6',
    'invenio-base==1.2.13',
    'invenio-cache==1.1.1',
    'invenio-celery==1.2.2',
    'invenio-config==1.0.3',
    'invenio-db==1.0.14',
    'invenio-files-rest==1.2.0',
    'invenio-formatter==1.0.3',
    'invenio-i18n==1.2.0',
    'invenio-iiif==1.1.1',
    'invenio-indexer==1.1.4',
    'invenio-jsonschemas==1.1.4',
    'invenio-logging==1.3.1',
    'invenio-mail==1.0.2',
    'invenio-oaiserver==1.2.1',
    'invenio-oauth2server==1.3.1',
    'invenio-oauthclient==1.4.0',
    'invenio-pidstore==1.2.4',
    'invenio-previewer==1.2.2',
    'invenio-records==1.3.2',
    'invenio-records-files==1.2.1',
    'invenio-records-rest==1.7.2',
    'invenio-records-ui==1.1.0',
    'invenio-rest==1.2.8',
    'invenio-search==1.3.1',
    'invenio-search-ui==1.2.0',
    'invenio-theme==1.1.5',
    'ipython==8.11.0',
    'isbnlib==3.10.13',
    'itsdangerous==1.1.0',
    'jedi==0.18.2',
    'jinja2==2.11.3',
    'jmespath==1.0.1',
    'jsmin==3.0.1',
    'jsonpatch==1.32',
    'jsonpointer==2.3',
    'jsonref==1.1.0',
    'jsonresolver==0.3.2',
    'jsonschema==3.2.0',
    'jupyter-client==7.2.0',
    'jupyter-core==5.3.0',
    'kombu==5.2.4',
    'limits==3.2.0',
    'lxml==4.9.2',
    'mako==1.2.4',
    'markupsafe==2.0.1',
    'marshmallow==3.19.0',
    'marshmallow-oneofschema==3.0.1',
    'marshmallow-utils==0.4.0',
    'matplotlib-inline==0.1.6',
    'maxminddb==2.2.0',
    'maxminddb-geolite2==2018.703',
    'mistune==0.8.4',
    'msgpack==1.0.5',
    'nbconvert==5.6.1',
    'nbformat==5.7.3',
    'nest-asyncio==1.5.6',
    'node-semver==0.1.1',
    'oauthlib==2.1.0',
    'packaging==23.0',
    'pandocfilters==1.5.0',
    'parso==0.8.3',
    'passlib==1.7.4',
    'pexpect==4.8.0',
    'pickleshare==0.7.5',
    'pillow==9.4.0',
    'platformdirs==3.1.1',
    'pluggy==0.13.1',
    'prompt-toolkit==3.0.38',
    'psycopg2-binary==2.9.5',
    'ptyprocess==0.7.0',
    'pure-eval==0.2.2',
    'pycountry==22.3.5',
    'pycparser==2.21',
    'pygments==2.14.0',
    'pyjwt==2.6.0',
    'pynpm==0.1.2',
    'pyparsing==3.0.9',
    'pyrsistent==0.19.3',
    'python-dateutil==2.8.2',
    'pytz==2022.7.1',
    'pywebpack==1.2.0',
    'pyzmq==25.0.1',
    'redis==4.5.1',
    'requests==2.28.2',
    'requests-oauthlib==1.1.0',
    's3-client-lib==0.2.2',
    's3transfer==0.6.0',
    'sentry-sdk==1.17.0',
    'setuptools==57.5.0',
    'simplejson==3.18.4',
    'simplekv==0.14.1',
    'six==1.16.0',
    'speaklater==1.3',
    'sqlalchemy==1.3.24',
    'sqlalchemy-continuum==1.3.14',
    'sqlalchemy-utils==0.35.0',
    'stack-data==0.6.2',
    'testpath==0.6.0',
    'tornado==6.3.3',
    'traitlets==5.9.0',
    'typing-extensions==4.5.0',
    'ua-parser==0.16.1',
    'uritemplate==4.1.1',
    'uritools==4.0.1',
    'urllib3==1.26.15',
    'validators==0.20.0',
    'vine==5.0.0',
    'wand==0.6.11',
    'wcwidth==0.2.6',
    'webargs==5.5.3',
    'webassets==2.0',
    'webencodings==0.5.1',
    'werkzeug==1.0.1',
    'wrapt==1.15.0',
    'wtforms==2.3.3',
    'wtforms-alchemy==0.18.0',
    'wtforms-components==0.10.5',
    'zipp==3.15.0',
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
