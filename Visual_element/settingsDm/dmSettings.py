from PyQt5.QtWidgets import (QWidget, QLabel, QTableWidget, QVBoxLayout,
                             QTableWidgetItem, QHeaderView)
from SqlLiteData.sqlLogic import sqlConfiguration


class DmSettings(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.dm_tab_layout = QVBoxLayout(self)
        self.sql_config = sqlConfiguration("usuario", "contraseña")
        self.conn = self.sql_config.create_connection()

        try:
            self.setup_dm_tab()
        except Exception as e:
            print("Error en DmSettings:", e)

    def setup_dm_tab(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #F0F0F0;
                font-family: Arial, sans-serif;
            }
            QLabel {
                color: #333333;
            }
            QTableWidget {
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                background-color: white;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #597DFA;
                color: white;
            }
        """)

        title_label = QLabel("Métodos y Funciones Asociadas")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;background-color:none;")
        self.dm_tab_layout.addWidget(title_label)

        self.methods_table = QTableWidget()
        self.methods_table.setColumnCount(3)
        self.methods_table.setHorizontalHeaderLabels(["Método", "Función Asociada", "Estado"])
        self.methods_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.dm_tab_layout.addWidget(self.methods_table)

        self.load_methods_and_functions()

    def load_methods_and_functions(self):
        self.conn = self.sql_config.create_connection()

        main_endpoint, methods, functions = self.sql_config.load_configuration(self.conn)
        parametrization = self.sql_config.load_parametrization(self.conn)

        all_methods = []
        all_functions = []
        free_functions = ["Login", "Consulta", "Acuse", "Connect_Socket1", "Connect_Socket2"]

        # Añadir métodos y funciones de la configuración general
        if methods and functions:
            all_methods.extend(methods)
            all_functions.extend(functions)

        # Añadir métodos y funciones de la parametrización
        if parametrization:
            # Asumiendo que los índices 7 y 9 corresponden a funcion_socket1 y funcion_socket2
            if parametrization[7]:  # funcion_socket1
                all_methods.append(f"Socket 1: {parametrization[6]}")  # socket1
                all_functions.append(parametrization[7])  # funcion_socket1
            if parametrization[9]:  # funcion_socket2
                all_methods.append(f"Socket 2: {parametrization[8]}")  # socket2
                all_functions.append(parametrization[9])  # funcion_socket2

        # Verificar qué funciones libres no están siendo utilizadas
        unused_free_functions = [func for func in free_functions if func not in all_functions]

        # Añadir funciones libres no utilizadas
        all_methods.extend([""] * len(unused_free_functions))
        all_functions.extend(unused_free_functions)

        if all_methods and all_functions:
            self.methods_table.setRowCount(len(all_methods))
            for row, (method, function) in enumerate(zip(all_methods, all_functions)):
                self.methods_table.setItem(row, 0, QTableWidgetItem(method))
                self.methods_table.setItem(row, 1, QTableWidgetItem(function))
                if function in unused_free_functions:
                    self.methods_table.setItem(row, 2, QTableWidgetItem("Libre"))
                else:
                    self.methods_table.setItem(row, 2, QTableWidgetItem("Ocupado"))
        else:
            self.methods_table.setRowCount(0)
            print("No se encontraron métodos o funciones")

        # Añadir información del endpoint principal
        if main_endpoint:
            self.methods_table.insertRow(0)
            self.methods_table.setItem(0, 0, QTableWidgetItem("Endpoint Principal"))
            self.methods_table.setItem(0, 1, QTableWidgetItem(main_endpoint))
            self.methods_table.setItem(0, 2, QTableWidgetItem(""))

        if self.conn:
            self.conn.close()

    def update_view(self):
        self.load_methods_and_functions()

    def showEvent(self, event):
        super().showEvent(event)
        self.update_view()

    def closeEvent(self, event):
        if self.conn:
            self.conn.close()
        super().closeEvent(event)

    def closeEvent(self, event):
        if self.conn:
            self.conn.close()
        super().closeEvent(event)
