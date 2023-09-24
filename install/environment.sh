#!/bin/bash

if [ -n venv ] ; then
    # Create a virtual environment
    python3 -m venv venv
    echo Created virtual environment

    # Activate the virtual environment
    source venv/bin/activate
    echo Activated virtual environment
fi