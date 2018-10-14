#!/bin/bash
set -ex

# collect posargs
envbindir=$1
toxinidir=$2

# purge previous build artifacts
rm -rf ./dist

# install package dependencies
poetry install -v -E services

# build and install actual package
poetry build -f wheel

pkg_name=$(ls ./dist | grep .whl)
${envbindir}/pip install -U ${toxinidir}/dist/${pkg_name}
