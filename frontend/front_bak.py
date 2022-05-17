import PySimpleGUI as sg
from frontend.screens import options_window

from frontend.utils import *

from frontend import explanation
from backend import classifier

# Class to define all functions to work the frontend
class GUI:
    def __init__(self, current_working_dir) -> None:
        self.current_working_dir = current_working_dir
        self.loop = True
        self.modelo = classifier.ImageClassifier()


    # Draw the GUI and hold it, until the user asks to exit
    def drawGUI(self):
        self.main_screen()

    # Drawing the drawTrainGUI
    def main_screen(self):
        layout = [  
                    [sg.Text('\tAplicativo de detecção de tumores em mamografias')],
                    [sg.Text('Escolha a porcentagem de dados disponível para treino: '), 
                    sg.Slider(range=(1,99), default_value=75, size=(20,15),
                    orientation='horizontal', key='-PORCENTAGEM_TREINAMENTO-')],
                    [sg.Text('Escolha quantos tons de cinza para o processamento: '), 
                    sg.Slider(range=(1,32), default_value=32, size=(20,15), key='-GREY_COLORS-', orientation='horizontal')],
                    [sg.Text('Escolha o arquivo que deseja abrir:')],
                    [sg.InputText(key='-FILE_PATH-'), sg.FolderBrowse(initial_folder=self.current_working_dir, key='-IMAGES_FOLDER-')],
                    [sg.Button('Treinar')]
                ]

        # Create the Window
        window = sg.Window('Treinamento das mamografias ', layout, resizable=False, font=('Helvetica', 16))

        # Event Loop to process "events" and get the "values" of the inputs
        while self.loop:
            event, values = window.read()

            if event == sg.WIN_CLOSED: 
                self.loop = False
                break
            elif event == 'Treinar':
                image_folder = values['-IMAGES_FOLDER-']
                grey_colors  = int(values['-GREY_COLORS-'])
                train_size   = int(values['-PORCENTAGEM_TREINAMENTO-'])
                
                print("Pasta carregada:", image_folder)
                
                accuracy, especificidade = classifier.runPrediction(train_size, image_folder, grey_colors)
                sg.Popup(f"Acurácia: {accuracy}", image='./metricas.png', title='Resultado Treinamento', font=('Helvetica', 16))
                    
                break

        window.close()