import sounddevice as sd

# list all avaliable audio device
device = sd.query_devices()
print(device)
