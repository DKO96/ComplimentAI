import os
import time
import threading
import openai
import pathlib
import json
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer
from gtts import gTTS

class ComplimentBot():
  def __init__(self, compliment, generate, stop_flag):
    # openai token
    self.client = openai.OpenAI()

    # speech output path 
    self.speech_path = pathlib.Path(__file__).parent.parent / "reply.mp3"
    self.compliment = compliment

    # initialize tts
    mixer.init()

    # load assistant config 
    config_path = pathlib.Path(__file__).parent / "config.json"
    with open (config_path, "r") as config_file:
      self.config = json.load(config_file)

    # lock for synchronizing
    self.emotion_lock = threading.Lock()
    self.generate = generate
    self.stop_flag = stop_flag

  def complimentUser(self, emotion_detector):
    while True:
      if self.stop_flag.is_set():
        break

      if self.generate.is_set():
        with self.emotion_lock:
          emotion = emotion_detector.emotion
          response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
              {"role": "system", "content": " ".join(self.config["assistant"][emotion])},
              {"role": "user", "content": " ".join(self.config["user"][emotion])}
            ],
            max_tokens=100,
            temperature=1.0,
          )
          reply = response.choices[0].message.content
          self.compliment.put(reply)

        audio = gTTS(text=reply, lang='en', tld='ca', slow=False)
        audio.save("reply.mp3")

        mixer.music.load(self.speech_path)
        mixer.music.play()
        while mixer.music.get_busy():
          time.sleep(0.1)

        self.generate.clear()

      time.sleep(0.075)





