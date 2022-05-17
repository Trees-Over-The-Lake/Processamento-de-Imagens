import PySimpleGUI as sg

from frontend.utils import *

from backend import classifier
from frontend.screens import menu
from frontend.screens import advanced_options

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
                metricas = self.modelo.get_runtime_metrics()
                            
                texto_final = ''
                # Formatar o print                
                for key in metricas:
                    texto_final += f"{key}: {metricas[key]}\n\n"
                
                sg.popup_ok(texto_final, title='Métricas de Avaliação do Modelo', font=('Helvetica', 16))
            
            # Abrir opções avançadas
            elif event == menu.keys.OPCOES_AVANCADAS_KEY:
                acessar_opcoes = sg.popup_ok_cancel('Opções avançadas podem afetar o desempenho do modelo!\nUse com cautela!', title='Aviso!', font=('Helvetica', 16))
                
                if acessar_opcoes == 'OK':
                    layout_opcoes_avancadas = advanced_options.AdvancedOptions()
                    layout_opcoes_avancadas.construir_tela_opcoes_avancadas(self.modelo)
            
            # Opções avançadas
            elif event == menu.keys.AJUDA_KEY:
                print('AJUDA_KEY')
            
            # Créditos da aplicação
            elif event == menu.keys.CREDITOS_KEY:
                print('CREDITOS_KEY')

        # Finalizar aplicação e fechar a janela
        window.close()
        