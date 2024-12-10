#!/usr/bin/env bash

V=3.12

# Install Python
add-apt-repository -y ppa:deadsnakes/ppa
apt-get update
apt-get install -y python${V}-venv jq

# Virtual environment
cd /autograder/source
python${V} -m venv .venv
source .venv/bin/activate
pip install --upgrade pip

# Install libraries
pip install git+https://github.com/JMU-CS/jmu_pytest_utils.git
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi
