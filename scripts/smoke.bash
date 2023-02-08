#!/usr/bin/env bash

set -ex

PYVER=3

fd pycache -u | xargs rm -rf

tox -c tox.ini        \
  -e py${PYVER}flakes

tox --parallel -c tox.ini        \
  -e py${PYVER}       \
  -e py${PYVER}black  \
  -e py${PYVER}lint   \
  -e py${PYVER}mypy

tox -c tox-integration.ini  \
  -e py${PYVER}-generic

tox --parallel -c tox-integration.ini  \
  -e py${PYVER}-advanced     \
  -e py${PYVER}-cookies     \
  -e py${PYVER}-components     \
  -e py${PYVER}-hooks     \
  -e py${PYVER}-mqtt
