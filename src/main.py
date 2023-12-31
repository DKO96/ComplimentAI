import cv2
import threading
import queue
import PySimpleGUI as sg
from emotiondetection.emotionDetection import EmotionDetector
from chatbot.complimentBot import ComplimentBot

class ComplimentAI:
  def __init__(self):
    self.frame_emotion = queue.Queue()
    self.compliment = queue.Queue()
    self.generate = threading.Event()
    self.stop_flag = threading.Event()

    self.emotion_detector = EmotionDetector(self.frame_emotion, self.stop_flag)
    self.compliment_bot = ComplimentBot(self.compliment, self.generate, self.stop_flag)
    
  def run(self):
    emotion_thread = threading.Thread(target=self.emotion_detector.emotionDetector) 
    emotion_thread.start()

    compliment_thread = threading.Thread(target=lambda: 
                                         self.compliment_bot.complimentUser(self.emotion_detector))
    compliment_thread.start()
    

def main():
  compliment_ai = ComplimentAI()
  compliment_ai.run()

  # gui 
  width = 60
  layout = [
    [sg.Column([[sg.Image(filename="", key="-IMAGE-")]], justification='center', k='-COLUMN-')],
    [sg.Column([[sg.Text(key="-EMOTION-")]], justification='center', k='-COLUMN-')],
    [sg.Text('', size=(1, 1))],
    [sg.Column([[sg.Text(key="-COMPLIMENT-", size=(width, 6), justification='center', font=("Helvetica", 14))]],
                justification='center')],
    [sg.Text('', size=(1, 1))],
    [sg.Column([[sg.Button('Generate')]], justification='center')],
  ]
  window = sg.Window("Compliment AI", layout=layout, margins=(75, 55))

  while True:
    event, values = window.read(timeout=5)
    if event == sg.WIN_CLOSED:
      compliment_ai.stop_flag.set()
      break

    if event == "Generate":
      compliment_ai.generate.set()

    if not compliment_ai.frame_emotion.empty():
      frame, emotion = compliment_ai.frame_emotion.get()
      imgbytes = cv2.imencode(".png", frame)[1].tobytes()
      window["-IMAGE-"].update(data=imgbytes)
      window["-EMOTION-"].update(f"Emotion: {emotion}")

    if not compliment_ai.compliment.empty(): 
      compliment = compliment_ai.compliment.get()
      window["-COMPLIMENT-"].update(compliment)

  window.close()

if __name__ == "__main__":
  main()



