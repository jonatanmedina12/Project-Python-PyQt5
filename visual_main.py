import qtawesome as qta
from PyQt5.QtCore import QSize, QEvent, Qt
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QStackedLayout, QMessageBox

from Visual_element.settingsHistory.historial import Historial
from Visual_element.sidebar import SideBar
from Visual_element.settings import SettingsScreen
from Visual_element.inicio import Dashboard
from SqlLiteData.sqlLogic import sqlConfiguration


class ConfirmationDialog(QMessageBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        try:
            self.setWindowTitle("Cerrar")
            self.setText("¿Estás seguro de que desea cerrar el aplicativo?")
            self.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            self.setDefaultButton(QMessageBox.No)

            # Agregar icono de salir usando qtawesome
            logout_icon = qta.icon('fa5s.sign-out-alt', color='red', color_bg='transparent')

            self.setIconPixmap(logout_icon.pixmap(QSize(48, 48)))

            # Aplicar estilos al cuadro de diálogo y los botones
            self.setStyleSheet("""
                     ConfirmationDialog {
                         background-color: #FFFFFF;
                         color: #333333;
                         font-family: Arial;
                         font-size: 14px;
                         border: 1px solid #CCCCCC;
                         border-radius: 5px;
                     }
                     ConfirmationDialog QLabel {
                         color: black;
                         background-color: #FFFFFF;

                     }

                 """)

            # Personalizar los botones
            yes_button = self.button(QMessageBox.Yes)
            yes_button.setText("Salir")
            yes_icon = qta.icon('fa5s.check', color='white')
            yes_button.setIcon(yes_icon)
            yes_button.setStyleSheet("""
                     QPushButton {
                         background-color: #4CAF50;
                         color: white;
                         border: none;
                         padding: 10px 20px;
                         font-size: 16px;
                         font-weight: bold;
                         border-radius: 5px;
                     }
                     QPushButton:hover {
                         background-color: #45a049;
                     }
                     QPushButton:pressed {
                         background-color: #3e8e41;
                     }
                 """)

            no_button = self.button(QMessageBox.No)
            no_button.setText("Cancelar")
            no_icon = qta.icon('fa5s.times', color='white')
            no_button.setIcon(no_icon)
            no_button.setStyleSheet("""
                     QPushButton {
                         background-color: #f44336;
                         color: white;
                         border: none;
                         padding: 10px 20px;
                         font-size: 16px;
                         font-weight: bold;
                         border-radius: 5px;
                     }
                     QPushButton:hover {
                         background-color: #e53935;
                     }
                     QPushButton:pressed {
                         background-color: #c62828;
                     }
                 """)
        except Exception as e:
            print(e)


class Background(QWidget):
    def __init__(self):
        super().__init__()
        try:
            self.setWindowTitle("INTERFACE")
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
            self.setStyleSheet("background-color: #fff;")

            # Ajustar el tamaño de la ventana inicialmente
            self.adjustWindowSize()

            self.sidebar = SideBar(self)

            self.stacked_layout = QStackedLayout()
            self.stacked_layout2 = QStackedLayout()

            self.dashboard = Dashboard(self)
            self.stacked_layout.addWidget(self.dashboard)

            self.settings_screen = SettingsScreen(self)
            self.stacked_layout.addWidget(self.settings_screen)

            self.historial_screen = Historial(self)  # Crea una instancia de Historial
            self.stacked_layout.addWidget(self.historial_screen)  # Agrega Historial al stacked_layout

            self.layout = QHBoxLayout()
            self.layout.setContentsMargins(0, 0, 0, 0)
            self.layout.setSpacing(0)
            self.layout.addWidget(self.sidebar)
            self.layout.addLayout(self.stacked_layout)

            self.setLayout(self.layout)
        except Exception as e:
            print(e)

    def adjustWindowSize(self):
        try:
            # Obtener la información de la pantalla actual
            screen = QGuiApplication.screenAt(self.pos())
            if screen:
                screen_rect = screen.geometry()
                screen_width = screen_rect.width()
                screen_height = screen_rect.height()

                # Calcular el tamaño de la ventana en función del tamaño de la pantalla
                window_width = int(screen_width * 0.5)  # Ancho del 80% del tamaño de la pantalla
                window_height = int(screen_height * 0.6)  # Alto del 80% del tamaño de la pantalla

                # Calcular la posición de la ventana para centrarla en la pantalla
                window_x = (screen_width - window_width) // 2
                window_y = (screen_height - window_height) // 2

                # Establecer la geometría de la ventana
                self.setGeometry(window_x, window_y, window_width, window_height)
                self.setFixedSize(self.size())

        except Exception as e:
            print(e)

    def closeEvent(self, event):
        try:
            confirmation = ConfirmationDialog(self)
            result = confirmation.exec_()
            if result == QMessageBox.Yes:
                event.accept()
                QApplication.quit()
            else:
                event.ignore()
        except Exception as e:
            print(e)

    def event(self, event):
        try:
            if event.type() == QEvent.WindowStateChange:
                if self.isMaximized():
                    self.adjust_font_size(True)
                else:
                    self.adjust_font_size(False)
            return super().event(event)
        except Exception as e:
            print(e)

    def adjust_font_size(self, is_maximized):
        try:
            self.settings_screen.adjust_font_size(is_maximized)

        except Exception as e:
            print(e)

    def show_logout_confirmation(self):
        try:
            confirmation = ConfirmationDialog(self)
            result = confirmation.exec_()
            if result == QMessageBox.Yes:
                # Realizar acciones de cierre de sesión, como borrar tokens, restablecer estados, etc.
                # Cerrar la ventana principal de la aplicación
                QApplication.quit()
        except Exception as e:
            print(e)


if __name__ == "__main__":
    import sys

    sqlconnect = sqlConfiguration("desarrollo4", "Colcan2024*")
    sqlconnect.create_connection()
    app = QApplication(sys.argv)
    background = Background()
    background.show()
    sys.exit(app.exec_())
