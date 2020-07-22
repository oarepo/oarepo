[![](https://img.shields.io/github/license/oarepo/oarepo.svg)](https://github.com/oarepo/oarepo/blob/master/LICENSE)
[![](https://img.shields.io/travis/oarepo/oarepo.svg)](https://travis-ci.org/oarepo/oarepo)
[![](https://img.shields.io/coveralls/oarepo/oarepo.svg)](https://coveralls.io/r/oarepo/oarepo)
[![](https://img.shields.io/pypi/v/oarepo.svg)](https://pypi.org/pypi/oarepo)

CESNET, UCT Prague and NTK wrapper around invenio v3
====================================================

This meta-package contains a curated and tested set of dependencies on Invenio and OArepo libraries.
It should be considered as a base building block for creating any OA repository applications.

The package contains the following dependency bundles:



| Bundle name | Description  |
|-------------|--------------|
| deploy      |              |
| deploy-es7  |              |
| openid      |              |
| multisum    |              |
| files       |              |
| acls        |              |
| links       |              |
| models      |              |
| includes    |              |
| taxonomies  |              |
| tests       |              |
| draft       |              |
| iiif        |              |


They could be installed, depending on needs of each repository application, by running:

```
pip install oarepo[bundle-name]
```
