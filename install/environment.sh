#!/bin/bash

if [ -n venv ] ; then
    # Create a virtual environment
    python3 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate
