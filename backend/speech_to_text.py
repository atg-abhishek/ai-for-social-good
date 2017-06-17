
import json
from os.path import join, dirname
from watson_developer_cloud import SpeechToTextV1

speech_to_text = SpeechToTextV1(
    username='23d436aa-5ad1-4f18-b143-35298ff1836f',
    password='8h2CmnJumDb5',
    x_watson_learning_opt_out=False
)

filename = join(dirname(__file__), './Untitled.wav')


def call_speech_to_text_on_wav(wav_file_path):
	with open(wav_file_path, 'rb') as audio_file:
	    return json.dumps(speech_to_text.recognize(
	        	audio_file, content_type='audio/wav', timestamps=True,
	        	word_confidence=True),
	        	indent=2)