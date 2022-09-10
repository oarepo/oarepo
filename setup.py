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
        'alabaster==0.7.12',
        'alembic==1.8.1',
        'amqp==5.1.1',
        'appdirs==1.4.4',
        'arrow==1.2.3',
        'asttokens==2.0.8',
        'async-timeout==4.0.2',
        'attrs==22.1.0',
        'Babel==2.10.3',
        'backcall==0.2.0',
        'base32-lib==1.0.2',
        'beautifulsoup4==4.11.1',
        'billiard==3.6.4.0',
        'black==22.8.0',
        'bleach==5.0.1',
        'blinker==1.5',
        'build==0.8.0',
        'cachelib==0.9.0',
        'cairocffi==1.3.0',
        'CairoSVG==2.5.2',
        'cchardet==2.1.7',
        'celery==5.2.7',
        'certifi==2022.6.15.1',
        'cffi==1.15.1',
        'charset-normalizer==2.1.1',
        'check-manifest==0.48',
        'click==8.1.3',
        'click-default-group==1.2.2',
        'click-didyoumean==0.3.0',
        'click-plugins==1.1.1',
        'click-repl==0.2.0',
        'coverage==5.5',
        'cryptography==38.0.1',
        'cssselect2==0.6.0',
        'decorator==5.1.1',
        'defusedxml==0.7.1',
        'Deprecated==1.2.13',
        'dnspython==2.2.1',
        'Docker-Services-CLI==0.5.0',
        'docutils==0.19',
        'dojson==1.4.0',
        'elasticsearch==7.13.4',
        'elasticsearch-dsl==7.4.0',
        'email-validator==1.2.1',
        'entrypoints==0.4',
        'executing==1.0.0',
        'fastjsonschema==2.16.1',
        'Flask==2.2.2',
        'Flask-Admin==1.6.0',
        'Flask-Alembic==2.0.1',
        'Flask-BabelEx==0.9.4',
        'Flask-Breadcrumbs==0.5.1',
        'Flask-Caching==2.0.1',
        'Flask-CeleryExt==0.4.3',
        'Flask-Collect-Invenio==1.4.0',
        'Flask-Cors==3.0.10',
        'Flask-KVSession-Invenio==0.6.3',
        'Flask-Limiter==1.1.0',
        'Flask-Login==0.6.2',
        'Flask-Mail==0.9.1',
        'Flask-Menu==0.7.2',
        'Flask-OAuthlib==0.9.6',
        'Flask-Principal==0.4.0',
        'Flask-Security-Invenio==3.1.3',
        'flask-shell-ipython==0.4.1',
        'Flask-SQLAlchemy==2.5.1',
        'flask-talisman==0.8.1',
        'flask-webpackext==1.0.2',
        'Flask-WTF==1.0.1',
        'fs==2.4.16',
        'ftfy==6.1.1',
        'future==0.18.2',
        'greenlet==1.1.3',
        'idna==3.3',
        'imagesize==1.4.1',
        'importlib-metadata==4.12.0',
        'importlib-resources==5.9.0',
        'infinity==1.5',
        'iniconfig==1.1.1',
        'intervals==0.9.2',
        'invenio-access==1.4.4',
        'invenio-accounts==2.0.0',
        'invenio-admin==1.3.2',
        'invenio-app==1.3.4',
        'invenio-assets==1.3.1',
        'invenio-base==1.2.13',
        'invenio-cache==1.1.1',
        'invenio-celery==1.2.4',
        'invenio-config==1.0.3',
        'invenio-db==1.0.14',
        'invenio-files-rest==1.3.3',
        'invenio-formatter==1.1.3',
        'invenio-i18n==1.3.2',
        'invenio-indexer==1.2.7',
        'invenio-jsonschemas==1.1.4',
        'invenio-logging==1.3.2',
        'invenio-mail==1.0.2',
        'invenio-oaiserver==1.4.2',
        'invenio-oauth2server==1.3.7',
        'invenio-oauthclient==2.0.1',
        'invenio-pidstore==1.2.3',
        'invenio-previewer==1.3.7',
        'invenio-records==1.7.6',
        'invenio-records-files==1.2.1',
        'invenio-records-rest==1.9.0',
        'invenio-records-ui==1.2.0',
        'invenio-rest==1.2.8',
        'invenio-search==1.4.2',
        'invenio-search-ui==2.1.9',
        'invenio-theme==1.3.28',
        'invenio-userprofiles==2.0.3',
        'ipython==8.5.0',
        'isort==5.10.1',
        'itsdangerous==2.0.1',
        'jedi==0.18.1',
        'Jinja2==3.1.2',
        'jsmin==3.0.1',
        'jsonpatch==1.32',
        'jsonpointer==2.3',
        'jsonref==0.2',
        'jsonresolver==0.3.1',
        'jsonschema==4.16.0',
        'jupyter-core==4.11.1',
        'jupyter_client==7.3.5',
        'jupyterlab-pygments==0.2.2',
        'kombu==5.2.4',
        'limits==1.6',
        'lxml==4.9.1',
        'Mako==1.2.2',
        'MarkupSafe==2.1.1',
        'marshmallow==3.17.1',
        'matplotlib-inline==0.1.6',
        'maxminddb==2.2.0',
        'maxminddb-geolite2==2018.703',
        'mistune==0.8.4',
        'mock==3.0.5',
        'msgpack==1.0.4',
        'mypy-extensions==0.4.3',
        'nbclient==0.6.8',
        'nbconvert==6.5.3',
        'nbformat==5.4.0',
        'nest-asyncio==1.5.5',
        'node-semver==0.1.1',
        'oauthlib==2.1.0',
        'packaging==21.3',
        'pandocfilters==1.5.0',
        'parso==0.8.3',
        'passlib==1.7.4',
        'pathspec==0.10.1',
        'pep517==0.13.0',
        'pexpect==4.8.0',
        'pickleshare==0.7.5',
        'Pillow==9.2.0',
        'pip-tools==6.8.0',
        'pkgutil_resolve_name==1.3.10',
        'platformdirs==2.5.2',
        'pluggy==0.13.1',
        'prompt-toolkit==3.0.31',
        'psycopg2-binary==2.9.3',
        'ptyprocess==0.7.0',
        'pure-eval==0.2.2',
        'py==1.11.0',
        'pycodestyle==2.9.1',
        'pycparser==2.21',
        'pydocstyle==6.1.1',
        'Pygments==2.13.0',
        'PyJWT==2.4.0',
        'PyMySQL==1.0.2',
        'pynpm==0.1.2',
        'pyparsing==3.0.9',
        'pyrsistent==0.18.1',
        'pytest==6.2.5',
        'pytest-black==0.3.9',
        'pytest-cov==3.0.0',
        'pytest-flask==1.2.0',
        'pytest-invenio[docs]==1.4.13',
        'pytest-isort==3.0.0',
        'pytest-pycodestyle==2.2.1',
        'pytest-pydocstyle==2.2.1',
        'python-dateutil==2.8.2',
        'pytz==2022.2.1',
        'pywebpack==1.2.0',
        'pyzmq==23.2.1',
        'redis==4.3.4',
        'requests==2.28.1',
        'requests-oauthlib==1.1.0',
        'requirements-builder==0.4.4',
        'selenium==3.141.0',
        'sentry-sdk==1.9.8',
        'simplejson==3.17.6',
        'simplekv==0.14.1',
        'six==1.16.0',
        'snowballstemmer==2.2.0',
        'soupsieve==2.3.2.post1',
        'speaklater==1.3',
        'Sphinx==5.1.1',
        'sphinxcontrib-applehelp==1.0.2',
        'sphinxcontrib-devhelp==1.0.2',
        'sphinxcontrib-htmlhelp==2.0.0',
        'sphinxcontrib-jsmath==1.0.1',
        'sphinxcontrib-qthelp==1.0.3',
        'sphinxcontrib-serializinghtml==1.1.5',
        'SQLAlchemy==1.4.41',
        'SQLAlchemy-Continuum==1.3.13',
        'SQLAlchemy-Utils==0.38.3',
        'stack-data==0.5.0',
        'tinycss2==1.1.1',
        'toml==0.10.2',
        'tomli==2.0.1',
        'tornado==6.2',
        'traitlets==5.3.0',
        'typing_extensions==4.3.0',
        'ua-parser==0.16.1',
        'uritools==4.0.0',
        'urllib3==1.26.12',
        'validators==0.20.0',
        'vine==5.0.0',
        'wcwidth==0.2.5',
        'webargs==5.5.3',
        'webencodings==0.5.1',
        'Werkzeug==2.2.2',
        'wrapt==1.14.1',
        'WTForms==2.3.3',
        'WTForms-Alchemy==0.18.0',
        'WTForms-Components==0.10.5',
        'zipp==3.8.1',
    ]
}

setup_requires = [
    'pytest-runner>=3.0.0,<5',
]

install_requires = [
    'alembic==1.8.1',
    'amqp==5.1.1',
    'appdirs==1.4.4',
    'arrow==1.2.3',
    'asttokens==2.0.8',
    'async-timeout==4.0.2',
    'attrs==22.1.0',
    'Babel==2.10.3',
    'backcall==0.2.0',
    'base32-lib==1.0.2',
    'beautifulsoup4==4.11.1',
    'billiard==3.6.4.0',
    'bleach==5.0.1',
    'blinker==1.5',
    'build==0.8.0',
    'cachelib==0.9.0',
    'cairocffi==1.3.0',
    'CairoSVG==2.5.2',
    'cchardet==2.1.7',
    'celery==5.2.7',
    'certifi==2022.6.15.1',
    'cffi==1.15.1',
    'charset-normalizer==2.1.1',
    'click==8.1.3',
    'click-default-group==1.2.2',
    'click-didyoumean==0.3.0',
    'click-plugins==1.1.1',
    'click-repl==0.2.0',
    'cryptography==38.0.1',
    'cssselect2==0.6.0',
    'decorator==5.1.1',
    'defusedxml==0.7.1',
    'Deprecated==1.2.13',
    'dnspython==2.2.1',
    'dojson==1.4.0',
    'elasticsearch==7.13.4',
    'elasticsearch-dsl==7.4.0',
    'email-validator==1.2.1',
    'entrypoints==0.4',
    'executing==1.0.0',
    'fastjsonschema==2.16.1',
    'Flask==2.2.2',
    'Flask-Admin==1.6.0',
    'Flask-Alembic==2.0.1',
    'Flask-BabelEx==0.9.4',
    'Flask-Breadcrumbs==0.5.1',
    'Flask-Caching==2.0.1',
    'Flask-CeleryExt==0.4.3',
    'Flask-Collect-Invenio==1.4.0',
    'Flask-Cors==3.0.10',
    'Flask-KVSession-Invenio==0.6.3',
    'Flask-Limiter==1.1.0',
    'Flask-Login==0.6.2',
    'Flask-Mail==0.9.1',
    'Flask-Menu==0.7.2',
    'Flask-OAuthlib==0.9.6',
    'Flask-Principal==0.4.0',
    'Flask-Security-Invenio==3.1.3',
    'flask-shell-ipython==0.4.1',
    'Flask-SQLAlchemy==2.5.1',
    'flask-talisman==0.8.1',
    'flask-webpackext==1.0.2',
    'Flask-WTF==1.0.1',
    'fs==2.4.16',
    'ftfy==6.1.1',
    'future==0.18.2',
    'greenlet==1.1.3',
    'idna==3.3',
    'importlib-metadata==4.12.0',
    'importlib-resources==5.9.0',
    'infinity==1.5',
    'intervals==0.9.2',
    'invenio-access==1.4.4',
    'invenio-accounts==2.0.0',
    'invenio-admin==1.3.2',
    'invenio-app==1.3.4',
    'invenio-assets==1.3.1',
    'invenio-base==1.2.13',
    'invenio-cache==1.1.1',
    'invenio-celery==1.2.4',
    'invenio-config==1.0.3',
    'invenio-db==1.0.14',
    'invenio-files-rest==1.3.3',
    'invenio-formatter==1.1.3',
    'invenio-i18n==1.3.2',
    'invenio-indexer==1.2.7',
    'invenio-jsonschemas==1.1.4',
    'invenio-logging==1.3.2',
    'invenio-mail==1.0.2',
    'invenio-oaiserver==1.4.2',
    'invenio-oauth2server==1.3.7',
    'invenio-oauthclient==2.0.1',
    'invenio-pidstore==1.2.3',
    'invenio-previewer==1.3.7',
    'invenio-records==1.7.6',
    'invenio-records-files==1.2.1',
    'invenio-records-rest==1.9.0',
    'invenio-records-ui==1.2.0',
    'invenio-rest==1.2.8',
    'invenio-search==1.4.2',
    'invenio-search-ui==2.1.9',
    'invenio-theme==1.3.28',
    'invenio-userprofiles==2.0.3',
    'ipython==8.5.0',
    'itsdangerous==2.0.1',
    'jedi==0.18.1',
    'Jinja2==3.1.2',
    'jsmin==3.0.1',
    'jsonpatch==1.32',
    'jsonpointer==2.3',
    'jsonref==0.2',
    'jsonresolver==0.3.1',
    'jsonschema==4.16.0',
    'jupyter-core==4.11.1',
    'jupyter_client==7.3.5',
    'jupyterlab-pygments==0.2.2',
    'kombu==5.2.4',
    'limits==1.6',
    'lxml==4.9.1',
    'Mako==1.2.2',
    'MarkupSafe==2.1.1',
    'marshmallow==3.17.1',
    'matplotlib-inline==0.1.6',
    'maxminddb==2.2.0',
    'maxminddb-geolite2==2018.703',
    'mistune==0.8.4',
    'mock==3.0.5',
    'msgpack==1.0.4',
    'nbclient==0.6.8',
    'nbconvert==6.5.3',
    'nbformat==5.4.0',
    'nest-asyncio==1.5.5',
    'node-semver==0.1.1',
    'oauthlib==2.1.0',
    'packaging==21.3',
    'pandocfilters==1.5.0',
    'parso==0.8.3',
    'passlib==1.7.4',
    'pep517==0.13.0',
    'pexpect==4.8.0',
    'pickleshare==0.7.5',
    'Pillow==9.2.0',
    'pip-tools==6.8.0',
    'pkgutil_resolve_name==1.3.10',
    'pluggy==0.13.1',
    'prompt-toolkit==3.0.31',
    'psycopg2-binary==2.9.3',
    'ptyprocess==0.7.0',
    'pure-eval==0.2.2',
    'py==1.11.0',
    'pycparser==2.21',
    'Pygments==2.13.0',
    'PyJWT==2.4.0',
    'PyMySQL==1.0.2',
    'pynpm==0.1.2',
    'pyparsing==3.0.9',
    'pyrsistent==0.18.1',
    'python-dateutil==2.8.2',
    'pytz==2022.2.1',
    'pywebpack==1.2.0',
    'pyzmq==23.2.1',
    'redis==4.3.4',
    'requests==2.28.1',
    'requests-oauthlib==1.1.0',
    'requirements-builder==0.4.4',
    'sentry-sdk==1.9.8',
    'simplejson==3.17.6',
    'simplekv==0.14.1',
    'six==1.16.0',
    'soupsieve==2.3.2.post1',
    'speaklater==1.3',
    'SQLAlchemy==1.4.41',
    'SQLAlchemy-Continuum==1.3.13',
    'SQLAlchemy-Utils==0.38.3',
    'stack-data==0.5.0',
    'tinycss2==1.1.1',
    'tomli==2.0.1',
    'tornado==6.2',
    'traitlets==5.3.0',
    'ua-parser==0.16.1',
    'uritools==4.0.0',
    'urllib3==1.26.12',
    'validators==0.20.0',
    'vine==5.0.0',
    'wcwidth==0.2.5',
    'webargs==5.5.3',
    'webencodings==0.5.1',
    'Werkzeug==2.2.2',
    'wrapt==1.14.1',
    'WTForms==2.3.3',
    'WTForms-Alchemy==0.18.0',
    'WTForms-Components==0.10.5',
    'zipp==3.8.1',
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

# test trig change
