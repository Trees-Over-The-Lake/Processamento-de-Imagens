import PySimpleGUI as sg

DEFAULT_IMG="./frontend/assets/sample_preview_image.png"

def options_window(modelo):

    layout_options = [
        [
            sg.Text('Escolha a porcentagem de dados disponível para treino (padrão=75):', font=('Helvetica', 16)),
            sg.Button("?", border_width=4, key="__help_porcentagem"),
            
        ],
        [
            sg.Text('Escolha o raio da matriz gaussiana (padrão=0):', font=('Helvetica', 16)),
            sg.Button("?", border_width=4, key="__help_gaussian"),
            
        ],
        [
            sg.Text('Escolha a quantidade de aumento do sharpen (padrão=1.4):', font=('Helvetica', 16)),
            sg.Button("?", border_width=4, key="__help_sharpen"),
           
        ],
        [
            sg.Text('Escolha a quantidade de aumento do contraste (padrão=2.2):', font=('Helvetica', 16)),
            sg.Button("?", border_width=4, key="__help_contrast"),
        ],
        [
            sg.Text('Escolha a quantidade de aumento do brilho (padrão=1.1):', font=('Helvetica', 16)),
            sg.Button("?", border_width=4, key="__help_brightness"),
        ],
        [sg.Button('Preview das configurações', border_width=4, key="__preview")],
        [sg.Button('Ok!', border_width=4, key="__ok")]
    ]
    
    layout_sliders = [
        [sg.Slider(range=(1,99), 
                default_value=modelo.get_percentage_train(), 
                size=(20,15),
                orientation='horizontal', 
                key='-PORCENTAGEM_TREINAMENTO-')],
        [sg.Slider(range=(0,4), 
                default_value=modelo.get_gaussian_radius(),
                size=(20,15),
                orientation='horizontal', 
                key='-RAIO_MATRIX_GAUSSIANA-'
            )],
        [sg.Slider(range=([0.0, 4.0]), 
            resolution=0.2, 
            default_value=modelo.get_sharpness_boost_strength(),
            size=(20,15),
            orientation='horizontal', 
            key='-SHARPEN_BOOST-',
            )],
        [sg.Slider(range=([0.0, 4.0]), 
            resolution=0.2, 
            default_value=modelo.get_contrast_boost_strength(),
            size=(20,15),
            orientation='horizontal', 
            key='-CONTRAST_BOOST-'
            )],
        [sg.Slider(range=([0.0, 4.0]), 
            resolution=0.2, 
            default_value=modelo.get_brightness_boost_strength(),
            size=(20,15),
            orientation='horizontal', 
            key='-BRIGHTNESS_BOOST-'
            )]
    ]

    layout_tela = [
        [sg.Column(layout_options), sg.VSeparator(), sg.Column(layout_sliders)],
    ]

    options_window = sg.Window('Opções avançadas', layout_tela)

    while True:

        event, values = options_window.read()

        porcentagem       = values['-PORCENTAGEM_TREINAMENTO-']
        gaussian_radius   = values['-RAIO_MATRIX_GAUSSIANA-']
        sharpen_factor    = values['-SHARPEN_BOOST-']
        contrast_factor   = values['-CONTRAST_BOOST-']
        brightness_factor = values['-BRIGHTNESS_BOOST-']
        ncolors           = values['']

        if event == '__help_porcentagem':
            print("ABRIR HELP_SHARPEN")

        if event == '__ok':
            

            modelo.set_percentage_train(porcentagem)
            modelo.set_gaussian_radius(gaussian_radius)
            modelo.set_sharpness_boost_strength(sharpen_factor)
            modelo.set_contrast_boost_strength(contrast_factor)
            modelo.set_brightness_boost_strength(brightness_factor)
            
            options_window.close()
            break

        elif event == '__preview':

            modelo.set_percentage_train(porcentagem)
            modelo.set_gaussian_radius(gaussian_radius)
            modelo.set_sharpness_boost_strength(sharpen_factor)
            modelo.set_contrast_boost_strength(contrast_factor)
            modelo.set_brightness_boost_strength(brightness_factor)

            modelo.preview_single_image(DEFAULT_IMG)