# Bug: OpenSearch aliases are never created during `./run.sh reset`, breaking all search queries that use alias names

## Summary

After `./run.sh reset` (which delegates to `.runner.sh reset`), OpenSearch indices are created but their aliases are not. Every InvenioRDM search query that resolves an index by alias name fails with `NotFoundError(404, 'index_not_found_exception', 'no such index [<prefix>-<alias>]')`. This affects the vocabulary search, the dataset search, and all other record type searches.

## Affected component

`.runner.sh` (oarepo runner script, downloaded from `https://raw.githubusercontent.com/oarepo/oarepo/main/tools/repository_runner.sh`)

## Steps to reproduce

1. Run `./run.sh reset` on a fresh checkout.
2. Start the development server with `./run.sh run`.
3. Navigate to any search page in the UI (e.g., Datasets).

**Result:**
```
opensearchpy.exceptions.NotFoundError: NotFoundError(404,
  'index_not_found_exception',
  'no such index [frozen_testing-vocabularies]',
  frozen_testing-vocabularies, index_or_alias)
```

## Root cause

The runner's reset sequence creates the OpenSearch indices (via `invenio index create` or `invenio index init`) but does not create the aliases that InvenioRDM uses to access those indices. In a correctly initialized instance, `invenio index create` should create both the versioned index (e.g., `frozen_testing-vocabularies-vocabulary-v1.0.0`) and an alias pointing to it (e.g., `frozen_testing-vocabularies`).

After reset, all indices exist but have no aliases:

```
frozen_testing-vocabularies-vocabulary-v1.0.0  ->  (no alias)
frozen_testing-dataset-metadata-v1.0.0         ->  (no alias)
frozen_testing-users-user-v3.0.0               ->  (no alias)
... (all indices similarly missing aliases)
```

Additionally, several expected indices are entirely missing (e.g., `frozen_testing-users-user-v*.0.0`, `frozen_testing-communities-*`, `frozen_testing-requests-*`), requiring a separate `invenio index create` pass to create them.

## Impact

The instance is completely non-functional after reset. All UI search pages fail with 404 index errors. This is a blocking issue for any fresh setup.

## Workaround (applied in this repository)

After reset, manually create all missing indices and aliases from within the Invenio shell:

```python
from flask import current_app
from invenio_search import current_search, current_search_client

prefix = current_app.config.get('SEARCH_INDEX_PREFIX', '')
existing = set(current_search_client.cat.indices(h='index').strip().split('\n'))

# Create any missing indices
for alias_name, index_set in current_search.aliases.items():
    for idx in index_set:
        full_idx = prefix + idx
        if full_idx not in existing:
            list(current_search.create_index(idx, ignore=[400]))

# Refresh existing index list and create all aliases
existing = set(current_search_client.cat.indices(h='index').strip().split('\n'))
actions = []
for alias_name, index_set in current_search.aliases.items():
    full_alias = prefix + alias_name
    for idx in index_set:
        full_idx = prefix + idx
        if full_idx in existing:
            actions.append({'add': {'index': full_idx, 'alias': full_alias}})

current_search_client.indices.update_aliases({'actions': actions})
```

Note: indices created via `current_search.create_index()` may receive a timestamp suffix (e.g., `frozen_testing-users-user-v3.0.0-1777386382`); the alias must be pointed at the suffixed name.
