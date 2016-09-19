import pyaudio
import wave
import houndify
import sys
import time
import MontyAI as Monty

#houndify client keys
CLIENT_ID = "gKnfKJWW3bfGxlNReX17ow=="
CLIENT_KEY = "n9-dxiLzlonHpFivPWK2LqxuuDuM_vwTq1jXvAorxFMgDSnc8Od9VT-Xv_yI3F7f3B6pWkzKbn6ZmvLNImZstw=="


chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 4
WAVE_OUTPUT_FILENAME = "output-sing1.wav"
p = pyaudio.PyAudio()
stream = p.open(format = FORMAT,
	channels = CHANNELS,
	rate = RATE,
	input = True,
	frames_per_buffer = chunk)
all = []
for i in range(0, int(RATE / chunk * RECORD_SECONDS)):
	data = stream.read(chunk)
	all.append(data)
print("* done recording")
stream.close()
p.terminate()
len(data)
data = b"".join(all)
wf = wave.open(WAVE_OUTPUT_FILENAME, "wb")
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(data)
wf.close()

BUFFER_SIZE = 512
transcribed_text = ""
class MyListener(houndify.HoundListener):
	def onPartialTranscript(self, transcript):
#		print("Partial transcript: " + transcript)
		self.full_transcript = transcript
	def onFinalResponse(self, response):
#		print("Final response: " + str(response))
		return response
	def onTranslatedResponse(self, response):
		print("Translated response: " + response)
	def onError(self, err):
		print("ERROR")


client = houndify.StreamingHoundClient(CLIENT_ID, CLIENT_KEY, "test_user")
## Pretend we're at SoundHound HQ.  Set other fields as appropriate
client.setLocation(37.388309, -121.973968)
audio = wave.open(WAVE_OUTPUT_FILENAME)
client.setSampleRate(audio.getframerate())
samples = audio.readframes(BUFFER_SIZE)
finished = False
listener = MyListener()
client.start(listener)
while not finished:
	finished = client.fill(samples)
	time.sleep(0.032)     ## simulate real-time so we can see the partial transcripts
	samples = audio.readframes(BUFFER_SIZE)
	if len(samples) == 0:
		break
client.finish()


print("Transcript of audio:" + listener.full_transcript)

AI = Monty.MontyAI(listener.full_transcript)
print(AI.response)