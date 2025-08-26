#!/usr/bin/env bash

set -euo pipefail

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
repository_description: 'Sample Repository'
repository_human_name: Sample Repository
EOF

chmod +x repository_installer.sh
./repository_installer.sh --config initial_config.yaml sample_repository

cd sample_repository
./run.sh install
./run.sh services setup