import PySimpleGUI as sg

def read_file(filepath):
    with open(filepath) as f:
        text = f.read()
    
    return text


def draw_credits_window():
    credits_text = read_file("./frontend/assets/texts/creditos.txt")

    layout_creditos = [
        [sg.Text(credits_text)],
        [sg.Button("Retornar", border_width=4, key='__return')]
    ]

    creditos_window = sg.Window('Créditos', layout_creditos)
    event, values = creditos_window.read()

    if event == '__return':
        creditos_window.close()


def draw_help_window():

    help_text = read_file("./frontend/assets/texts/help.txt")

    layout_help = [
        [sg.Text(help_text)],
        [sg.Button("Retornar", key='__return')]
    ]

    help_window = sg.Window('Informações sobre o trabalho', layout_help)
    event, values = help_window.read()

    if event == '__return':
        help_window.close()