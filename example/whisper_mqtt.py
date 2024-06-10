import sounddevice as sd
import numpy as np
from transformers import WhisperProcessor, WhisperForConditionalGeneration
#import torchaudio
import torch
import paho.mqtt.client as mqtt

# transcribing audio that is 
def transcribe_audio(audio_array, model, processor):
    # transcrible audio using whisper model
    #print("transcribe function called")

    #print("Array shape : " , audio_array.shape)
    #print("Array type : " , audio_array.dtype)

    # MAKE SURE THE DATA IS IN AN 1D ARRAY BEFORE PASS IT IN
    inputs = processor(audio_array , sampling_rate = 16000 , return_tensors = 'pt').input_features
    inputs = inputs.to('cuda')
    
    #print("start to transcrpting")
    
    # generated new ids base on the inputs
    with torch.no_grad():
        output_ids = model.generate(inputs)
    
    # Decode tokens
    output_text = processor.batch_decode(output_ids, skip_special_tokens = True)
    
    return output_text[0]
    

def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    # Append the incoming audio data to the global list
    global audio_data
    audio_data.append(indata.copy())  

def record_audio(duration = 5 , model = None, processor = None):
    # define global variable for all audio samples
    global audio_data
    audio_data = []
    
    # define sampling rate
    sampling_rate = 16000
    channels = 1 # mono channels
    
    # Start the stream
    with sd.InputStream(callback=audio_callback, samplerate=sampling_rate, channels=channels):
        sd.sleep(duration * 1000)  # Sleep for the duration of the recording


    audio_array = np.concatenate(audio_data)
    audio_array = audio_array.squeeze()
    transcription = transcribe_audio(audio_array, model, processor)
    
    sd.wait()
    return transcription

    #return audio_array

# prepare MQTT client servers
broker_address = "192.168.1.223"
port = 1883

# define topic
topic = "NASCAR_Radio"

# MQTT clients creation
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.connect(broker_address , port)


model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small.en").to('cuda')
processor = WhisperProcessor.from_pretrained("openai/whisper-small.en")

sd.default.samplerate = 16000
sd.default.device = "pulse"


while True:
    print("Starting a new 10-second recording...")
    transcription = record_audio(5, model=model, processor=processor)
    # mqtt pubulish
    client.publish(topic , transcription)
    # print result
    print("Recording completed. Transcription:", transcription)
    print("Waiting for the next recording...")
    sd.sleep(10)  # Delay before the next recording
