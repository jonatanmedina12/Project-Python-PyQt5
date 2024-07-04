from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTabWidget, QGroupBox
from Visual_element.settingslogic.settingsConfiguracion import Configuration
from Visual_element.parametrizacionlogic.parametrizacionLogic import Parametrization
from Visual_element.settingsDm.dmSettings import DmSettings
class SettingsScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        try:
            self.bidireccional_layout = None
            self.bidireccional_widget = None
            self.socket_layout = None
            self.socket_widget = None
            self.setStyleSheet("background-color: #FFFFFF;")
            layout = QVBoxLayout()
            self.setLayout(layout)

            self.title_label = QLabel("Configuración")
            self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
            layout.addWidget(self.title_label)

            self.tab_widget = QTabWidget()
            layout.addWidget(self.tab_widget)

            self.config_tab = QWidget()
            self.param_tab = QWidget()
            self.dm_tab = QWidget()

            self.tab_widget.addTab(self.config_tab, "Configuración")
            self.tab_widget.addTab(self.param_tab, "Parametrización")
            self.tab_widget.addTab(self.dm_tab, "Analizadores")
            self.tab_widget.setStyleSheet("""
                       QTabBar::tab {
                           background-color: #F5F7F9;
                           color: #333;
                           padding: 10px;
                           border-top-left-radius: 5px;
                           border-top-right-radius: 5px;
                           border: 1px solid #CCC;
                       }
                       QTabBar::tab:selected {
                           background-color: #597DFA;
                           color: white;
                       }
                   """)

            self.config_tab_layout = QVBoxLayout()
            self.config_tab.setLayout(self.config_tab_layout)
            self.config_tab_layout.setContentsMargins(10, 10, 10, 10)
            self.config_tab_layout.setSpacing(10)

            self.param_tab_layout = QVBoxLayout()
            self.param_tab.setLayout(self.param_tab_layout)
            self.param_tab_layout.setContentsMargins(10, 10, 10, 10)
            self.param_tab_layout.setSpacing(10)

            self.Dm_tab_layout = QVBoxLayout()
            self.dm_tab.setLayout(self.Dm_tab_layout)
            self.Dm_tab_layout.setContentsMargins(10, 10, 10, 10)
            self.Dm_tab_layout.setSpacing(10)

            self.config_group_box = QGroupBox("Configuración")
            self.param_group_box = QGroupBox("Parametrización")
            self.Dm_group_box = QGroupBox("Analizadores")
            self.config = Configuration(self, self.config_tab_layout)
            self.config_tab_layout.addWidget(self.config.endpoints_group_box)

            self.parametrizacion = Parametrization(self)
            self.param_tab_layout.addWidget(self.parametrizacion)

            self.Dmsettings = DmSettings(self)
            self.Dm_tab_layout.addWidget(self.Dmsettings)
        except Exception as e:
            print(e)


