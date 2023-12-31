import pathlib
import cv2
import torch
import torchvision.transforms as transforms

from .emotionCNN import CNN

class EmotionDetector:
  def __init__(self, frame_emotion, stop_flag):
    # directory path
    directory = pathlib.Path(__file__).parent
    model_path = directory / "model.pt"
    haar_path = directory / "haarcascade_frontalface_default.xml"

    # initialize classifier
    self.N_CLASSES = 5
    self.IMAGE_SIZE = 48
    self.label_map = {0:"angry", 1:"happy", 2:"neutral", 3:"sad", 4:"surprised"}

    # model setup
    self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    self.model = CNN(self.N_CLASSES).to(self.device)
    self.model.load_state_dict(torch.load(model_path))

    # face detection setup
    self.face_cascade = cv2.CascadeClassifier(str(haar_path))
    cam_res = (1920, 1080)
    self.cap = cv2.VideoCapture(0)
    self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, cam_res[0])
    self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_res[1])

    self.emotion = ""
    self.frame_emotion = frame_emotion
    self.stop_flag = stop_flag


  def preprocess(self, image):
    transform = transforms.Compose([transforms.ToTensor()])
    TENSOR_IMAGE = transform(image)
    return TENSOR_IMAGE

  def emotionDetector(self):
    while True:
      ret, frame = self.cap.read()
      if not ret or self.stop_flag.is_set():
        break

      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=20, minSize=(90,90))

      for (x, y, w, h) in faces:
        roi = gray[y:y+h, x:x+w]
        roi = cv2.resize(roi, (self.IMAGE_SIZE, self.IMAGE_SIZE))
        roi = self.preprocess(roi).unsqueeze(0)
        roi = roi.to(self.device)

        with torch.no_grad():
          self.model.eval()
          output = self.model(roi)
          _, preds = torch.max(output, dim=1)
          self.emotion = self.label_map[preds.item()]

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, self.emotion, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

      self.frame_emotion.put((frame, self.emotion))
    
      if cv2.waitKey(1) & 0xFF == ord('q'):
        self.stop_flag = True
        break
    
    self.cap.release()
    cv2.destroyAllWindows()




