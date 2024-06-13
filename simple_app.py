import sys
import random
import matplotlib
matplotlib.use('Qt5Agg')  # Define o backend do matplotlib para Qt5Agg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout, QCheckBox, QRadioButton, QTextEdit, QMessageBox
from PyQt5.QtCore import QTimer

import zmq
import time

class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None):
        # Cria o contexto ZMQ
        self.context = zmq.Context()
        # Cria um socket REP (reply)
        self.socket = self.context.socket(zmq.REQ)
        # Liga o socket a um arquivo IPC
        self.socket.connect("ipc:///tmp/Z03")
        self.socket.setsockopt(zmq.RCVTIMEO, 200)
        
        fig, self.ax = plt.subplots()
        super().__init__(fig)
        self.setParent(parent)
        self.plot_data = [0] * 31  # Inicializa com 30 zeros
        self.time_values = list(range(0, 31))  # Valores de tempo para o eixo x
        self.plot()

    def plot(self):
        self.ax.clear()
        self.ax.plot(self.time_values, self.plot_data, 'r-')
        self.ax.set_title('Gráfico de Exemplo (últimos 30 segundos)')
        self.ax.set_xlabel('Tempo (s)')
        self.ax.set_ylabel('Valor')
        self.ax.set_xlim(0, 30)  # Limita o eixo x aos últimos 30 segundos
        self.ax.set_ylim(0, 4)   # Limita o eixo y de 0 a 10
        self.draw()

    def update_plot(self):
        try:
            self.socket.send_string("Read")
            msg = self.socket.recv_string()
            self.plot_data.insert(0,float(msg))
        except Exception as e:
            print(f"Erro ao receber resposta: {e}")
            self.plot_data.insert(0,0)
        self.plot_data.pop()
        self.plot()



def show_message():
    line_edit_text = line_edit.text()
    text_edit_text = text_edit.toPlainText()
    QMessageBox.information(None, 'Botao', f"BotaoOK")



app = QApplication(sys.argv)

# Criação da janela principal
window = QWidget()
window.setWindowTitle('Exemplo PyQt5 com Vários Widgets e Gráfico')
window.resize(800, 600)  # Define o tamanho da janela

# Layout vertical principal
main_layout = QVBoxLayout()

# Criação dos widgets
label = QLabel('Digite algo:')
line_edit = QLineEdit()
check_box = QCheckBox('Opção 1')
radio_button = QRadioButton('Escolha 1')
text_edit = QTextEdit()
button = QPushButton('Ler Sensor Z03')
button.clicked.connect(show_message)

# Criação do gráfico
plot_canvas = PlotCanvas(window)

# Adiciona os widgets ao layout
main_layout.addWidget(label)
main_layout.addWidget(line_edit)
main_layout.addWidget(check_box)
main_layout.addWidget(radio_button)
main_layout.addWidget(text_edit)
main_layout.addWidget(button)
main_layout.addWidget(plot_canvas)

# Define o layout na janela principal
window.setLayout(main_layout)

# Configura o timer para atualizar o gráfico a cada 1 segundo
timer = QTimer()
timer.timeout.connect(plot_canvas.update_plot)
timer.start(1000)  # Intervalo de 1000 milissegundos (1 segundo)

# Mostrar a janela
window.show()

# Executar a aplicação
sys.exit(app.exec_())
