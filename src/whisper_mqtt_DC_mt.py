import sounddevice as sd
import numpy as np
from transformers import WhisperProcessor, WhisperForConditionalGeneration
#import torchaudio
from threading import Thread
import queue
import torch
#import keyboard
import paho.mqtt.client as mqtt

# define audio queue
audio_queue = queue.Queue()

# transcribing audio that is 
def transcript_audio(client, topic, model, processor):
    # transcrible audio using whisper model
    #print("transcribe function called")
	while True:
		audio_array = audio_queue.get()
		
		# error check maker sure it is not getting empty frame
		if audio_array is None:
			break

    		# MAKE SURE THE DATA IS IN AN 1D ARRAY BEFORE PASS IT IN
		inputs = processor(audio_array , sampling_rate = 16000 , return_tensors = 'pt').input_features
		inputs = inputs.to('cuda')
    
    		#print("start to transcrpting")
    
    		# generated new ids base on the inputs
		with torch.no_grad():
			output_ids = model.generate(inputs)
    
   	 	# Decode tokens
		output_text = processor.batch_decode(output_ids, skip_special_tokens = True)
    			
   		# push it though MQTT client
		print("Transcript Start : ")
		client.publish(topic , output_text[0])
		print(output_text[0])

def record_audio(duration = 5 , channels = 1 , sampling_rate = 16000):
    
    	
    	# Start the stream 
	while True:
		recording = sd.rec(int(sampling_rate * duration) , sampling_rate , channels = channels)
		sd.wait()
		audio_queue.put(recording.squeeze())

def main():
	# prepare MQTT client servers
	broker_address = "SHR1716.shracing.com"
	port = 1883

	# define topic
	#topic = "NASCAR_Radio"
	topic = input("What is the car number you are listening?")

	# MQTT clients creation
	client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
	client.connect(broker_address , port)

	model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small.en").to('cuda')
	processor = WhisperProcessor.from_pretrained("openai/whisper-small.en")

	sd.default.samplerate = 16000
	sd.default.device = "pulse"


	# setup multi threads
	recording_thread = Thread(target = record_audio)
	transcript_thread = Thread(target = transcript_audio, args = (client, topic, model, processor))

	# stare the thread
	recording_thread.start()
	transcript_thread.start()
	
	# Join the thread for safty
	recording_thread.join()
	transcript_thread.join()


if __name__ == "__main__":
	main()
