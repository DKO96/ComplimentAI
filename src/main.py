import time
import threading
from emotiondetection.emotionDetection import EmotionDetector
from chatbot.complimentBot import ComplimentBot

class ComplimentAI:
  def __init__(self):
    self.emotion_detector = EmotionDetector()
    self.compliment_bot = ComplimentBot()
    
  def run(self):
    emotion_thread = threading.Thread(target=self.emotion_detector.emotionDetector) 
    emotion_thread.start()

    compliment_thread = threading.Thread(target=lambda: self.compliment_bot.complimentUser(self.emotion_detector))
    compliment_thread.start()


def main():
  compliment_ai = ComplimentAI()
  compliment_ai.run()


if __name__ == "__main__":
  main()



