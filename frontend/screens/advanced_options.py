import PySimpleGUI as sg
from frontend.screens.models import keys

from backend import classifier

class AdvancedOptions:
    __tela: sg.Window
    
    def _build_layout(self):
        layout_options = [
            [  
                sg.Text(keys.ADVANCED_OPTIONS_HELP_PORCENTAGEM_TREINO_BUTTON_TEXT),
                sg.Button(keys.ADVANCED_OPTIONS_GENERAL_HELP_BUTTON_TEXT, border_width=4, key=keys.ADVANCED_OPTIONS_HELP_PORCENTAGEM_TREINO_KEY),
            ],
            [
                sg.Text(keys.ADVANCED_OPTIONS_GAUSSIAN_MATRIX_BUTTON_TEXT),
                sg.Button(keys.ADVANCED_OPTIONS_GENERAL_HELP_BUTTON_TEXT, border_width=4, key=keys.ADVANCED_OPTIONS_GAUSSIAN_MATRIX_KEY),
                
            ],
            [
                sg.Text(keys.ADVANCED_OPTIONS_SHARPEN_BUTTON_TEXT),
                sg.Button(keys.ADVANCED_OPTIONS_GENERAL_HELP_BUTTON_TEXT, border_width=4, key=keys.ADVANCED_OPTIONS_SHARPEN_KEY),
                
            ],
            [
                sg.Text(keys.ADVANCED_OPTIONS_CONTRAST_TEXT_BUTTON),
                sg.Button(keys.ADVANCED_OPTIONS_GENERAL_HELP_BUTTON_TEXT, border_width=4, key=keys.ADVANCED_OPTIONS_CONTRAST_KEY),
            ],
            [
                sg.Text(keys.ADVANCED_OPTIONS_BRIGHTNESS_TEXT_BUTTON),
                sg.Button(keys.ADVANCED_OPTIONS_GENERAL_HELP_BUTTON_TEXT, border_width=4, key=keys.ADVANCED_OPTIONS_BRIGHTNESS_KEY),
            ],
            [
                sg.Text(keys.ADVANCED_OPTIONS_N_COLORS_TEXT_BUTTON),
                sg.Button(keys.ADVANCED_OPTIONS_GENERAL_HELP_BUTTON_TEXT, border_width=4, key=keys.ADVANCED_OPTIONS_N_COLORS_KEY),
            ],
            [sg.Button(keys.ADVANCED_OPTIONS_RESET_TEXT_BUTTON, border_width=4, key=keys.ADVANCED_OPTIONS_RESET_KEY)],
            [sg.Button(keys.ADVANCED_OPTIONS_CONFIRM_MODIFICATIONS_TEXT_BUTTON, border_width=4, key=keys.ADVANCED_OPTIONS_CONFIRM_MODIFICATIONS_KEY)]
        ]

        layout_sliders = [
            [sg.Slider(range=(1,99), size=(20,15), orientation='horizontal', key=keys.ADVANCED_OPTIONS_PORCENTAGEM_TREINAMENTO_SLIDER_KEY)],
            [sg.Slider(range=(0,4), size=(20,15), orientation='horizontal', key=keys.ADVANCED_OPTIONS_GAUSSIAN_MATRIX_SLIDER_KEY)],
            [sg.Slider(range=([0.0, 4.0]), resolution=0.1, size=(20,15), orientation='horizontal', key=keys.ADVANCED_OPTIONS_SHARPEN_SLIDER_KEY)],
            [sg.Slider(range=([0.0, 4.0]), resolution=0.1, size=(20,15), orientation='horizontal', key=keys.ADVANCED_OPTIONS_CONTRAST_SLIDER_KEY)],
            [sg.Slider(range=([0.0, 4.0]), resolution=0.1, size=(20,15), orientation='horizontal', key=keys.ADVANCED_OPTIONS_BRIGHTNESS_SLIDER_KEY)],
            [sg.Slider(range=(1,32), size=(20,15), orientation='horizontal', key=keys.ADVANCED_OPTIONS_N_COLORS_SLIDER_KEY)]
        ]

        layout_advanced_options = [
            [sg.Column(layout_options), sg.VSeparator(), sg.vtop(sg.Column(layout_sliders))],
        ]
        
        return layout_advanced_options

    # Apagar tela    
    def close(self):
        self.__tela.close()

    # Init da tela
    def init_tela(self, modelo: classifier.ImageClassifier):
        # Aplicando valores padrão do modelo na tela
        self.__tela[keys.ADVANCED_OPTIONS_PORCENTAGEM_TREINAMENTO_SLIDER_KEY].update(value=modelo.get_percentage_train())
        self.__tela[keys.ADVANCED_OPTIONS_GAUSSIAN_MATRIX_SLIDER_KEY].update(value=modelo.get_gaussian_radius())
        self.__tela[keys.ADVANCED_OPTIONS_SHARPEN_SLIDER_KEY].update(value=modelo.get_sharpness_boost_strength())
        self.__tela[keys.ADVANCED_OPTIONS_CONTRAST_SLIDER_KEY].update(value=modelo.get_contrast_boost_strength())
        self.__tela[keys.ADVANCED_OPTIONS_BRIGHTNESS_SLIDER_KEY].update(value=modelo.get_brightness_boost_strength())
        self.__tela[keys.ADVANCED_OPTIONS_N_COLORS_SLIDER_KEY].update(value=modelo.get_n_colors())

    # Reset os valores da tela para seus valores padrão
    def reset_tela_default_values(self, modelo: classifier.ImageClassifier):
        # Aplicando valores padrão do modelo na tela
        self.__tela[keys.ADVANCED_OPTIONS_PORCENTAGEM_TREINAMENTO_SLIDER_KEY].update(value=modelo.get_percentage_train())
        self.__tela[keys.ADVANCED_OPTIONS_GAUSSIAN_MATRIX_SLIDER_KEY].update(value=modelo.get_gaussian_radius())
        self.__tela[keys.ADVANCED_OPTIONS_SHARPEN_SLIDER_KEY].update(value=modelo.get_sharpness_boost_strength())
        self.__tela[keys.ADVANCED_OPTIONS_CONTRAST_SLIDER_KEY].update(value=modelo.get_contrast_boost_strength())
        self.__tela[keys.ADVANCED_OPTIONS_BRIGHTNESS_SLIDER_KEY].update(value=modelo.get_brightness_boost_strength())
        self.__tela[keys.ADVANCED_OPTIONS_N_COLORS_SLIDER_KEY].update(value=modelo.get_n_colors())

    def construir_tela_opcoes_avancadas(self, modelo: classifier.ImageClassifier):
        self.__tela = sg.Window('Opções avançadas', self._build_layout(), resizable=False, font=('Helvetica', 16), finalize=True)
        
        # Aplicando valores padrao dentro da tela
        self.init_tela(modelo)
        
        while True:
            event, values = self.__tela.read()
            
            if event == sg.WIN_CLOSED:
                break
            
            
            elif event == keys.ADVANCED_OPTIONS_CONFIRM_MODIFICATIONS_KEY:
                # Aplicar efeitos                
                modelo.set_percentage_train(int(values[keys.ADVANCED_OPTIONS_PORCENTAGEM_TREINAMENTO_SLIDER_KEY]))
                modelo.set_gaussian_radius(values[keys.ADVANCED_OPTIONS_GAUSSIAN_MATRIX_SLIDER_KEY])
                modelo.set_sharpness_boost_strength(values[keys.ADVANCED_OPTIONS_SHARPEN_SLIDER_KEY])
                modelo.set_contrast_boost_strength(values[keys.ADVANCED_OPTIONS_CONTRAST_SLIDER_KEY])
                modelo.set_brightness_boost_strength(values[keys.ADVANCED_OPTIONS_BRIGHTNESS_SLIDER_KEY])
                modelo.set_n_colors(int(values[keys.ADVANCED_OPTIONS_N_COLORS_SLIDER_KEY]))
                
                # Fechar a janela
                break
            
            elif event == keys.ADVANCED_OPTIONS_RESET_KEY:
                modelo_default = classifier.ImageClassifier()
                self.reset_tela_default_values(modelo_default)
                del modelo_default
            
        self.close()