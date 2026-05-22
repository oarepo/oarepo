#!/usr/bin/env bash
# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 CESNET z.s.p.o.
# OARepo is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.
#
# Local equivalent of .github/workflows/repository-generation-test.yaml.
# All dependencies (Python, Node, pnpm, uv, gh) must already be installed.
# Modify the variables in the Configuration section below, then run the script.

set -euo pipefail

# ==============================================================================
# Configuration – edit these before running
# ==============================================================================

PYTHON_VERSION="3.14"

# Git ref (branch or tag) for the oarepo tools repo
OAREPO_REF="main"

# SHA or branch name for oarepo-app; leave empty to use the default from the template
OAREPO_APP_REF="temporary-14.2.1b10.dev7-2.rdm.14.0.0b10.dev7"

APP_TEMPLATE="https://github.com/oarepo/nrp-app-copier"
APP_TEMPLATE_VERSION="rdm-14"

# MODEL_TEMPLATE and MODEL_TEMPLATE_VERSION are exported and picked up by repository_runner.sh
export MODEL_TEMPLATE="https://github.com/oarepo/nrp-model-copier"
export MODEL_TEMPLATE_VERSION="rdm-14"

# Directory that will be created to hold the cloned oarepo repo and testrepo.
# Must not exist yet (or be empty).
WORK_DIR="./oarepo-test-workspace"

# ==============================================================================
# Helpers
# ==============================================================================

step() { echo; echo "===> $*"; }

# ==============================================================================
# Checkout oarepo (provides the workspace; install_dependencies is skipped
# because all deps are assumed to be present locally)
# ==============================================================================

if [ -d "$WORK_DIR" ]; then
  echo "Error: $WORK_DIR already exists, removing it..."
  rm -rf "$WORK_DIR"
fi

step "Checkout oarepo/oarepo @ ${OAREPO_REF}"
gh repo clone oarepo/oarepo "$WORK_DIR" -- --branch "$OAREPO_REF" --depth 1
cd "$WORK_DIR"

# ==============================================================================
# Display environment info
# ==============================================================================

step "Environment info"
echo "Python version: $(python${PYTHON_VERSION} --version)"
echo "Node version:   $(node --version)"
echo "pnpm version:   $(pnpm --version)"
echo "uv version:     $(uv --version)"
echo ""
echo "App template:         $APP_TEMPLATE"
echo "App template version: $APP_TEMPLATE_VERSION"
echo "Model template:       $MODEL_TEMPLATE"
echo "Model template version: $MODEL_TEMPLATE_VERSION"
echo "OARepo ref:           $OAREPO_REF"
echo "OARepo app ref:       ${OAREPO_APP_REF:-(not set)}"

# ==============================================================================
# Download repository_installer.sh (as a user would)
# ==============================================================================

step "Downloading repository_installer.sh"
curl -o repository_installer.sh \
  "https://raw.githubusercontent.com/oarepo/oarepo/${OAREPO_REF}/tools/repository_installer.sh"
chmod +x repository_installer.sh

# ==============================================================================
# Create test repository
# ==============================================================================

step "Creating test repository"
printf '%s\n' \
  "repository_name: testrepo" \
  "repository_human_name: Test Repository" \
  "repository_description: Integration test repository" \
  "languages: cs" > repo_config.yaml

bash repository_installer.sh \
  --python "python${PYTHON_VERSION}" \
  --template "$APP_TEMPLATE" \
  --version "$APP_TEMPLATE_VERSION" \
  --config repo_config.yaml \
  testrepo

# If OAREPO_APP_REF is set, pin oarepo-app to the specified branch/SHA
if [ -n "$OAREPO_APP_REF" ]; then
  if ! grep -q "\[tool.uv.sources\]" testrepo/pyproject.toml; then
    echo "" >> testrepo/pyproject.toml
    echo "" >> testrepo/pyproject.toml
    echo "[tool.uv.sources]" >> testrepo/pyproject.toml
  fi
  # Determine whether OAREPO_APP_REF is a branch name or a commit SHA
  if gh api "repos/oarepo/oarepo-app/branches/${OAREPO_APP_REF}" --silent 2>/dev/null; then
    OAREPO_APP_REF_KEY="branch"
  else
    OAREPO_APP_REF_KEY="rev"
  fi
  # Insert the source entry after [tool.uv.sources] – awk avoids BSD/GNU sed differences
  awk \
    -v key="$OAREPO_APP_REF_KEY" \
    -v ref="$OAREPO_APP_REF" \
    '/^\[tool\.uv\.sources\]/ { print; print "oarepo-app = { git = \"https://github.com/oarepo/oarepo-app\", " key " = \"" ref "\" }"; next } { print }' \
    testrepo/pyproject.toml > testrepo/pyproject.toml.tmp
  mv testrepo/pyproject.toml.tmp testrepo/pyproject.toml
fi

# ==============================================================================
# Create all models
# ==============================================================================

step "Creating models"
cd testrepo

cat > model_ccmm.yaml << 'EOF'
model_name: ccmm_model
model_human_name: CCMM Model
model_description: Test model using Czech Core Metadata Model
base_model: ccmm
EOF

cat > model_rdm_complete.yaml << 'EOF'
model_name: rdm_complete_model
model_human_name: Complete RDM Model
model_description: Test model using Complete RDM preset
base_model: rdm_complete
EOF

cat > model_rdm_basic.yaml << 'EOF'
model_name: rdm_basic_model
model_human_name: Basic RDM Model
model_description: Test model using Basic RDM preset
base_model: rdm_basic
EOF

cat > model_rdm_minimal.yaml << 'EOF'
model_name: rdm_minimal_model
model_human_name: Minimal RDM Model
model_description: Test model using Minimal RDM preset
base_model: rdm_minimal
EOF

cat > model_empty.yaml << 'EOF'
model_name: empty_model
model_human_name: Empty Model
model_description: Test model using Empty preset
base_model: empty
EOF

# Create each model (passing --data-file as extra arg)
# TODO: use just --data-file once https://github.com/oarepo/oarepo/pull/214 is merged
echo "Creating CCMM model..."
./run.sh model create ccmm_model model_ccmm.yaml --data-file model_ccmm.yaml

echo "Creating Complete RDM model..."
./run.sh model create rdm_complete_model model_rdm_complete.yaml --data-file model_rdm_complete.yaml

echo "Creating Basic RDM model..."
./run.sh model create rdm_basic_model model_rdm_basic.yaml --data-file model_rdm_basic.yaml

echo "Creating Minimal RDM model..."
./run.sh model create rdm_minimal_model model_rdm_minimal.yaml --data-file model_rdm_minimal.yaml

echo "Creating Empty model..."
./run.sh model create empty_model model_empty.yaml --data-file model_empty.yaml

# ==============================================================================
# Show repository structure
# ==============================================================================

step "Repository structure"
ls -la
echo ""
echo "=== Models created ==="
ls -la models/ 2>/dev/null || ls -la */model.py 2>/dev/null || echo "No models directory found"
echo ""
echo "=== pyproject.toml entry points ==="
grep -A 20 '\[project.entry-points' pyproject.toml || true

# ==============================================================================
# Install repository
# ==============================================================================

step "Installing repository"
./run.sh install

# ==============================================================================
# Verify installation
# ==============================================================================

step "Verifying installation"
echo "=== Checking virtual environment ==="
test -d .venv && echo "Virtual environment exists" || (echo "Virtual environment missing!" && exit 1)

echo ""
echo "=== Checking installed packages ==="
.venv/bin/pip list | grep -E "(oarepo|invenio)" | head -20

echo ""
echo "=== Repository info ==="
./run.sh info

# ==============================================================================
# Setup services
# ==============================================================================

step "Setting up services"
./run.sh services setup

# ==============================================================================
# Run repository (smoke-test: verify the app loads without crashing)
# ==============================================================================

step "Running repository (smoke test)"
./run.sh run &
curl -skf --retry 10 --retry-connrefused --retry-delay 3 --retry-max-time 60 \
  https://localhost:5000/ && echo "Repository is running"

# Release uv cache lock held by background processes
pkill -f "uv run"  || true
pkill -f "invenio" || true
pkill -f "celery"  || true
sleep 2

step "Done"
