CESNET, UCT Prague and NTK wrapper around invenio v3
====================================================

This meta-package contains a curated and tested set of dependencies on Invenio and OArepo libraries.
It should be considered as a base building block for creating any OA repository applications.

The package contains the following dependency bundles:



| Bundle name | Description  |
------------------------------
| deploy      |              |
| deploy-es7  |              |

They could be installed, depending on needs of each repository application, by running:

```
pip install oarepo[bundle-name]
```

.. image:: https://img.shields.io/travis/oarepo/oarepo.svg
        :target: https://travis-ci.org/oarepo/oarepo

.. image:: https://img.shields.io/coveralls/oarepo/oarepo.svg
        :target: https://coveralls.io/r/oarepo/oarepo

.. image:: https://img.shields.io/github/tag/oarepo/oarepo.svg
        :target: https://github.com/oarepo/oarepo/releases

.. image:: https://img.shields.io/pypi/dm/oarepo.svg
        :target: https://pypi.python.org/pypi/oarepo

.. image:: https://img.shields.io/github/license/oarepo/oarepo.svg
        :target: https://github.com/oarepo/oarepo/blob/master/LICENSE