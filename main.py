#!/usr/bin/env python
# coding: utf-8

# In[6]:


pip install pyaudio


# In[5]:


pip install vosk


# In[5]:


pip install llama-cpp-python --prefer-binary


# In[6]:


pip install cmake


# In[8]:


pip install llama-cpp-python


# In[23]:


import os
import pyaudio
from vosk import Model, KaldiRecognizer
import json  # Import the JSON module to parse the result

# Set the path to the model you downloaded
MODEL_PATH = "model"  # Replace with the actual model path

# Try loading the Vosk model
try:
    model = Model(MODEL_PATH)
    recognizer = KaldiRecognizer(model, 16000)  # 16000 is the sample rate
except Exception as e:
    print(f"Error loading model: {e}")
    exit(1)  # Exit the script if the model cannot be loaded

# Initialize PyAudio for microphone input
try:
    p = pyaudio.PyAudio()
except Exception as e:
    print(f"Error initializing microphone: {e}")
    exit(1)  # Exit if the microphone cannot be initialized

# Try opening the microphone stream
try:
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4000)
    stream.start_stream()
except Exception as e:
    print(f"Error opening microphone stream: {e}")
    exit(1)  # Exit if the microphone stream cannot be opened

print("Listening...")

# Continuously listen to the microphone and process audio
while True:
    try:
        data = stream.read(4000)  # Read the audio data in chunks of 4000 bytes
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()  # Get the recognized result (returns a JSON string)

            # Parse the JSON result to get the recognized text
            result_dict = json.loads(result)

            # Print the recognized text
            print(f"Recognized text: {result_dict['text']}")

    except Exception as e:
        print(f"Error during speech recognition: {e}")


# In[1]:


from llama_cpp import Llama

llm = Llama(model_path="D:/models/phi-2.gguf")


# In[ ]:


prompt = "You are a helpful dental clinic assistant. If someone asks about appointments, guide them. If they ask about parking, explain location."

while True:
    question = input("You: ")
    full_prompt = prompt + f"\nUser: {question}\nAssistant:"
    output = llm(full_prompt, max_tokens=150, stop=["User:"], echo=False)
    print("Assistant:", output['choices'][0]['text'].strip())

