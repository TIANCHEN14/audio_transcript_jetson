import sounddevice as sd
import numpy as np
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import torchaudio
import torch
import queue
from threading import Thread

audio_queue = queue.Queue()

# record function
def record_audio(sample_rate = 16000 , channels = 1, duration = 10):
    
    # record audio for 10 second
    # threads function
    while True:
        recording = sd.rec(int(sample_rate * duration) , sample_rate, channels = channels)
        sd.wait()
        audio_queue.put(recording.squeeze())
        
# transcrip function
def transcribe_audio(model, processor):
    
    # contiunes check to get audio from queue to transcribe it
    while True:

        # get array from audio queue
        audio_array = audio_queue.get()

        # error handling
        if audio_array is None:
            break

        # use huggingface library for transcribe
        inputs = processor(audio_array, sample_rate = 16000 , return_tensors = 'pt').input_features
        inputs = inputs.to("cuda")

        # whisper
        with torch.no_grad():
            output_ids = model.generate(inputs)

        trasncible_text = processor.batch_decode(output_ids, skip_speical_tokens = True)

        print("Transcription : " , trasncible_text[0])

# main functions
 
# define models and processors
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-medium.en").to('cuda')
processor = WhisperProcessor.from_pretrained("openai/whisper-medium.en")

# define threads
record_thread = Thread(target = record_audio)
transcribe_thread = Thread(target = transcribe_audio, args = (model, processor))

# start the thread
record_thread.start()
transcribe_thread.start()

# join the threads when it is done
record_thread.join()
transcribe_thread.join()


