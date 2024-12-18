#!/usr/bin/env bash

# set autograder environment variables
cd /autograder/source
source config.sh

# Install Python
add-apt-repository -y ppa:deadsnakes/ppa
apt-get update
apt-get install -y python${INSTALL_PYTHON_V}-venv jq

# Virtual environment
python${INSTALL_PYTHON_V} -m venv .venv
source .venv/bin/activate
pip install --upgrade pip

# Install libraries
pip install git+https://github.com/JMU-CS/jmu_pytest_utils.git
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi
