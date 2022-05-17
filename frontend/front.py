import PySimpleGUI as sg
import os
import enum

from frontend.utils import *

from backend import classifier
from frontend.screens import menu
from frontend.screens import advanced_options

# Tristate -> Consistência das métricas na tela
class ConsistenciaMetricas(enum.Enum):
    nullState = 0,
    consistentState = 1,
    inconsistentState = 2

# Class to define all functions to work the frontend
class GUI:
    # Tristate -> Consistência das métricas na tela
    __consistencia_metricas: ConsistenciaMetricas
    
    def __init__(self, current_working_dir) -> None:
        self.current_working_dir = current_working_dir
        self.loop = True
        self.modelo = classifier.ImageClassifier()
        
        
        # Ao iniciar a aplicação não existe nenhum dado
        self.__consistencia_metricas = ConsistenciaMetricas.nullState


    # Draw the GUI and hold it, until the user asks to exit
    def drawGUI(self):
        self.main_screen()

    # Drawing the drawTrainGUI
    def main_screen(self):
        # Layout da tela para o usuário
        layout = menu.layout_tela
        layout_opcoes_avancadas: advanced_options.AdvancedOptions
        
        # Criando a janela
        window = sg.Window('Reconhecimento de Tumores', layout, resizable=False, font=('Helvetica', 16))

        # Eventos ocorridos
        while self.loop:
            event, values = window.read()

            # Sair da aplicação
            if event == sg.WIN_CLOSED: 
                self.loop = False
                break
            
            # Selecionar os arquivos do disco
            elif event == menu.keys.ABRIR_PASTA_BIRADS_KEY:
                # Validação da entrada
                self.modelo.set_images_dir(values[menu.keys.ABRIR_PASTA_BIRADS_KEY])
                del values[menu.keys.ABRIR_PASTA_BIRADS_BUTTON_TEXT]

            
            # Treinar modelo
            elif event == menu.keys.TREINAR_MODELO_KEY:
                self.modelo.split_train_test()
                self.modelo.train_model()
                
                # Sempre que treinar o modelo tornar os valores de métricas da tela para inconsistentes
                self.__consistencia_metricas = ConsistenciaMetricas.inconsistentState
            
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
                layout_opcoes_avancadas = advanced_options.AdvancedOptions()
                layout_opcoes_avancadas.construir_tela_opcoes_avancadas(self.modelo)
            
            # Opções avançadas
            elif event == menu.keys.AJUDA_KEY:
                print('AJUDA_KEY')
            
            # Creditos da aplicação
            elif event == menu.keys.CREDITOS_KEY:
                print('CREDITOS_KEY')

            # Atualizar métricas do app para todos
            # if self.__consistencia_metricas == ConsistenciaMetricas.inconsistentState:
            #     acuracia, especificidade = self.modelo.get_prediction_metrics()
                
            #     print(acuracia, especificidade)
                
            #     # Todos os dados da tela foram atualizados com sucesso
            #     self.__consistencia_metricas = ConsistenciaMetricas.consistentState

        # Finalizar aplicação e fechar a janela
        window.close()
        