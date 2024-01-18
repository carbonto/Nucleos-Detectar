import pandas as pd
import matplotlib.pyplot as plt
import PySimpleGUI as sg
import os
import numpy as np

def diagrama_lineas(file_path):
    global genero, segundos, minutos, horas
    # Load the CSV file
    file = file_path   # Replace with your actual file path
    data = pd.read_csv(file,usecols=range(8))

    # Clean column names (remove extra spaces)
    data.columns = data.columns.str.strip()

    if segundos:
        # Selecting every 50th second for the x-axis
        x_ticks = data['sec'][::intervalo]
        x_ticks_rounded = np.round(x_ticks).astype(int)
        x_label_name = 'Segundos'
    elif minutos:
        # Convert seconds to minutes and select every 20th minute for the x-axis
        data['sec'] = data['sec'] / 60
        x_ticks = data['sec']
        x_ticks_rounded = np.round(x_ticks).astype(int)
        x_label_name = 'Minutos'
    elif horas:
        # Convert seconds to hours and select every hour for the x-axis
        data['sec'] = data['sec'] / 3600
        x_ticks = data['sec']
        x_ticks_rounded = np.round(x_ticks).astype(int)
        x_label_name = 'Horas'

    # Plotting again with the adjusted x-axis
    plt.figure(figsize=(15, 6))
    plt.plot(data['sec'], data['total_count(in)(line1)'], label='IN')
    plt.plot(data['sec'], data['total_count(out)(line1)'], label='OUT')
    if genero:
        #Calculate and plot increments for man
        increment_man = data['man'].cumsum()
        plt.plot(data['sec'],increment_man, label='Hombres in + out')

        #Calculate and plot increments for woman
        increment_woman = data['woman'].cumsum()
        plt.plot(data['sec'], increment_woman, label='Mujeres in + out')

        #Find max 
        max_man = increment_man.max()
        max_woman = increment_woman.max()
        #Get index of maxq
        max_man_index = increment_man.idxmax()
        max_woman_index = increment_woman.idxmax()
        # Annotate the maximum points
        plt.annotate(f'Max MAN: {int(max_man)}', 
                    xy=(data['sec'][max_man_index], max_man), 
                    xytext=(10, 3),
                    textcoords="offset points",
                    arrowprops=dict(arrowstyle="->", color='green'))

        plt.annotate(f'Max WOMAN: {int(max_woman)}', 
                    xy=(data['sec'][max_woman_index], max_woman), 
                    xytext=(10, -15),
                    textcoords="offset points",
                    arrowprops=dict(arrowstyle="->", color='red'))

    # Asegurar una buena distribución de ticks
    plt.title('Conteo de personas al entrar y salir de la zona de la playa')
    plt.xlabel(x_label_name)
    plt.ylabel('Total Conteo')
    plt.xticks(x_ticks,labels=x_ticks_rounded)
    # Reducir la cantidad de ticks manualmente
    plt.xticks(np.arange(min(x_ticks), max(x_ticks)+1, step=intervalo))
    plt.legend()
    plt.grid(True)  

    # Find the maximum value for IN and OUT
    max_in = data['total_count(in)(line1)'].max()
    max_out = data['total_count(out)(line1)'].max()

    # Get the index of the maximum value for IN and OUTnge(min(x_ticks), max(x_ticks)+1, step=1
    max_in_index = data['total_count(in)(line1)'].idxmax()
    max_out_index = data['total_count(out)(line1)'].idxmax()

    # Annotate the maximum points
    plt.annotate(f'Max IN: {int(max_in)}', 
                xy=(data['sec'][max_in_index], max_in), 
                xytext=(10, 3),
                textcoords="offset points",
                arrowprops=dict(arrowstyle="->", color='blue'))

    plt.annotate(f'Max OUT: {int(max_out)}', 
                xy=(data['sec'][max_out_index], max_out), 
                xytext=(10, -15),
                textcoords="offset points",
                arrowprops=dict(arrowstyle="->", color='orange'))
    plt.show()

def diagrama_barras(file_path):
    global genero
    # Load the CSV file
    file = file_path   # Replace with your actual file path
    data = pd.read_csv(file,usecols=range(8))

    # Clean column names (remove extra spaces)
    data.columns = data.columns.str.strip()

    # Creating a vertical bar chart with "IN" and "OUT" labels on the x-axis and total counts on the y-axis

    # Calculating the total counts for IN and OUT
    total_count_in = data['total_count(in)(line1)'].iloc[-1]
    total_count_out = data['total_count(out)(line1)'].iloc[-1]

    # X-axis labels
    x_labels = ['IN', 'OUT']

    # Y-axis values
    y_values = [total_count_in, total_count_out]
    
    plt.figure(figsize=(10, 6))

    bars = plt.bar(x_labels, y_values, color=['blue', 'orange'])
    if genero:
        # X-axis labels
        x_labels = ['IN', 'OUT','MAN IN+OUT','WOMAN IN+OUT']

        increment_man = data['man'].cumsum().iloc[-1]
        increment_woman =data['woman'].cumsum().iloc[-1]
        # Y-axis values
        y_values = [total_count_in, total_count_out,increment_man,increment_woman]
        
        plt.figure(figsize=(10, 6))

        bars = plt.bar(x_labels, y_values, color=['blue', 'orange','green','red'])

    plt.title('Conteo de personas al entrar y salir de la zona de la playa')
    plt.xlabel('Entrada o salida')
    plt.ylabel('Conteo total')

    # Annotate each bar with its height value
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval, int(yval), va='bottom', ha='center')


    plt.grid(False)
    plt.show()


def main():
    global genero,segundos,minutos,horas,intervalo
    #Define graphical interface 
    sg.theme('DarkAmber')   # Add a touch of color
    # All the stuff inside your window.
    layout = [  [sg.Text("Seleccione el archivo .csv")],
                [sg.Text('Archivo', size=(8, 1)), sg.Input(), sg.FileBrowse()],
                [sg.Text("Seleccione el tipo de grafica")],
                [sg.Checkbox("Diagrama de lineas", key="-LINES-", default=False)], 
                [sg.Checkbox('Diagrama de barras', key="-BARS-", default=False)],
                [sg.Checkbox('Formato segundos',key="-SECONDS-", default=False)],
                [sg.Checkbox('Formato minutos',key="-MINUTES-", default=False)],
                [sg.Checkbox('Formato horas',key="-HOURS-", default=False)],
                [sg.Text("Intervalo:", size=(8, 1)), sg.InputText(key="-INTERVAL-", size=(10, 1), default_text="50")],
                [sg.Checkbox('Contar genero',key = "-GENDER-", default=False)],
                [sg.Submit(), sg.Cancel()] 
    ]
    #Create window aplication
    window = sg.Window('Analisis csv conteo', layout)

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        #Read events
        event, values = window.read()
        #Close window
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
       
        #Read file
        if event == 'Submit':
            file_path = values[0]
            lineas = values['-LINES-']
            barras = values['-BARS-']
            genero = values['-GENDER-']
            minutos = values['-MINUTES-']
            horas = values['-HOURS-']
            segundos = values['-SECONDS-']
            intervalo = int(values['-INTERVAL-'])
        #Validate csv path
        if not file_path or not file_path.endswith('.csv'):
            sg.popup_error('Por favor seleccione un archivo .csv')
            continue
        #Validate diagram is selected
        if not lineas and not barras:
            sg.popup_error('Por favor seleccione un tipo de diagrama')
            continue
        if lineas and barras:
            sg.popup_error('Por favor seleccione solo un tipo de diagrama')
            continue
        if lineas:
            # Validate time format selection
            if not (minutos or horas or segundos):
                sg.popup_error('Por favor seleccione un formato de tiempo')
            elif sum([minutos, horas, segundos]) > 1:
                sg.popup_error('Por favor seleccione solo un formato de tiempo')
            
        if lineas:
            diagrama_lineas(file_path)
        elif barras:
            diagrama_barras(file_path)


if __name__ == '__main__':
    main()  