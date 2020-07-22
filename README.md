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
| deploy      | All the dependencies needed for a basic repository deployment                            |
| deploy-es7  | All the ElasticSearch 7 compatible dependencies needed for a basic repository deployment |
| openid      | Dependencies needed for openid authentication                                            |
| multisum    | Support for multiple file checksums (deprecated)                                         |
| files       | Support for uploading files                                                              |
| acls        | ACLs support                                                                             |
| links       | Enable linking to another records                                                        |
| models      | Includes all the common data models (DCObject, multilingual fields, Invenio model,...)   |
| includes    | Adds support to compose ES mappings by including another mappings                        |
| taxonomies  | Adds support for taxonomic trees                                                         |
| tests       | Includes test dependencies                                                               |
| draft       | Adds support for draft records                                                           |
| iiif        | Adds support for file (image) preview generation                                         |
| micro-api   | A WSGI app to serve API-only apps under the `/api` prefix                                |

They could be installed, depending on needs of each repository application, by running:

```
pip install oarepo[bundle-name]
```
