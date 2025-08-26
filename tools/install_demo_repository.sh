#!/usr/bin/env bash

set -euo pipefail

echo "###############################################################################"
echo "#                                                                             #"
echo "#                   OAREPO Demo Repository Installer                          #"
echo "#                                                                             #"
echo "###############################################################################"
echo
echo "This command will install a sample repository with a simple metadata schema."
echo
echo "Please wait, installation in progress"
echo

LOCAL_OAREPO_DIR=${LOCAL_OAREPO_DIR:-""}

# download the installer script
if [ -z "$LOCAL_OAREPO_DIR" ] ; then
    curl -L https://raw.githubusercontent.com/oarepo/oarepo/main/tools/repository_installer.sh -o repository_installer.sh
else
    cp "$LOCAL_OAREPO_DIR/tools/repository_installer.sh" .
fi

if [ -d sample_repository ] ; then
    rm -rf sample_repository
fi

cat <<EOF >initial_config.yaml
languages: 'cs'
repository_name: 'sample_repository'
repository_description: 'Sample Repository'
repository_human_name: Sample Repository
EOF

chmod +x repository_installer.sh
./repository_installer.sh --config initial_config.yaml sample_repository


cd sample_repository

# create sample model
mkdir datasets
touch datasets/__init__.py
cat <<EOF >datasets/model.py

#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of oarepo-rdm (see https://github.com/oarepo/oarepo-rdm).
#
# oarepo-rdm is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
from __future__ import annotations

from invenio_i18n import lazy_gettext as _
from oarepo_model.api import model
from oarepo_model.presets.drafts import drafts_presets
from oarepo_model.presets.rdm import rdm_presets
from oarepo_model.presets.records_resources import records_resources_presets
from oarepo_model.datatypes.registry import from_yaml

datasets = model(
    "datasets",
    version="1.0.0",
    presets=[records_resources_presets, drafts_presets, rdm_presets],
    types=[
        from_yaml("metadata.yaml", __file__)
    ],
    metadata_type="Metadata",
    customizations=[],
)
EOF

cat <<EOF >datasets/metadata.yaml
Metadata:
  properties:
    title:
      type: keyword
      required: true
    description:
      type: keyword
EOF

# register the model to the invenio.cfg
cat <<EOF >>invenio.cfg

# datasets model registration
from datasets.model import datasets

datasets.register()
EOF

# add the model to the pyproject.toml
cat pyproject.toml | sed 's/\(module-name = \[\)/\1"datasets", /' > pyproject.toml.new
mv pyproject.toml.new pyproject.toml

cat <<'EOF' >datasets/sample_data.sh
./run.sh invenio users create -a -c "demo@test.com" --password "demodemo" --profile '{"full_name": "Demo user"}'

token=$(./run.sh invenio tokens create -n demo-data -u demo@test.com)

curl -k -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $token" -d '{
  "metadata": {
    "title": "Sample Dataset",
    "description": "This is a sample dataset."
  }
}' https://localhost:5000/api/datasets
EOF

chmod +x datasets/sample_data.sh

# install the repository
./run.sh install
./run.sh services setup
./run.sh invenio files location create --default default s3://default

echo "Sample repository has been created successfully."
echo "To run it, use the following command:"
echo
echo "  cd sample_repository"
echo "  ./run.sh run"
echo
echo
echo "To load sample data, call the following while the repository is running:"
echo
echo "  cd sample_repository"
echo "  ./datasets/sample_data.sh"
echo
echo "They you can visit https://127.0.0.1:5000/"
echo "Log in as user demo@test.com with password demodemo"
echo "and visit https://127.0.0.1:5000/api/user/datasets to see your sample record"
