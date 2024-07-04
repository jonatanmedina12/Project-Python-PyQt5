from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QSize, QPropertyAnimation, QEasingCurve, Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFrame, QPushButton, QSpacerItem, QSizePolicy, QLabel, QDesktopWidget
from qtawesome import icon


class SideBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.text_scale = "18px"

        self.scale_factor = None
        self.historial1 = None
        self.is_settings_selected = False
        self.is_history_selected = False

        self.scale_factor = 1.5
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(1, 1, 5, 5)  # Eliminar los márgenes del layout principal
        self.layout.setSpacing(80)

        self.content_frame = QFrame()
        self.content_frame.setStyleSheet("""
            QFrame {
        background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #15E0D5, stop:1 #6778D2);
                color: #003559;
                border-radius: 5px;
                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
            }
        """)
        self.content_frame.setMinimumSize(65, 30)

        self.content_layout = QVBoxLayout()
        self.content_frame.setLayout(self.content_layout)
        self.content_layout.setContentsMargins(1, 1, 1, 1)  # Agregar pequeños márgenes al layout interno

        self.toggle_button = QPushButton()
        self.toggle_button.clicked.connect(self.toggle_sidebar)
        self.toggle_button.setStyleSheet(f"""
                     QPushButton  {{
                         background-color: transparent;
                         color: white;
                         border: none;
                         padding: 10px;
                         text-align: center;
                         font-size: {self.text_scale};
                         border-radius: 3px;
                        font: Open Sans;
                        
                     }}
                    QPushButton:hover {{
                        background-color: white;
                        color: white;
                         }}
                    
                 """)
        self.toggle_button.setIcon(icon('mdi.menu', color="white", scale_factor=self.scale_factor))

        self.toggle_button.enterEvent = lambda event: self.toggle_button.setIcon(
            icon('mdi.menu', color='#6778D2', scale_factor=self.scale_factor))
        self.toggle_button.leaveEvent = lambda event: self.toggle_button.setIcon(
            icon('mdi.menu', color='white', scale_factor=self.scale_factor))

        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setFrameShadow(QFrame.Sunken)
        divider.setStyleSheet("""
              QFrame {
                  background-color: white;
                  border: none;
                  height: 15px;
              }
              QFrame::before {
                  content: "";
                  position: absolute;
                  top: 0;
                  left: 0;
                  right: 0;
                  height: 4px;
                  background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #B9B8B8, stop:0.25 #A8A8A8, stop:0.5 #666666, stop:0.75 #A8A8A8, stop:1 #B9B8B8);
                  border-top: 1px solid #666666;
              }
              QFrame::after {
                  content: "";
                  position: absolute;
                  bottom: 0;
                  left: 0;
                  right: 0;
                  height: 4px;
                  background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #FFFFFF, stop:0.25 #E6E6E6, stop:0.5 #C8C8C8, stop:0.75 #E6E6E6, stop:1 #FFFFFF);
                  border-bottom: 1px solid #C8C8C8;
              }
          """)

        self.content_layout.addWidget(self.toggle_button)
        self.content_layout.addWidget(divider)

        self.image_label = QLabel()
        self.image_label.setPixmap(QPixmap(""))
        self.image_label.setScaledContents(True)  # Desactiva el ajuste de escala automático
        self.image_label.setFixedSize(QSize(30, 30))  # Ajusta el tamaño según tus necesidades
        self.image_label.setVisible(True)

        self.image_label2 = QLabel()
        self.image_label2.setPixmap(QPixmap(""))
        self.image_label2.setScaledContents(True)  # Desactiva el ajuste de escala automático
        self.image_label2.setFixedSize(QSize(105, 70))  # Ajusta el tamaño según tus necesidades
        self.image_label2.setVisible(False)
        self.image_label2.setStyleSheet("""
            QLabel {
                background-color: transparent;
            }
            QLabel::item {
                background-color: transparent;
            }
        """)

        self.content_layout.addWidget(self.toggle_button)
        self.content_layout.addWidget(divider)
        self.content_layout.addWidget(self.image_label, alignment=Qt.AlignCenter)
        self.content_layout.addWidget(self.image_label2, alignment=Qt.AlignCenter)

        self.home_button = QPushButton()
        self.home_button.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: white;
                border: none;
                padding: 10px;
                text-align: center;
                font-size: {self.text_scale};
                border-radius: 5px;
                font-weight: bold;
                  font: Open Sans;


            }}
            QPushButton:hover {{
                background-color: white;
            }}
        """)
        self.home_button.setIcon(icon('mdi.home-account', color="white", scale_factor=self.scale_factor))
        self.home_button.setIconSize(QSize(24, 24))
        self.home_button.clicked.connect(self.go_back)

        self.home_button.enterEvent = lambda event: self.update_button_style(self.home_button, '#6778D2',
                                                                             'mdi.home-account', self.scale_factor)
        self.home_button.leaveEvent = lambda event: self.update_button_style(self.home_button, 'white',
                                                                             'mdi.home-account', self.scale_factor)

        self.content_layout.addWidget(self.home_button)

        self.settings_button = QPushButton()
        self.settings_button.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: white;
                border: none;
                padding: 10px;
                text-align: center;
                font-size: {self.text_scale};
                border-radius: 10px;
                font-weight: bold;
                        font: Open Sans;

            }}
            QPushButton:hover {{
                background-color:white;
            }}
        """)
        self.settings_button.setIcon(icon('fa.gear', color="white", scale_factor=1.2))
        self.settings_button.setIconSize(QSize(24, 24))

        self.settings_button.enterEvent = lambda event: self.update_button_style(self.settings_button, '#6778D2',
                                                                                 'fa.gear', 1.2)
        self.settings_button.leaveEvent = lambda event: self.update_button_style(self.settings_button, 'white',
                                                                                 'fa.gear', 1.2)

        self.settings_button.clicked.connect(self.show_settings_screen)
        self.content_layout.addWidget(self.settings_button)

        self.historial = QPushButton()
        self.historial.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: white;
                border: none;
                padding: 10px;
                text-align: center;
                font-size: {self.text_scale};
                border-radius: 10px;
                font-weight: bold;
                        font: Open Sans;

            }}
            QPushButton:hover {{
                background-color: white;
            }}
        """)
        self.historial.setIcon(icon('fa.history', color="white", scale_factor=1.3))
        self.historial.setIconSize(QSize(24, 24))
        self.historial.enterEvent = lambda event: self.update_button_style(self.historial, '#6778D2',
                                                                           'fa.history', 1.3)
        self.historial.leaveEvent = lambda event: self.update_button_style(self.historial, 'white',
                                                                           'fa.history', 1.3)

        self.historial.clicked.connect(self.show1)

        self.content_layout.addWidget(self.historial)

        self.content_layout.setSpacing(15)

        spacer = QSpacerItem(30, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.content_layout.addItem(spacer)
        # Agregar el botón de "Salir" al final
        self.logout_button = QPushButton()
        self.logout_button.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: white;
                border: none;
                padding: 10px;
                text-align: center;
                font-size: {self.text_scale};
                border-radius: 5px;
                 font-weight: bold;
                        font: Open Sans;

            }}
            QPushButton:hover {{
                background-color: white;
            }}
        """)
        self.logout_button.setIcon(icon('fa.sign-out', color="white", scale_factor=1.3))
        self.logout_button.setIconSize(QSize(24, 24))
        self.logout_button.clicked.connect(self.logout)
        self.logout_button.enterEvent = lambda event: self.update_button_style(self.logout_button, '#6778D2',
                                                                               'fa.sign-out', 1.3)
        self.logout_button.leaveEvent = lambda event: self.update_button_style(self.logout_button, 'white',
                                                                               'fa.sign-out', 1.3)

        self.content_layout.addWidget(self.logout_button)

        self.layout.addWidget(self.content_frame)
        self.animation = QPropertyAnimation(self, b"maximumWidth")
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.is_expanded = False

    def logout(self):
        self.parent().show_logout_confirmation()

    def update_button_style(self, button, text_color, icon_name, escala):
        button.setStyleSheet(f"""
              QPushButton {{
                  background-color: transparent;
                  color: {text_color};
                  border: none;
                  padding: 10px;
                  text-align: center;
                  font-size: {self.text_scale};
                  border-radius: 5px;
                  font-weight: bold;
                  font: Open Sans;
              }}
              QPushButton:hover {{
                  background-color: white;
                  color: #6778D2;
              }}
          """)
        button.setIcon(icon(icon_name, color=text_color, scale_factor=escala))

    def go_back(self):
        self.settings_button.setEnabled(True)
        self.is_settings_selected = False
        self.is_history_selected = False
        self.historial.setEnabled(True)

        self.update_settings_button_style()
        self.parent().stacked_layout.setCurrentIndex(0)

    def show_settings_screen(self):
        self.settings_button.setEnabled(False)
        self.historial.setEnabled(True)

        self.is_history_selected = False
        self.update_settings_button_style()
        self.parent().stacked_layout.setCurrentIndex(1)

    def show1(self):
        try:
            self.historial.setEnabled(False)
            self.settings_button.setEnabled(True)
            self.is_settings_selected = False

            self.is_history_selected = True
            self.update_historial_button_style()
            self.parent().stacked_layout.setCurrentIndex(2)  # Asumiendo que el historial será el índice 2

        except Exception as e:
            print(f"Error al mostrar el historial: {e}")

    def update_historial_button_style(self):
        if self.is_history_selected:
            self.historial.setStyleSheet("""
                QPushButton {
                     background-color: #ADCDF4;
                    color: white;
                    border: none;
                    padding: 10px;
                    text-align: left;
                    font-size: 12px;
                    border-radius: 5px;
                    font: Open Sans;
                }
                QPushButton:hover {
                    background-color: #4C6FD5;
                }
            """)
        else:
            self.historial.setStyleSheet("""
                QPushButton {
                  background-color: transparent;
                    color: white;
                    border: none;
                    padding: 10px;
                    text-align: left;
                    font-size: 12px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: white;
                }
            """)

    def update_settings_button_style(self):
        if self.is_settings_selected:
            self.settings_button.setStyleSheet("""
                QPushButton {
                    background-color: #ADCDF4;
                    color: white;
                    border: none;
                    padding: 10px;
                    text-align: center;
                    font-size: 15px;
                    border-radius: 5px;
                    font: Open Sans;

                }
                QPushButton:hover {
                    background-color: #4C6FD5;
                }
            """)
        else:
            self.settings_button.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: white;
                    border: none;
                    padding: 10px;
                    text-align: center;
                    font-size: 15px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: white;
                }
            """)

    def toggle_sidebar(self):
        if self.is_expanded:
            self.collapse()
        else:
            self.expand()

    def expand(self):

        self.is_expanded = True
        self.image_label.setVisible(False)
        self.image_label2.setVisible(True)

        self.animation.setStartValue(self.width())
        self.animation.setEndValue(500)
        self.animation.start()

        self.toggle_button.setStyleSheet(""" QPushButton {
                         background-color: transparent;
                         color: black;
                         border: none;
                         padding: 10px;
                         text-align: right;
                         font-size: 96px;
                         border-radius: 3px;
                         font: Open Sans;

                     } 
                     QPushButton:hover {
                        background-color: white;
                    }
                     """)

        self.toggle_button.leaveEvent = lambda event: self.toggle_button.setIcon(
            icon('mdi.menu-down', color='purple', scale_factor=1.5))

        self.settings_button.setText("Configuración")
        self.home_button.setText("Inicio")
        self.historial.setText("Historial")
        self.logout_button.setText("Salir")

    def collapse(self):
        print("Collapsing sidebar")
        self.is_expanded = False
        self.image_label.setVisible(True)  # Muestra la imagen cuando la barra lateral está expandida
        self.image_label2.setVisible(False)  # Muestra la imagen cuando la barra lateral está expandida

        self.animation.setStartValue(self.width())
        self.animation.setEndValue(80)
        self.animation.start()
        self.toggle_button.setStyleSheet(""" QPushButton {
                                 background-color: transparent;
                                 color: black;
                                 border: none;
                                 padding: 10px;
                                 text-align: center;
                                 font-size: 16px;
                                 border-radius: 3px;
                                                         font: Open Sans;

                             }
                               QPushButton:hover {
                background-color: white;
            }""")

        self.toggle_button.leaveEvent = lambda event: self.toggle_button.setIcon(
            icon('mdi.menu', color='white', scale_factor=1.5))

        self.settings_button.setText("")
        self.home_button.setText("")
        self.historial.setText("")
        # self.back_button.setText("")
        self.logout_button.setText("")

