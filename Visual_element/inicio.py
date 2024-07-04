import random
import string
from PyQt5.QtCore import QObject, QTimer, Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTabWidget, QPlainTextEdit, QPushButton, QHBoxLayout, \
     QFormLayout, QGroupBox
from qtawesome import icon

class Dashboard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet("background-color: transparent; border-radius: 5px;")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)

        # Create a horizontal layout for the title and connection status widget
        self.header_layout = QHBoxLayout()
        self.layout.addLayout(self.header_layout)

        self.title_label = QLabel("Dashboard")
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold; background-color: transparent;")
        self.header_layout.addWidget(self.title_label)

        # Add a stretch to the header layout to push the title to the left
        self.header_layout.addStretch()

        # Create a group box for the connection status
        self.connection_group = QGroupBox("Conexión")
        self.connection_group.setStyleSheet("QGroupBox { border: 1px solid gray; border-radius: 5px; padding: 10px; }")
        self.header_layout.addWidget(self.connection_group)
        self.connection_group.setMinimumWidth(500)  # Establece un ancho máximo de 800 píxeles

        # Create a horizontal layout inside the group box
        self.connections_layout = QHBoxLayout()
        self.connection_group.setLayout(self.connections_layout)

        # Add some example connections
        self.add_connection("IP: 192.168.1.100", "Puerto: 8080", "Estado: Conectado")
        self.add_connection("IP: 192.168.1.101", "Puerto: 8081", "Estado: Conectado")



        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget {
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 5px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                font-size: 18px; 
                font-weight: bold;
                font: Open Sans;

                
            }
            QTabBar::tab {
                background-color: #E0E0E0;
                color: #333;
                padding: 10px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-bottom: none;
                margin-right: 2px;
                transition: background-color 0.3s, color 0.3s, transform 0.3s;
            }
            QTabBar::tab:selected {
                background-color: #6778D2;
                color: white;
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-bottom: none;
                transform: translateY(-3px) scale(1.05);
            }
            QTabBar::tab:!selected {
                margin-top: 2px;
                background-color: #F0F0F0;
                color: #777;
                transform: perspective(100px) rotateX(5deg);
                transition: transform 0.3s;
            }
            QTabBar::tab:!selected:hover {
                background-color: #E0E0E0;
                color: #333;
                transform: perspective(100px) rotateX(0deg) translateY(-2px);
            }
            QTabWidget::pane {
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-top: none;
                top: -1px;
                background-color: transparent;
            }
        """)
        self.layout.addWidget(self.tab_widget)

        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab_widget.addTab(self.tab1, icon('fa.sitemap',scale_factor=1.5), "Resultados")
        self.tab_widget.addTab(self.tab2, icon('fa.bar-chart',scale_factor=1.5), "Ordenes")


        self.tab1.setStyleSheet("background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #E3E3E3, "
                                "stop:1 #B1F2F0);")

        self.tab2.setStyleSheet("background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #E3E3E3, "
                                "stop:1 #B1F2F0);")

        self.tab1_layout = QVBoxLayout()
        self.tab1.setLayout(self.tab1_layout)
        self.tab1_layout.setContentsMargins(10, 10, 10, 10)
        self.tab1_layout.setSpacing(10)
        self.tab1_connect_button = QPushButton("Conectar")
        self.tab1_connect_button.setStyleSheet("""
                   QPushButton {
                       background-color: #6778D2;
                       color: white;
                       border: none;
                       padding: 10px;
                       font-size: 18px;
                       font-weight: bold;
                       border-radius: 5px;
                   }
                   QPushButton:hover {
                       background-color: #5A6AC4;
                   }
                   QPushButton:pressed {
                       background-color: #4E5AA6;
                   }
               """)
        self.tab1_connect_button.setFixedSize(150, 40)  # Establecer un tamaño fijo para el botón

        self.tab1_connect_button_layout = QHBoxLayout()
        self.tab1_connect_button_layout.addStretch()  #

        self.tab1_connect_button_layout.addWidget(self.tab1_connect_button)  # Agregar el botón a la derecha
        self.tab1_layout.addLayout(self.tab1_connect_button_layout)  # Agregar el layout horizontal al layout principal
        self.tab1_label = QLabel("Resultados Estatus: ")
        self.tab1_label.setStyleSheet("color: black; font-size: 16px; background-color: transparent;font-weight: "
                                      "bold;font: Open Sans;")


        self.tab1_layout.addWidget(self.tab1_label)





        self.tab2_layout = QVBoxLayout()
        self.tab2.setLayout(self.tab2_layout)
        self.tab2_layout.setContentsMargins(10, 10, 10, 10)
        self.tab2_layout.setSpacing(10)
        self.tab2_connect_button = QPushButton("Conectar")
        self.tab2_connect_button.setStyleSheet("""
                          QPushButton {
                              background-color: #6778D2;
                              color: white;
                              border: none;
                              padding: 10px;
                              font-size: 18px;
                              font-weight: bold;
                              border-radius: 5px;
                          }
                          QPushButton:hover {
                              background-color: #5A6AC4;
                          }
                          QPushButton:pressed {
                              background-color: #4E5AA6;
                          }
                      """)
        self.tab2_connect_button.setFixedSize(150, 40)  # Establecer un tamaño fijo para el botón

        self.tab2_connect_button_layout = QHBoxLayout()
        self.tab2_connect_button_layout.addStretch()  #
        self.tab2_connect_button_layout.addWidget(self.tab2_connect_button)  # Agregar el botón a la derecha

        self.tab2_layout.addLayout(self.tab2_connect_button_layout)  # Agregar el layout horizontal al layout principal

        self.tab2_label = QLabel("Ordenes Estatus:")
        self.tab2_label.setStyleSheet("color: black; font-size: 16px; background-color: transparent;font-weight: "
                                      "bold;font: Open Sans;")
        self.tab2_layout.addWidget(self.tab2_label)



        self.tab1_text_edit = QPlainTextEdit()
        self.tab1_text_edit.setReadOnly(True)
        self.tab1_text_edit.setStyleSheet(""" 
                 QPlainTextEdit {
                color: black;
                font-size: 18px;
                background-color: white;
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 5px;
                padding: 10px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                                        font: Open Sans;

            }
            QScrollBar:vertical {
                background-color: transparent;
                border: none;
                width: 8px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background-color: #bfbfbf;
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #999999;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
                height: 0;
            }
        """)
        self.tab1_layout.addWidget(self.tab1_text_edit)
        self.tab1_word_generator = WordGenerator(self.tab1_text_edit)

        self.tab2_text_edit = QPlainTextEdit()
        self.tab2_text_edit.setReadOnly(True)
        self.tab2_text_edit.setStyleSheet("""
               QPlainTextEdit {
                color: black;
                font-size: 18px;
                background-color: white;
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 5px;
                padding: 10px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                                        font: Open Sans;

            }
            QScrollBar:vertical {
                background-color: transparent;
                border: none;
                width: 8px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background-color: #bfbfbf;
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #999999;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
                height: 0;
            }
        """)
        self.tab2_layout.addWidget(self.tab2_text_edit)
        self.tab2_word_generator = WordGenerator(self.tab2_text_edit)

    def add_connection(self, ip, port, status):
        form_layout = QFormLayout()
        form_layout.setFormAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        form_layout.setLabelAlignment(Qt.AlignLeft)

        ip_label = QLabel(ip)
        ip_label.setStyleSheet("font-weight: bold; color: #333333;font-size: 14px;")
        port_label = QLabel(port)
        port_label.setStyleSheet("color: #666666;font-size: 14px;")
        status_label = QLabel(status)
        status_label.setStyleSheet("color: #666666;font-size: 14px;")

        form_layout.addRow(QLabel("IP:"), ip_label)
        form_layout.addRow(QLabel("Puerto:"), port_label)
        form_layout.addRow(QLabel("Estado:"), status_label)

        widget = QWidget()
        widget.setLayout(form_layout)
        widget.setStyleSheet("""
            QWidget {
                background-color: #F0F0F0;
                border-radius: 5px;
                padding: 1px;
            }
        """)

        self.connections_layout.addWidget(widget)

class WordGenerator(QObject):
    def __init__(self, text_edit, min_length=3, max_length=10):
        super().__init__()
        self.text_edit = text_edit
        self.min_length = min_length
        self.max_length = max_length
        self.timer = QTimer()
        self.timer.timeout.connect(self.generate_word)
        self.timer.start(1000)  # Generar una nueva palabra cada 1 segundo

    def generate_word(self):
        word_length = random.randint(self.min_length, self.max_length)
        word = ''.join(random.choices(string.ascii_letters, k=word_length))
        self.text_edit.appendPlainText(word + '\n ')  # Agregar un espacio después de cada palabra
