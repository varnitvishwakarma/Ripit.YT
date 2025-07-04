#!/bin/bash

# Update apt and install FFmpeg
apt-get update
apt-get install -y ffmpeg

# Install Python dependencies
pip install -r requirements.txt
