import os
import time
import openai
import pathlib
import json
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer
from gtts import gTTS

client = openai.OpenAI()

speech_path = pathlib.Path(__file__).parent / "reply.mp3"
config_path = pathlib.Path(__file__).parent / "config.json"

with open (config_path, "r") as config_file:
  config = json.load(config_file)

while True:
  user_input = input()
  if user_input == "quit":
    break

  emotion = "surprised"

  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": " ".join(config["assistant"][emotion])},
      {"role": "user", "content": " ".join(config["user"][emotion])}
    ],
    max_tokens=150,
    temperature=0.7,
  )

  reply = response.choices[0].message.content
  print(reply)

  audio = gTTS(text=reply, lang='en', tld='ca', slow=False)
  audio.save("reply.mp3")

  mixer.init()
  mixer.music.load(speech_path)
  mixer.music.play()
  while mixer.music.get_busy():
    time.sleep(0.1)






