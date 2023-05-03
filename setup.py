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
        'alabaster==0.7.13',
        'alembic==1.10.4',
        'amqp==5.1.1',
        'aniso8601==9.0.1',
        'appdirs==1.4.4',
        'arrow==1.2.3',
        'asttokens==2.2.1',
        'async-timeout==4.0.2',
        'attrs==23.1.0',
        'Babel==2.10.3',
        'babel-edtf==1.0.0',
        'backcall==0.2.0',
        'base32-lib==1.0.2',
        'beautifulsoup4==4.12.2',
        'billiard==3.6.4.0',
        'black==23.3.0',
        'bleach==6.0.0',
        'blinker==1.6.2',
        'boto3==1.26.125',
        'botocore==1.29.125',
        'build==0.10.0',
        'cachelib==0.9.0',
        'cairocffi==1.5.1',
        'CairoSVG==2.7.0',
        'cchardet==2.1.7',
        'celery==5.2.7',
        'certifi==2022.12.7',
        'cffi==1.15.1',
        'charset-normalizer==3.1.0',
        'check-manifest==0.49',
        'citeproc-py==0.6.0',
        'citeproc-py-styles==0.1.3',
        'click==8.1.3',
        'click-default-group==1.2.2',
        'click-didyoumean==0.3.0',
        'click-plugins==1.1.1',
        'click-repl==0.2.0',
        'coverage==5.5',
        'cryptography==40.0.2',
        'cssselect2==0.7.0',
        'datacite==1.1.3',
        'dcxml==0.1.2',
        'decorator==5.1.1',
        'defusedxml==0.7.1',
        'dictdiffer==0.9.0',
        'dnspython==2.3.0',
        'Docker-Services-CLI==0.6.1',
        'docutils==0.19',
        'dojson==1.4.0',
        'edtf==4.0.1',
        'email-validator==2.0.0.post2',
        'entrypoints==0.4',
        'executing==1.2.0',
        'Faker==18.6.1',
        'fastjsonschema==2.16.3',
        'Flask==2.2.5',
        'Flask-Admin==1.6.1',
        'Flask-Alembic==2.0.1',
        'Flask-Babel==2.0.0',
        'Flask-BabelEx==0.9.4',
        'Flask-Breadcrumbs==0.5.1',
        'Flask-Caching==2.0.2',
        'Flask-CeleryExt==0.5.0',
        'Flask-Collect-Invenio==1.4.0',
        'Flask-Cors==3.0.10',
        'flask-iiif==0.6.3',
        'Flask-KVSession-Invenio==0.6.3',
        'Flask-Limiter==1.1.0',
        'Flask-Login==0.6.2',
        'Flask-Mail==0.9.1',
        'Flask-Menu==0.7.2',
        'Flask-OAuthlib==0.9.6',
        'Flask-Principal==0.4.0',
        'flask-resources==0.9.1',
        'Flask-RESTful==0.3.9',
        'Flask-Security-Invenio==3.1.4',
        'flask-shell-ipython==0.5.1',
        'Flask-SQLAlchemy==2.5.1',
        'flask-talisman==0.8.1',
        'flask-webpackext==1.0.2',
        'Flask-WTF==1.1.1',
        'fs==2.4.16',
        'fsspec==2023.4.0',
        'ftfy==4.4.3',
        'future==0.18.3',
        'geojson==3.0.1',
        'github3.py==4.0.1',
        'greenlet==2.0.2',
        'html5lib==1.1',
        'idna==3.4',
        'idutils==1.2.1',
        'imagesize==1.4.1',
        'importlib-metadata==4.13.0',
        'importlib-resources==5.12.0',
        'infinity==1.5',
        'iniconfig==2.0.0',
        'intervals==0.9.2',
        'invenio-access==1.4.5',
        'invenio-accounts==2.0.2',
        'invenio-admin==1.3.2',
        'invenio-administration==1.0.6',
        'invenio-app==1.3.4',
        'invenio-assets==2.0.0',
        'invenio-base==1.2.15',
        'invenio-cache==1.1.1',
        'invenio-celery==1.2.5',
        'invenio-communities==4.1.2',
        'invenio-config==1.0.3',
        'invenio-db==1.0.14',
        'invenio-drafts-resources==1.0.4',
        'invenio-files-rest==1.4.0',
        'invenio-formatter==1.1.4',
        'invenio-i18n==1.3.3',
        'invenio-indexer==2.1.1',
        'invenio-jsonschemas==1.1.4',
        'invenio-logging==1.3.2',
        'invenio-mail==1.0.2',
        'invenio-oaiserver==2.1.1',
        'invenio-oauth2server==1.3.8',
        'invenio-oauthclient==2.1.1',
        'invenio-pages==2.0.0',
        'invenio-pidstore==1.2.4',
        'invenio-previewer==1.3.9',
        'invenio-records==2.0.1',
        'invenio-records-files==1.2.1',
        'invenio-records-permissions==0.15.3',
        'invenio-records-resources==1.0.9',
        'invenio-records-rest==2.1.0',
        'invenio-records-ui==1.2.0',
        'invenio-requests==1.0.5',
        'invenio-rest==1.2.8',
        'invenio-s3==1.0.6',
        'invenio-search==2.2.0',
        'invenio-search-ui==2.3.0',
        'invenio-theme==1.4.8',
        'invenio-userprofiles==2.0.5',
        'invenio-users-resources==1.0.2',
        'invenio-vocabularies==1.0.4',
        'ipython==8.13.1',
        'isbnlib==3.10.14',
        'isort==5.12.0',
        'itsdangerous==2.0.1',
        'jedi==0.18.2',
        'Jinja2==3.1.2',
        'jmespath==1.0.1',
        'jsmin==3.0.1',
        'jsonpatch==1.32',
        'jsonpointer==2.3',
        'jsonref==1.1.0',
        'jsonresolver==0.3.2',
        'jsonschema==4.17.3',
        'jupyter_client==8.2.0',
        'jupyter_core==5.3.0',
        'jupyterlab-pygments==0.2.2',
        'kombu==5.2.4',
        'limits==1.6',
        'luqum==0.13.0',
        'lxml==4.9.2',
        'Mako==1.2.4',
        'MarkupSafe==2.1.2',
        'marshmallow==3.19.0',
        'marshmallow-oneofschema==3.0.1',
        'marshmallow-utils==0.5.8',
        'matplotlib-inline==0.1.6',
        'maxminddb==2.2.0',
        'maxminddb-geolite2==2018.703',
        'mistune==0.8.4',
        'mock==3.0.5',
        'msgpack==1.0.5',
        'mypy-extensions==1.0.0',
        'nbclient==0.7.4',
        'nbconvert==6.5.4',
        'nbformat==5.8.0',
        'node-semver==0.1.1',
        'oauthlib==2.1.0',
        'opensearch-dsl==2.1.0',
        'opensearch-py==2.2.0',
        'packaging==23.1',
        'pandocfilters==1.5.0',
        'parso==0.8.3',
        'passlib==1.7.4',
        'pathspec==0.11.1',
        'pexpect==4.8.0',
        'pickleshare==0.7.5',
        'Pillow==9.5.0',
        'pip-tools==6.13.0',
        'platformdirs==3.5.0',
        'pluggy==0.13.1',
        'ply==3.11',
        'prompt-toolkit==3.0.38',
        'psycopg2-binary==2.9.6',
        'ptyprocess==0.7.0',
        'pure-eval==0.2.2',
        'py==1.11.0',
        'pycodestyle==2.10.0',
        'pycountry==22.3.5',
        'pycparser==2.21',
        'pydocstyle==6.3.0',
        'Pygments==2.15.1',
        'PyJWT==2.6.0',
        'PyMySQL==1.0.3',
        'pynpm==0.1.2',
        'pyparsing==3.0.9',
        'pyproject_hooks==1.0.0',
        'pyrsistent==0.19.3',
        'pytest==7.1.3',
        'pytest-black==0.3.12',
        'pytest-cov==4.0.0',
        'pytest-flask==1.2.0',
        'pytest-invenio[docs]==2.1.2',
        'pytest-isort==3.1.0',
        'pytest-mock==3.10.0',
        'pytest-pycodestyle==2.3.1',
        'pytest-pydocstyle==2.3.2',
        'python-dateutil==2.8.2',
        'pytz==2023.3',
        'pywebpack==1.2.0',
        'PyYAML==6.0',
        'pyzmq==25.0.2',
        'redis==4.5.4',
        'requests==2.29.0',
        'requests-oauthlib==1.1.0',
        'requirements-builder==0.4.4',
        's3fs==0.4.2',
        's3transfer==0.6.0',
        'selenium==3.141.0',
        'sentry-sdk==1.21.1',
        'simplejson==3.19.1',
        'simplekv==0.14.1',
        'six==1.16.0',
        'snowballstemmer==2.2.0',
        'soupsieve==2.4.1',
        'speaklater==1.3',
        'Sphinx==7.0.0',
        'sphinxcontrib-applehelp==1.0.4',
        'sphinxcontrib-devhelp==1.0.2',
        'sphinxcontrib-htmlhelp==2.0.1',
        'sphinxcontrib-jsmath==1.0.1',
        'sphinxcontrib-qthelp==1.0.3',
        'sphinxcontrib-serializinghtml==1.1.5',
        'SQLAlchemy==1.4.48',
        'SQLAlchemy-Continuum==1.3.14',
        'SQLAlchemy-Utils==0.38.3',
        'stack-data==0.6.2',
        'tinycss2==1.2.1',
        'toml==0.10.2',
        'tomli==2.0.1',
        'tornado==6.3.1',
        'traitlets==5.9.0',
        'tripoli==2.0.0',
        'typing_extensions==4.5.0',
        'ua-parser==0.16.1',
        'uritemplate==4.1.1',
        'uritools==4.0.1',
        'urllib3==1.26.15',
        'validators==0.20.0',
        'vine==5.0.0',
        'Wand==0.6.11',
        'wcwidth==0.2.6',
        'webargs==5.5.3',
        'webencodings==0.5.1',
        'Werkzeug==2.2.3',
        'WTForms==2.3.3',
        'WTForms-Alchemy==0.18.0',
        'WTForms-Components==0.10.5',
        'xmltodict==0.12.0',
        'zipp==3.15.0',
        'zipstream-ng==1.5.0',
    ]
}

setup_requires = [
    'pytest-runner>=3.0.0,<5',
]

install_requires = [
    'alembic==1.10.4',
    'amqp==5.1.1',
    'aniso8601==9.0.1',
    'appdirs==1.4.4',
    'arrow==1.2.3',
    'asttokens==2.2.1',
    'async-timeout==4.0.2',
    'attrs==23.1.0',
    'Babel==2.10.3',
    'babel-edtf==1.0.0',
    'backcall==0.2.0',
    'base32-lib==1.0.2',
    'beautifulsoup4==4.12.2',
    'billiard==3.6.4.0',
    'bleach==6.0.0',
    'blinker==1.6.2',
    'boto3==1.26.125',
    'botocore==1.29.125',
    'build==0.10.0',
    'cachelib==0.9.0',
    'cairocffi==1.5.1',
    'CairoSVG==2.7.0',
    'cchardet==2.1.7',
    'celery==5.2.7',
    'certifi==2022.12.7',
    'cffi==1.15.1',
    'charset-normalizer==3.1.0',
    'citeproc-py==0.6.0',
    'citeproc-py-styles==0.1.3',
    'click==8.1.3',
    'click-default-group==1.2.2',
    'click-didyoumean==0.3.0',
    'click-plugins==1.1.1',
    'click-repl==0.2.0',
    'cryptography==40.0.2',
    'cssselect2==0.7.0',
    'datacite==1.1.3',
    'dcxml==0.1.2',
    'decorator==5.1.1',
    'defusedxml==0.7.1',
    'dictdiffer==0.9.0',
    'dnspython==2.3.0',
    'Docker-Services-CLI==0.6.1',
    'dojson==1.4.0',
    'edtf==4.0.1',
    'email-validator==2.0.0.post2',
    'entrypoints==0.4',
    'executing==1.2.0',
    'Faker==18.6.1',
    'fastjsonschema==2.16.3',
    'Flask==2.2.5',
    'Flask-Admin==1.6.1',
    'Flask-Alembic==2.0.1',
    'Flask-Babel==2.0.0',
    'Flask-BabelEx==0.9.4',
    'Flask-Breadcrumbs==0.5.1',
    'Flask-Caching==2.0.2',
    'Flask-CeleryExt==0.5.0',
    'Flask-Collect-Invenio==1.4.0',
    'Flask-Cors==3.0.10',
    'flask-iiif==0.6.3',
    'Flask-KVSession-Invenio==0.6.3',
    'Flask-Limiter==1.1.0',
    'Flask-Login==0.6.2',
    'Flask-Mail==0.9.1',
    'Flask-Menu==0.7.2',
    'Flask-OAuthlib==0.9.6',
    'Flask-Principal==0.4.0',
    'flask-resources==0.9.1',
    'Flask-RESTful==0.3.9',
    'Flask-Security-Invenio==3.1.4',
    'flask-shell-ipython==0.5.1',
    'Flask-SQLAlchemy==2.5.1',
    'flask-talisman==0.8.1',
    'flask-webpackext==1.0.2',
    'Flask-WTF==1.1.1',
    'fs==2.4.16',
    'fsspec==2023.4.0',
    'ftfy==4.4.3',
    'future==0.18.3',
    'geojson==3.0.1',
    'github3.py==4.0.1',
    'greenlet==2.0.2',
    'html5lib==1.1',
    'idna==3.4',
    'idutils==1.2.1',
    'importlib-metadata==4.13.0',
    'importlib-resources==5.12.0',
    'infinity==1.5',
    'intervals==0.9.2',
    'invenio-access==1.4.5',
    'invenio-accounts==2.0.2',
    'invenio-admin==1.3.2',
    'invenio-administration==1.0.6',
    'invenio-app==1.3.4',
    'invenio-assets==2.0.0',
    'invenio-base==1.2.15',
    'invenio-cache==1.1.1',
    'invenio-celery==1.2.5',
    'invenio-communities==4.1.2',
    'invenio-config==1.0.3',
    'invenio-db==1.0.14',
    'invenio-drafts-resources==1.0.4',
    'invenio-files-rest==1.4.0',
    'invenio-formatter==1.1.4',
    'invenio-i18n==1.3.3',
    'invenio-indexer==2.1.1',
    'invenio-jsonschemas==1.1.4',
    'invenio-logging==1.3.2',
    'invenio-mail==1.0.2',
    'invenio-oaiserver==2.1.1',
    'invenio-oauth2server==1.3.8',
    'invenio-oauthclient==2.1.1',
    'invenio-pages==2.0.0',
    'invenio-pidstore==1.2.4',
    'invenio-previewer==1.3.9',
    'invenio-records==2.0.1',
    'invenio-records-files==1.2.1',
    'invenio-records-permissions==0.15.3',
    'invenio-records-resources==1.0.9',
    'invenio-records-rest==2.1.0',
    'invenio-records-ui==1.2.0',
    'invenio-requests==1.0.5',
    'invenio-rest==1.2.8',
    'invenio-s3==1.0.6',
    'invenio-search==2.2.0',
    'invenio-search-ui==2.3.0',
    'invenio-theme==1.4.8',
    'invenio-userprofiles==2.0.5',
    'invenio-users-resources==1.0.2',
    'invenio-vocabularies==1.0.4',
    'ipython==8.13.1',
    'isbnlib==3.10.14',
    'itsdangerous==2.0.1',
    'jedi==0.18.2',
    'Jinja2==3.1.2',
    'jmespath==1.0.1',
    'jsmin==3.0.1',
    'jsonpatch==1.32',
    'jsonpointer==2.3',
    'jsonref==1.1.0',
    'jsonresolver==0.3.2',
    'jsonschema==4.17.3',
    'jupyter_client==8.2.0',
    'jupyter_core==5.3.0',
    'jupyterlab-pygments==0.2.2',
    'kombu==5.2.4',
    'limits==1.6',
    'luqum==0.13.0',
    'lxml==4.9.2',
    'Mako==1.2.4',
    'MarkupSafe==2.1.2',
    'marshmallow==3.19.0',
    'marshmallow-oneofschema==3.0.1',
    'marshmallow-utils==0.5.8',
    'matplotlib-inline==0.1.6',
    'maxminddb==2.2.0',
    'maxminddb-geolite2==2018.703',
    'mistune==0.8.4',
    'mock==3.0.5',
    'msgpack==1.0.5',
    'nbclient==0.7.4',
    'nbconvert==6.5.4',
    'nbformat==5.8.0',
    'node-semver==0.1.1',
    'oauthlib==2.1.0',
    'opensearch-dsl==2.1.0',
    'opensearch-py==2.2.0',
    'packaging==23.1',
    'pandocfilters==1.5.0',
    'parso==0.8.3',
    'passlib==1.7.4',
    'pexpect==4.8.0',
    'pickleshare==0.7.5',
    'Pillow==9.5.0',
    'pip-tools==6.13.0',
    'platformdirs==3.5.0',
    'pluggy==0.13.1',
    'ply==3.11',
    'prompt-toolkit==3.0.38',
    'psycopg2-binary==2.9.6',
    'ptyprocess==0.7.0',
    'pure-eval==0.2.2',
    'py==1.11.0',
    'pycountry==22.3.5',
    'pycparser==2.21',
    'Pygments==2.15.1',
    'PyJWT==2.6.0',
    'PyMySQL==1.0.3',
    'pynpm==0.1.2',
    'pyparsing==3.0.9',
    'pyproject_hooks==1.0.0',
    'pyrsistent==0.19.3',
    'python-dateutil==2.8.2',
    'pytz==2023.3',
    'pywebpack==1.2.0',
    'PyYAML==6.0',
    'pyzmq==25.0.2',
    'redis==4.5.4',
    'requests==2.29.0',
    'requests-oauthlib==1.1.0',
    'requirements-builder==0.4.4',
    's3fs==0.4.2',
    's3transfer==0.6.0',
    'sentry-sdk==1.21.1',
    'simplejson==3.19.1',
    'simplekv==0.14.1',
    'six==1.16.0',
    'soupsieve==2.4.1',
    'speaklater==1.3',
    'SQLAlchemy==1.4.48',
    'SQLAlchemy-Continuum==1.3.14',
    'SQLAlchemy-Utils==0.38.3',
    'stack-data==0.6.2',
    'tinycss2==1.2.1',
    'tomli==2.0.1',
    'tornado==6.3.1',
    'traitlets==5.9.0',
    'typing_extensions==4.5.0',
    'ua-parser==0.16.1',
    'uritemplate==4.1.1',
    'uritools==4.0.1',
    'urllib3==1.26.15',
    'validators==0.20.0',
    'vine==5.0.0',
    'Wand==0.6.11',
    'wcwidth==0.2.6',
    'webargs==5.5.3',
    'webencodings==0.5.1',
    'Werkzeug==2.2.3',
    'WTForms==2.3.3',
    'WTForms-Alchemy==0.18.0',
    'WTForms-Components==0.10.5',
    'xmltodict==0.12.0',
    'zipp==3.15.0',
    'zipstream-ng==1.5.0',
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
