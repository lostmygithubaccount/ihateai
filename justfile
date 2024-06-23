# justfile

# load environment variables
set dotenv-load

# variables

# aliases
alias fmt:=format

# list justfile recipes
default:
    just --list

# build
build:
    just clean-dist
    @python -m build

# setup
setup:
    @pip install uv
    @uv pip install -r dev-requirements.txt
    just install

# install
install:
    @uv pip install -e .

# format
format:
    @ruff format .

# publish-test
release-test:
    just build
    @twine upload --repository testpypi dist/* -u __token__ -p ${PYPI_TEST_TOKEN}

# publish
release:
    just build
    @twine upload dist/* -u __token__ -p ${PYPI_TOKEN}

# clean dist
clean-dist:
    @rm -rf dist

# clean all
clean-all:
    just clean-dist

# open
open:
    @open apps/testing_interface.html

# tensors
tensors:
    @tensorboard --logdir=lightning_logs
