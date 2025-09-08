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

# prepare sample Copier configs
cat <<EOF >initial_repository_config.yaml
languages: 'cs'
repository_name: 'sample_repository'
repository_description: 'Sample Repository'
repository_human_name: Sample Repository
EOF

cat <<EOF >initial_model_config.yaml
model_name: 'datasets'
model_human_name: 'Datasets'
model_description: 'A generic dataset model'
EOF

chmod +x repository_installer.sh
./repository_installer.sh --config initial_repository_config.yaml sample_repository

cd sample_repository

cat <<'EOF' >fixtures/sample_data.sh
./run.sh invenio users create -a -c "demo@test.com" --password "demodemo" --profile '{"full_name": "Demo user"}'

token=$(./run.sh invenio tokens create -n demo-data -u demo@test.com)

curl -k -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $token" -d '{
  "metadata": {
    "title": "Sample Dataset",
    "description": "This is a sample dataset."
  }
}' https://127.0.0.1:5000/api/datasets
EOF

chmod +x fixtures/sample_data.sh

# install the repository
./run.sh install
./run.sh services setup
./run.sh invenio files location create --default default s3://default

echo "Sample repository has been created successfully."
echo "To run it, use the following command:"
echo
echo "  cd sample_repository"
echo
echo "  ./run.sh model create ../initial_model_config.yaml"
echo "  ./run.sh run"
echo
echo
echo "To load sample data, call the following while the repository is running:"
echo
echo "  ./fixtures/sample_data.sh"
echo
echo "Then you can visit https://127.0.0.1:5000/"
echo "Log in as user demo@test.com with password demodemo"
echo "and visit https://127.0.0.1:5000/api/user/datasets to see your sample record"
