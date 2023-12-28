import os
import numpy as np
import cv2
import torch

class ComplimentAI:
  def __init__(self):
    pass






def main():
  # component paths 
  cnn_path = os.path.join("model/model.pt")
  face_rec_path = os.path.join("facerecognition/haarcascade_frontalface_default.xml")
  chatbot_path = os.path.join("chatbot/complimentbot.py") 

  compAI = ComplimentAI()

  pass


if __name__ == "__main__":
  main()



