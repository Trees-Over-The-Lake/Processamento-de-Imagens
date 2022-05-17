import PySimpleGUI as sg
import os

from frontend.utils import *

from backend import classifier
from frontend.screens import menu

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
        # Layout da tela para o usuário
        layout = menu.layout_tela
        
        # Criando a janela
        window = sg.Window('Reconhecimento de Tumores', layout, resizable=False, font=('Helvetica', 16))

        # Eventos ocorridos
        while self.loop:
            event, values = window.read()
            print(values)

            # Sair da aplicação
            if event == sg.WIN_CLOSED: 
                self.loop = False
                break
            
            # Selecionar os arquivos do disco
            elif event == menu.keys.ABRIR_PASTA_BIRADS_KEY:
                # Validação da entrada
                print('entrei')
                self.modelo.set_images_dir(values[menu.keys.ABRIR_PASTA_BIRADS_KEY])

            
            # Treinar modelo
            elif event == menu.keys.TREINAR_MODELO_KEY:
                self.modelo.set_images_dir(values[menu.keys.ABRIR_PASTA_BIRADS_KEY])
                self.modelo.split_train_test()
                self.modelo.train_model()
            
            # Prever imagem única
            elif event == menu.keys.PREVER_IMAGEM_KEY:
                print('PREVER_IMAGEM_KEY')
            
            # Prever múltiplas imagens
            elif event == menu.keys.PREVER_IMAGENS_KEY:
                print('PREVER_IMAGENS_KEY')
            
            # Cortar e prever imagem
            elif event == menu.keys.CORTAR_E_PREVER_IMAGEM_KEY:
                print('CORTAR_E_PREVER_IMAGEM_KEY')
            
            # Obter métricas de classificação do modelo
            elif event == menu.keys.OBTER_METRICAS_MODELO_KEY:
                print('OBTER_METRICAS_MODELO_KEY')
            
            # Abrir opções avançadas
            elif event == menu.keys.OPCOES_AVANCADAS_KEY:
                print('OPCOES_AVANCADAS_KEY')
            
            # Opções avançadas
            elif event == menu.keys.AJUDA_KEY:
                print('AJUDA_KEY')
            
            # Creditos da aplicação
            elif event == menu.keys.CREDITOS_KEY:
                print('CREDITOS_KEY')

        # Finalizar aplicação e fechar a janela
        window.close()