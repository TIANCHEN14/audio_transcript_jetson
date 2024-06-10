# Audio Transcript Jetson Setup Guide
When we setup an new Jetson ORIN NANO for live audio web scripting and transcription option please follow the following steps

## Pre-requirement
+ Nvidia jetson orin nano dev kit (8GB)
+ Jetpack 6.0

## Resource Monitor And Jetpack
We will install jtop first to make sure we have access the nvidia resource monitor

First we check see if pip installed
```
python3 -m pip --version
```
if not we will install it use 
```
sudo apt install python3-pip
```
Then we will install jtop
```
sudo pip3 install jetson-stats
sudo jtop
```
Sometime we might need to reboot the jetson in order to start the jtop services. After we open JTOP info page. If all cuda driver is missing we will need to install jetpack compontent
```
sudo apt update
sudo apt install jetpack
```


## Mosquitto Client
 Run following command to install mosquitto broker and client
 ```
 sudo apt install mosquitto
 sudo apt install mosquitto-clients
 ```

## Python setup
In order to run the script we will need to install following libraries
+ paho-mqtt
+ pytorch
+ transformer
+ huggingface-cli
+ numpy
+ sounddevice

We will install pytorch first since a lot of library will be depended on this library

[Nvidia offical guide](https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform/index.html#prereqs-install)

[Pytorch guide](https://pytorch.org/blog/running-pytorch-models-on-jetson-nano/#overview)

Note that when we use Nvidia offical guide it is use jp/v511 as default, We need to change the export path as
```
export TORCH_INSTALL=https://developer.download.nvidia.cn/compute/redist/jp/v60/pytorch/torch-2.4.0a0+07cecf4168.nv24.05.14710581-cp310-cp310-linux_aarch64.whl
```
After set the export path run following command to install pytorch
```
python3 -m pip install numpy
python3 -m pip install --no-cache $TORCH_INSTALL
```
After the install please check to make sure everything is properly installed before move on
```
python3
>>>import torch
>>>torch.get_device_name
'Orin'
```
The we can install the following library, remember to login into huggingface account after all the library done installing

```
python3 -m pip install transformers
python3 -m pip install paho-mqtt
```
Last piece will be the sounddevice. We will need to install PortAudio library on device and then install sounddevice
```
sudo apt-get update
sudo apt-get install libportaudio2 libportaudiocpp0 portaudio19-dev
python3 -m pip install sounddevice
```

## Pulse Audio sink loop setup
We use pulse audio to set up an sink loop so we can scrap the live system audio output
1. Install PulseAudio and related tools:
```
sudo apt-get install pulseaudio pavucontrol pulseaudio-utils
```
2. Load the virtual module 
```
pactl load-module module-null-sink sink_name=virtual_sink sink_properties=device.description=Virtual_Sink
pactl load-module module-loopback source=virtual_sink.monitor
```
3. Set default virtual sink
```
pactl set-default-sink virtual_sink
```
4. Edit Pulse Radio default config
```
sudo nano /etc/pulse/default.pa

### Load the virtual sink module
load-module module-null-sink sink_name=virtual_sink sink_properties=device.description=Virtual_Sink

### Load the loopback module for the virtual sink
load-module module-loopback source=virtual_sink.monitor

### Set the default sink to the virtual sink
set-default-sink virtual_sink
```

## Git Clone 
We will need to clone this repository on jetson local machine
```
git clone https://github.com/TIANCHEN14/audio_transcript_jetson.git
```