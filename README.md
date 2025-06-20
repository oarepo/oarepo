CESNET, UCT Prague and NTK wrapper around invenio v3
====================================================

This meta-package contains a curated and tested set of dependencies on Invenio and OArepo libraries.
It should be considered as a base building block for creating any OA repository applications.

Translations
------------

Note for RDM12:

This package also contains translations for all supported invenio languages,
as downloaded from Transifex server on June 20, 2025. 

If you want to make changes to translations, change them in the collected_translations
directory (use poedit to make tham as it will compile the .mo files for you).
If you need to change the javascript translations, add those directly 
to translation json files. Then create a PR to this repository with the changes.

During merge we'll make sure that these get propagated to RDM13 if approporiate.