import concurrent.futures
import PySimpleGUI as sg

from frontend.image import *
from backend import classifier

# Class to define all functions to work the frontend
class GUI:
    def __init__(self, current_working_dir) -> None:
        self.current_working_dir = current_working_dir
        self.loop = True

    # Draw the GUI and hold it, until the user ask to exit
    def drawGUI(self):
        self.startScreen()
        self.drawTrainGUI()

    # Drawing the drawTrainGUI
    def drawTrainGUI(self):
        # All the stuff inside your window.
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
        
    def startScreen(self):
        # Elementos da tela de predição

        topbar = [
                    [sg.Text('Reconhecimento Automático de Densidade da Mama',font=("Helvetica 17 bold"), size=(None, 3))],
                    [sg.Image(source="frontend/assets/logo-puc-minas.png")]
        ]
        
        centered_elements = [
                    [sg.Button('Como funciona?', border_width=4, key="__help"), sg.Button('Opções avançadas', border_width=4, key="__options")],
                    [sg.Button('Iniciar', border_width=4, key="__start")],
        ]

        layout = [
                topbar,
                [sg.VPush()],
                [sg.Push(), sg.Column(centered_elements, element_justification='c'), sg.Push()],
                [sg.VPush()]
        ]

        window = sg.Window('Predição das Mamografias', layout, resizable=False, font=('Helvetica', 16), auto_size_text=True)
        
        while self.loop:
            event, values = window.read()
            
            if event == sg.WIN_CLOSED: 
                self.loop = False
                break
                
            elif event == '__start':
                window.close()
                break

            elif event == '__help':
                text = [
                    [sg.Text("TESTE")]
                ]

                window = sg.Window("Ajuda", text)
                break

            
            elif event == '__options':
                sg.popup_ok_cancel('Tem certeza que deseja configurar as opções avançadas?', title='Aviso', font=('Helvetica', 16))
                window.close()
                break
            
            print(values)