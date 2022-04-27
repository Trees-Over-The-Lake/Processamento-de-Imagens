import PySimpleGUI as sg

from frontend.image import *

# Add a touch of color
sg.theme('DarkAmber')  

def drawGUI(current_working_dir, supported_types):
    # All the stuff inside your window.
    layout = [  [sg.Text('Aplicativo de detecção de tumores em mamografias')],
                [sg.Text('Escolha o arquivo que deseja abrir:')],
                [sg.InputText(key='-FILE_PATH-'), sg.FileBrowse(initial_folder=current_working_dir, file_types=supported_types)],
                [sg.Button('Ok')] ]

    # Create the Window
    window = sg.Window('Mamografias ', layout)

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED: 
            break
        elif event == 'Ok':
            image_path = values['-FILE_PATH-']
            
            print("Imagem carregada:", image_path)
            
            showImage(image_path)

    window.close()