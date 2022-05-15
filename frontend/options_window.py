import PySimpleGUI as sg


def options_window(modelo):

    layout_options = [
        [sg.Text(
            'Escolha a porcentagem de dados disponível para treino (padrão=75): '), 
            sg.Slider(range=(1,99), 
            default_value=75, 
            size=(20,15),
            orientation='horizontal', 
            key='-PORCENTAGEM_TREINAMENTO-')
        ],
        [sg.Text(
            'Escolha o raio da matriz gaussiana (padrão=0): '), 
                sg.Slider(range=(0,4), 
                default_value=0,
                size=(20,15),
                orientation='horizontal', 
                key='-RAIO_MATRIX_GAUSSIANA-'
            )
        ],
        [sg.Text(
            'Escolha a quantidade de aumento do sharpen (padrão=1.4): '), 
            sg.Slider(range=([0.0, 4.0]), 
                resolution=0.2, 
                default_value=1.4,
                size=(20,15),
                orientation='horizontal', 
                key='-SHARPEN_BOOST-'
                )
        ],
        [sg.Button('Ok!', border_width=4, key="__ok")]
    ]

    options_window = sg.Window('Créditos', layout_options)
    event, values = options_window.read()
    
    if event == '__ok':
        porcentagem     = values['-PORCENTAGEM_TREINAMENTO-']
        gaussian_radius = values['-RAIO_MATRIX_GAUSSIANA-']
        sharpen_factor  = values['-SHARPEN_BOOST-']
        
        modelo.set_percentage_train(porcentagem)
        modelo.set_gaussian_radius(gaussian_radius)
        modelo.set_sharpness_boost_strength(sharpen_factor)
        

        options_window.close()