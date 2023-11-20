import pandas as pd
import matplotlib.pyplot as plt
import PySimpleGUI as sg
import os

def diagrama_lineas(file_path):
    # Load the CSV file
    file = file_path   # Replace with your actual file path
    data = pd.read_csv(file)

    # Clean column names (remove extra spaces)
    data.columns = data.columns.str.strip()


    # Selecting every 50th second for the x-axis
    x_ticks = data['sec'][::50]

    # Plotting again with the adjusted x-axis
    plt.figure(figsize=(15, 6))
    plt.plot(data['sec'], data['total_count(in)(line0)'], label='IN')
    plt.plot(data['sec'], data['total_count(out)(line0)'], label='OUT')

    plt.title('Conteo de personas al entrar y salir de la zona de la playa')
    plt.xlabel('Segundos')
    plt.ylabel('Total Conteo')
    plt.xticks(x_ticks)
    plt.legend()
    plt.grid(True)

    # Find the maximum value for IN and OUT
    max_in = data['total_count(in)(line0)'].max()
    max_out = data['total_count(out)(line0)'].max()

    # Get the index of the maximum value for IN and OUT
    max_in_index = data['total_count(in)(line0)'].idxmax()
    max_out_index = data['total_count(out)(line0)'].idxmax()

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
    # Load the CSV file
    file = file_path   # Replace with your actual file path
    data = pd.read_csv(file)

    # Clean column names (remove extra spaces)
    data.columns = data.columns.str.strip()

    # Creating a vertical bar chart with "IN" and "OUT" labels on the x-axis and total counts on the y-axis

    # Calculating the total counts for IN and OUT
    total_count_in = data['total_count(in)(line0)'].iloc[-1]
    total_count_out = data['total_count(out)(line0)'].iloc[-1]

    # X-axis labels
    x_labels = ['IN', 'OUT']

    # Y-axis values
    y_values = [total_count_in, total_count_out]

    plt.figure(figsize=(10, 6))

    bars = plt.bar(x_labels, y_values, color=['blue', 'orange'])

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
    #Define graphical interface 
    sg.theme('DarkAmber')   # Add a touch of color
    # All the stuff inside your window.
    layout = [  [sg.Text("Seleccione el archivo .csv")],
                [sg.Text('Archivo', size=(8, 1)), sg.Input(), sg.FileBrowse()],
                [sg.Text("Seleccione el tipo de grafica")],
                [sg.Checkbox("Diagrama de lineas", key="-LINES-", default=False)], 
                [sg.Checkbox('Diagrama de barras', key="-BARS-", default=False)],
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
            diagrama_lineas(file_path)
        elif barras:
            diagrama_barras(file_path)


if __name__ == '__main__':
    main()  