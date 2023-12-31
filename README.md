# Compliment AI

## Description
Compliment AI detects facial emotions in real-time through a webcam and generates a compliment for the user to brighten their day. The application identifies faces through OpenCV's Haar cascade object detection. Various emotions including angry, happy, neutral, sad, and surprised are detected from the faces using a CNN built in Pytorch. The CNN model is trained on the FER2013 dataset, ensuring a broad understanding of facial expressions. Once an emotion is detected, the OpenAI API generates a tailored compliment, adding a positive spin to the user's day!

## Features
- **Real-time Emotion Detection**: Detects and interprets facial emotions through the webcam.
- **Dynamic Compliment Generation**: Generates compliments based on the detected emotion using OpenAI's API.

## Technologies Used
- **Language**: Python
- **Frameworks/Libraries**:
  - PyTorch 
  - OpenAI
  - OpenCV (cv2)
  - gTTS (Google Text-to-Speech)
  - PySimpleGUI

## Installation
1. Clone the repository to your local machine.
2. Install the necessary dependencies by running `pip install -r requirements.txt`.
3. Set your OpenAI API key in your environment: `export OPENAI_API_KEY="your_key_here"`.

## Usage
After installing the requirements and setting up your API key:
1. Run `main.py`.
2. Click on the "Generate" button to start detecting your facial emotion and receive a personalized compliment based on the detected emotion.

