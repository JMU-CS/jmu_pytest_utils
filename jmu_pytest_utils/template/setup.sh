#!/usr/bin/env bash

# Set autograder environment variables
cd /autograder/source
dos2unix config.sh
source config.sh

# Install Python
add-apt-repository -y ppa:deadsnakes/ppa
apt-get update
apt-get install -y python${INSTALL_PYTHON_V}-venv
apt-get install -y jq

# Virtual environment
python${INSTALL_PYTHON_V} -m venv .venv
source .venv/bin/activate
pip install --upgrade pip

# Install libraries
pip install git+https://github.com/JMU-CS/jmu_pytest_utils.git@v1.7.2
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

# Pytest settings
if [ ! -f "pytest.ini" ]; then
    cp .venv/lib/python*/site-packages/jmu_pytest_utils/template/pytest.ini .
fi

# Additional steps
if [ -f "postsetup.sh" ]; then
    dos2unix postsetup.sh
    source postsetup.sh
fi
