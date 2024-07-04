from PyQt5.QtCore import QTimer, Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtWidgets import QWidget, QGroupBox, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, \
    QScrollArea, QSpacerItem, QSizePolicy, QDialog, QMessageBox, QGraphicsOpacityEffect, QComboBox
from SqlLiteData.sqlLogic import sqlConfiguration


class SaveDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Guardando...")

        self.label = QLabel("Guardando...")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #FFFFFF;
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #15E0D5, stop:1 #6778D2);
            border-radius: 15px;
            padding: 20px;
        """)

        # Ajusta el tamaño del diálogo al tamaño del label
        self.setFixedSize(180, 80)

        # Configura el label como widget central
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.label)
        self.layout().setContentsMargins(0, 0, 0, 0)

        # Hace que el fondo del diálogo sea transparente
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)

        self.opacity_effect = QGraphicsOpacityEffect()
        self.label.setGraphicsEffect(self.opacity_effect)

        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(1000)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.start()

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.close_with_fade)
        self.timer.start(2000)

    def close_with_fade(self):
        self.animation.setDirection(QPropertyAnimation.Backward)
        self.animation.finished.connect(self.accept)
        self.animation.start()


class Configuration(QWidget):
    def __init__(self, parent, config_tab_layout):
        super().__init__(parent)
        self.save_button = None
        self.methods_layout = None
        self.methods_widget = None
        self.add_method_button = None
        self.main_endpoint_input = None
        self.main_endpoint_label = None
        self.main_endpoint_layout = None
        self.endpoints_layout = None
        self.endpoints_group_box = None
        self.methods_scroll_area = None
        self.configSql = sqlConfiguration("desarrollo4", "Colcan2024*")
        self.method_widgets = []  # Lista para almacenar los widgets de método
        self.endpointOriginal = None
        self.predefined_functions = [
            "Escoja una opción",
            "Login", "Consulta", "Acuse"
        ]
        try:
            self.config_tab_layout = config_tab_layout
            self.setup_ui()
            self.load_data()
        except Exception as e:
            print("aaaa", e)

    def setup_ui(self):
        try:
            self.setStyleSheet("""
                QGroupBox {
                    font-weight: bold;
                    margin-top: 10px;
                }
                QLineEdit {
                    padding: 5px;
                    border: 1px solid #ccc;
                    border-radius: 3px;
                    margin-bottom: 5px;
                }
                QPushButton {
                    padding: 5px 10px;
                    background-color: #597DFA;
                    color: white;
                    border: none;
                    border-radius: 3px;
                    margin-top: 10px;
                }
                QPushButton:hover {
                    background-color: #4C6BD6;
                }
                QFrame {
                    border: none;
                    border-bottom: 1px solid #ccc;
                    margin-bottom: 10px;
                }
            """)

            # Agregar sección de endpoints
            self.endpoints_group_box = QGroupBox("Endpoints")
            self.endpoints_layout = QVBoxLayout()
            self.endpoints_group_box.setLayout(self.endpoints_layout)

            # Agregar input para el endpoint principal y botón "Agregar método"
            self.main_endpoint_layout = QHBoxLayout()
            self.main_endpoint_label = QLabel("Endpoint principal:")
            self.main_endpoint_input = QLineEdit()
            self.main_endpoint_input.setText("https://api.example.com/v1")  # Ejemplo de endpoint principal
            self.main_endpoint_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.add_method_button = QPushButton("Agregar método")
            self.add_method_button.clicked.connect(self.add_method)
            self.add_method_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.add_method_button.setStyleSheet("""
                QPushButton {
                    padding: 8px 16px;
                    background-color: #2196F3;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                    cursor: pointer;
                }
            """)
            self.main_endpoint_layout.addWidget(self.main_endpoint_label)
            self.main_endpoint_layout.addWidget(self.main_endpoint_input, stretch=3)
            self.main_endpoint_layout.addWidget(self.add_method_button, stretch=2)
            self.endpoints_layout.addLayout(self.main_endpoint_layout)

            self.main_endpoint_input.textChanged.connect(self.update_method_paths)

            # Agregar separador
            separator = QFrame()
            self.endpoints_layout.addWidget(separator)

            # Agregar sección para agregar métodos de endpoint
            self.methods_scroll_area = QScrollArea()
            self.methods_scroll_area.setWidgetResizable(True)
            self.methods_widget = QWidget()
            self.methods_layout = QVBoxLayout(self.methods_widget)
            self.methods_layout.setSpacing(5)  # Reducir el espacio entre los métodos
            self.methods_scroll_area.setWidget(self.methods_widget)
            self.endpoints_layout.addWidget(self.methods_scroll_area)

            # Agregar espaciador para empujar los métodos hacia arriba
            spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
            self.methods_layout.addItem(spacer)

            # Agregar botón de guardar con estilo
            self.save_button = QPushButton("Guardar")
            self.save_button.clicked.connect(self.save_configuration)
            self.save_button.setStyleSheet("""
                QPushButton {
                    padding: 8px 16px;
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #45a049;
                    cursor: pointer;
                }
            """)
            self.endpoints_layout.addWidget(self.save_button)
        except Exception as e:
            print("zzzzzz", e)

    def load_data(self):
        try:
            conn = self.configSql.create_connection()
            self.configSql.create_table(conn)
            print("Intentando cargar la configuración...")
            result = self.configSql.load_configuration(conn)

            print(f"Resultado de load_configuration: {result}")

            if result and len(result) == 3:
                main_endpoint, methods, functions = result
                print("Datos cargados:")
                print(f"Main Endpoint: {main_endpoint}")
                print(f"Methods: {methods}")
                print(f"Functions: {functions}")

                if main_endpoint:
                    self.main_endpoint_input.setText(main_endpoint)
                    self.endpointOriginal = main_endpoint

                if methods and functions:
                    for method, function in zip(methods, functions):
                        self.add_method(method, function)
                else:
                    print("No hay métodos o funciones para cargar")
            else:
                print("No se encontraron datos de configuración o los datos están incompletos")

            conn.close()
        except Exception as e:
            print("Error al cargar datos:", e)

    def add_method(self, method_text=None, function_text=None):
        try:
            method_count = len(self.method_widgets) + 1
            method_name = f"Método {method_count}"
            method_widget = QWidget()
            method_layout = QHBoxLayout(method_widget)
            method_label = QLabel(method_name + ":")

            # LineEdit para ingresar el método
            method_input = QLineEdit()
            if method_text:
                method_input.setText(method_text)
            else:
                method_input.setText(f"{self.main_endpoint_input.text()}/")

            # ComboBox para la función asociada
            function_combo = QComboBox()
            function_combo.addItems(self.predefined_functions)
            if function_text and function_text in self.predefined_functions:
                function_combo.setCurrentText(function_text)
            else:
                function_combo.setCurrentIndex(0)
            function_combo.setStyleSheet("""
                       QComboBox {
                           padding: 8px;
                           border: 1px solid #ccc;
                           border-radius: 4px;
                           background-color: white;
                           color: #333;
                       }
                       QComboBox::drop-down {
                           subcontrol-origin: padding;
                           subcontrol-position: top right;
                           width: 20px;
                           border-left-width: 1px;
                           border-left-color: #ccc;
                           border-left-style: solid;
                           border-top-right-radius: 4px;
                           border-bottom-right-radius: 4px;
                       }
                       QComboBox::down-arrow {
                           image: url(:/images/down_arrow.png);
                           width: 10px;
                           height: 10px;
                       }
                       QComboBox QAbstractItemView {
                           border: 1px solid #ccc;
                           selection-background-color: #007bff;
                           selection-color: white;
                       }
                   """)
            remove_button = QPushButton("Eliminar")
            remove_button.setStyleSheet("""
                QPushButton {
                    padding: 8px 16px;
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #45a049;
                    cursor: pointer;
                }
            """)
            remove_button.clicked.connect(lambda: self.remove_method(method_widget))

            method_layout.addWidget(method_label)
            method_layout.addWidget(method_input)
            method_layout.addWidget(function_combo)
            method_layout.addWidget(remove_button)

            self.methods_layout.insertWidget(self.methods_layout.count() - 1, method_widget)
            self.method_widgets.append(method_widget)

            # No llamar a update_database aquí, solo actualizar la interfaz
            # self.update_database()
        except Exception as e:
            print("Error al añadir método:", e)

    def update_method_paths(self, new_endpoint):
        try:
            for method_widget in self.method_widgets:
                method_layout = method_widget.layout()
                method_input = method_layout.itemAt(1).widget()

                # Simplemente establecer el nuevo endpoint, sin modificaciones
                method_input.setText(new_endpoint)
        except Exception as e:
            print(e)

    def validate_method_fields(self):
        methods_without_function = []
        used_functions = set()
        for index, method_widget in enumerate(self.method_widgets):
            method_layout = method_widget.layout()
            method_input = method_layout.itemAt(1).widget()
            function_combo = method_layout.itemAt(2).widget()
            method_text = method_input.text().strip()
            function_text = function_combo.currentText()

            if not method_text:
                return False, f"El método {index + 1} no puede estar vacío."

            if function_text == "Escoja una opción":
                methods_without_function.append(index + 1)
            elif function_text in used_functions:
                return False, f"La función '{function_text}' está asignada a más de un método."
            else:
                used_functions.add(function_text)

        return True, methods_without_function

    def validate_unique_urls(self):
        urls = []
        for method_widget in self.method_widgets:
            method_layout = method_widget.layout()
            method_input = method_layout.itemAt(1).widget()
            url = method_input.text().strip()
            if url in urls:
                return False, f"La URL '{url}' está duplicada."
            urls.append(url)
        return True, None

    def validate_main_endpoint(self):
        main_endpoint = self.main_endpoint_input.text().strip()
        if not main_endpoint:
            return False
        return True

    def remove_method(self, method_widget):
        try:
            if not self.check_last_method():
                self.methods_layout.removeWidget(method_widget)
                self.method_widgets.remove(method_widget)
                method_widget.deleteLater()
                self.update_database()
        except Exception as e:
            print(e)

    def check_last_method(self):
        return len(self.method_widgets) == 1

    def update_database(self):
        try:
            main_endpoint = self.main_endpoint_input.text()
            methods = []
            functions = []
            for method_widget in self.method_widgets:
                method_layout = method_widget.layout()
                method_input = method_layout.itemAt(1).widget()
                function_combo = method_layout.itemAt(2).widget()
                method = method_input.text()
                function = function_combo.currentText()
                methods.append(method)
                functions.append(function)

            print("Actualizando base de datos:")
            print(f"Main Endpoint: {main_endpoint}")
            print(f"Methods: {methods}")
            print(f"Functions: {functions}")

            conn = self.configSql.create_connection()
            self.configSql.save_configuration(conn, main_endpoint, methods, functions)
            conn.close()
            print("Base de datos actualizada")
        except Exception as e:
            print("Error al actualizar la base de datos:", e)

    def save_configuration(self):
        try:
            # Validar el endpoint principal
            if not self.validate_main_endpoint():
                self.main_endpoint_input.setText(self.endpointOriginal)
                QMessageBox.warning(self, "Error", "El campo 'Endpoint principal' no puede estar vacío.")
                return

            # Validar los campos de los métodos y las funciones
            is_valid, result = self.validate_method_fields()
            if not is_valid:
                QMessageBox.warning(self, "Error", result)
                return

            # Validar URLs únicas
            is_unique, error_message = self.validate_unique_urls()
            if not is_unique:
                QMessageBox.warning(self, "Error", error_message)
                return

            # Mostrar advertencia si hay métodos sin función seleccionada
            if isinstance(result, list) and result:  # result contiene la lista de métodos sin función
                methods_str = ", ".join(map(str, result))
                response = QMessageBox.question(self, "Advertencia",
                                                f"Los siguientes métodos  no tienen una función "
                                                f"seleccionada no se utilizara el método seleccionado numeros: {methods_str}. ¿Desea continuar?",
                                                QMessageBox.Yes | QMessageBox.No)
                if response == QMessageBox.No:
                    return

            # Actualizar la base de datos
            self.update_database()

            # Mostrar el diálogo modal
            save_dialog = SaveDialog(self)
            save_dialog.exec_()

            QMessageBox.information(self, "Éxito", "La configuración se ha guardado correctamente.")

        except Exception as e:
            print("Error al guardar la configuración:", e)
            QMessageBox.critical(self, "Error", f"No se pudo guardar la configuración: {str(e)}")
