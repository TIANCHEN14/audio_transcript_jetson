#!/bin/bash

# Audio Transcript Jetson Setup Guide

# Pre-requirements
echo "Starting setup for Jetson ORIN NANO (8GB) with Jetpack 6.0"

# Resource Monitor and Jetpack

# Check if pip is installed
echo "Checking for pip installation..."
if ! python3 -m pip --version &>/dev/null; then
    echo "pip not found, installing pip..."
    sudo apt install -y python3-pip
else
    echo "pip is already installed"
fi

# Install jtop
echo "Installing jtop..."
sudo pip3 install jetson-stats

# Mosquitto Client

echo "Installing mosquitto broker and clients..."
sudo apt install -y mosquitto mosquitto-clients

# Python setup

# Install PyTorch
echo "Setting up PyTorch..."
export TORCH_INSTALL=https://developer.download.nvidia.cn/compute/redist/jp/v60/pytorch/torch-2.4.0a0+07cecf4168.nv24.05.14710581-cp310-cp310-linux_aarch64.whl
python3 -m pip install --upgrade numpy
python3 -m pip install --no-cache $TORCH_INSTALL

# Install other libraries
echo "Installing additional Python libraries..."
python3 -m pip install transformers
python3 -m pip install paho-mqtt

# Install sounddevice and PortAudio library
echo "Installing PortAudio library and sounddevice..."
sudo apt-get update
sudo apt-get install -y libportaudio2 libportaudiocpp0 portaudio19-dev
python3 -m pip install sounddevice

echo "Setup completed successfully."


