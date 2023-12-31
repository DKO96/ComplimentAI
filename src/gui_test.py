import PySimpleGUI as sg
import textwrap
import cv2

def main():
  sg.theme("LightGreen")

  width = 100
  emotion = "happy"
  text = "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?"
  wrap_text = textwrap.fill(text, width)

  # Define the window layout
  layout = [
    [sg.Text('', size=(1, 1))],
    [sg.Column([[sg.Image(filename="", key="-IMAGE-")]], justification='center', k='-COLUMN-')],
    [sg.Column([[sg.Text(emotion)]], justification='center')],
    [sg.Text('', size=(1, 2))],
    [sg.Column([[sg.Text(wrap_text, size=(width, 10), justification='center')]], justification='center')],
    [sg.Column([[sg.Button('Generate')]], justification='center')],
  ]

  window = sg.Window("GUI Testing", layout=layout, margins=(75, 100))
  cam_res = (1920, 1080)
  cap = cv2.VideoCapture(0)
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, cam_res[0])
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_res[1])

  while True:
    event, values = window.read(timeout=20)
    if event == sg.WIN_CLOSED:
        break

    ret, frame = cap.read()
    if not ret:
       break

    imgbytes = cv2.imencode(".png", frame)[1].tobytes()
    window["-IMAGE-"].update(data=imgbytes)
    

  window.close()
  cap.release()


main()




