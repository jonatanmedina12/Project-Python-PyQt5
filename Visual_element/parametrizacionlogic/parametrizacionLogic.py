from PyQt5.QtCore import QPropertyAnimation, Qt, QEasingCurve, QTimer
from PyQt5.QtWidgets import (QWidget, QFormLayout, QLineEdit, QComboBox,
                             QPushButton, QVBoxLayout, QFrame, QGraphicsOpacityEffect, QDialog, QLabel,
                             QHBoxLayout, QMessageBox)

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

        self.setFixedSize(180, 80)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.label)
        self.layout().setContentsMargins(0, 0, 0, 0)

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


class Parametrization(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.save_button = None
        self.sql_config = sqlConfiguration("usuario", "contraseña")
        self.conn = self.sql_config.create_connection()
        self.sql_config.create_parametrization_table(self.conn)
        try:
            self.setup_ui()
            self.fill_socket_functions()
            self.load_saved_parametrization()
        except Exception as e:
            print("Error en Parametrization:", e)

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        container = QFrame(self)
        container.setObjectName("main_container")
        container_layout = QVBoxLayout(container)

        form_layout = QFormLayout()
        container_layout.addLayout(form_layout)

        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 12px;
                background-color: white;
            }
            QLabel {
                color: #333;
            }
            QLineEdit, QComboBox {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 3px;
                background-color: white;
                min-height: 20px;
                max-height: 20px;
            }
            QLineEdit:focus, QComboBox:focus {
                border-color: #66afe9;
                outline: 0;
                box-shadow: inset 0 1px 1px rgba(0,0,0,.075), 0 0 8px rgba(102,175,233,.6);
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px;
                border-left: 1px solid #ccc;
            }
            QComboBox::down-arrow {
                width: 10px;
                height: 10px;
                image: url(down_arrow.png);
            }
            QPushButton {
                padding: 8px 20px;
                background-color: #5cb85c;
                color: white;
                border: none;
                border-radius: 3px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #4cae4c;
            }
            QPushButton:pressed {
                background-color: #449d44;
            }
            QFormLayout {
                spacing: 10px;
            }
            #main_container {
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: white;
                padding: 20px;
            }
        """)

        self.user_input = QLineEdit()
        form_layout.addRow("Usuario:", self.user_input)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Contraseña:", self.password_input)

        self.equipment_name_input = QLineEdit()
        form_layout.addRow("Nombre equipo:", self.equipment_name_input)

        self.connection_type = QComboBox()
        self.connection_type.addItem("Escoja una opción")
        self.connection_type.addItems(["Socket", "Puerto Serial"])
        self.connection_type.setCurrentIndex(0)
        self.connection_type.currentIndexChanged.connect(self.on_connection_type_changed)
        form_layout.addRow("Tipo de conexión:", self.connection_type)

        self.socket_widget = QWidget()
        self.socket_layout = QFormLayout(self.socket_widget)
        self.socket_layout.setContentsMargins(0, 0, 0, 0)

        self.direction_type = QComboBox()
        self.direction_type.addItem("Escoja una opción")
        self.direction_type.addItems(["Bidireccional", "Unidireccional"])
        self.direction_type.setCurrentIndex(0)
        self.direction_type.currentIndexChanged.connect(self.on_direction_type_changed)
        self.socket_layout.addRow("Dirección:", self.direction_type)

        self.ip_socket_widget = QWidget()
        self.ip_socket_layout = QFormLayout(self.ip_socket_widget)
        self.ip_socket_layout.setContentsMargins(0, 0, 0, 0)

        self.ip_input = QLineEdit()
        self.ip_input.textChanged.connect(self.check_fields)

        self.socket1_widget = QWidget()
        self.socket1_layout = QHBoxLayout(self.socket1_widget)
        self.socket1_layout.setContentsMargins(0, 0, 0, 0)
        self.socket_input1 = QLineEdit()
        self.socket_input1.textChanged.connect(self.check_fields)
        self.socket_function1 = QComboBox()
        self.socket_type1 = QComboBox()
        self.socket_type1.addItems(["Escoja una opción", "Envío de órdenes", "Envío de resultados"])
        self.socket1_layout.addWidget(QLabel(""))
        self.socket1_layout.addWidget(self.socket_input1)
        self.socket1_layout.addWidget(QLabel("Función:"))
        self.socket1_layout.addWidget(self.socket_function1)
        self.socket1_layout.addWidget(QLabel("Tipo:"))
        self.socket1_layout.addWidget(self.socket_type1)



        self.socket2_widget = QWidget()
        self.socket2_layout = QHBoxLayout(self.socket2_widget)
        self.socket2_layout.setContentsMargins(0, 0, 0, 0)
        self.socket_input2 = QLineEdit()
        self.socket_input2.textChanged.connect(self.check_fields)
        self.socket_function2 = QComboBox()
        self.socket_type2 = QComboBox()
        self.socket_type2.addItems(["Escoja una opción","Envío de órdenes", "Envío de resultados"])
        self.socket2_layout.addWidget(QLabel(""))
        self.socket2_layout.addWidget(self.socket_input2)
        self.socket2_layout.addWidget(QLabel("Función:"))
        self.socket2_layout.addWidget(self.socket_function2)
        self.socket2_layout.addWidget(QLabel("Tipo:"))
        self.socket2_layout.addWidget(self.socket_type2)



        self.ip_socket_layout.addRow("IP:", self.ip_input)
        self.ip_socket_layout.addRow("Socket 1:", self.socket1_widget)
        self.ip_socket_layout.addRow("Socket 2:", self.socket2_widget)

        self.socket_layout.addRow(self.ip_socket_widget)
        self.ip_socket_widget.hide()

        self.socket_widget.hide()
        form_layout.addRow(self.socket_widget)

        self.socket_mode_widget = QWidget()
        self.socket_mode_layout = QHBoxLayout(self.socket_mode_widget)
        self.socket_mode_layout.setContentsMargins(0, 0, 0, 0)
        self.socket_mode = QComboBox()
        self.socket_mode.addItems(["Escoja una opción","Cliente", "Servidor"])
        self.socket_mode_layout.addWidget(QLabel("Modo:"))
        self.socket_mode_layout.addWidget(self.socket_mode)
        self.socket_mode_layout.addStretch(1)

        self.socket_layout.addRow(self.socket_mode_widget)


        self.serial_widget = QWidget()
        self.serial_layout = QFormLayout(self.serial_widget)
        self.serial_layout.setContentsMargins(0, 0, 0, 0)

        self.port_name = QLineEdit()
        self.port_name.textChanged.connect(self.check_fields)

        self.baud_rate = QComboBox()
        self.baud_rate.addItems(["9600", "19200", "38400", "57600", "115200"])
        self.data_bits = QComboBox()
        self.data_bits.addItems(["5", "6", "7", "8"])
        self.parity = QComboBox()
        self.parity.addItems(["None", "Even", "Odd", "Mark", "Space"])
        self.stop_bits = QComboBox()
        self.stop_bits.addItems(["1", "1.5", "2"])

        self.serial_layout.addRow("Puerto:", self.port_name)
        self.serial_layout.addRow("Baudios:", self.baud_rate)
        self.serial_layout.addRow("Bits de datos:", self.data_bits)
        self.serial_layout.addRow("Paridad:", self.parity)
        self.serial_layout.addRow("Bits de parada:", self.stop_bits)

        self.serial_widget.hide()
        form_layout.addRow(self.serial_widget)

        self.save_button = QPushButton("Guardar")
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
        self.save_button.clicked.connect(self.on_save_button_clicked)
        container_layout.addWidget(self.save_button)

        main_layout.addWidget(container)
        main_layout.setContentsMargins(20, 20, 20, 20)

        self.user_input.textChanged.connect(self.check_fields)
        self.password_input.textChanged.connect(self.check_fields)
        self.equipment_name_input.textChanged.connect(self.check_fields)
        self.connection_type.currentIndexChanged.connect(self.check_fields)
        self.socket_function1.currentIndexChanged.connect(self.check_socket_functions)
        self.socket_function2.currentIndexChanged.connect(self.check_socket_functions)
        self.socket_mode.currentIndexChanged.connect(self.check_fields)
        self.socket_type2.currentIndexChanged.connect(self.check_fields)
        self.socket_type1.currentIndexChanged.connect(self.check_fields)

    def on_connection_type_changed(self, index):
        if index == 0:
            self.socket_widget.hide()
            self.serial_widget.hide()
        elif self.connection_type.currentText() == "Socket":
            self.socket_widget.show()
            self.serial_widget.hide()
            self.direction_type.setCurrentIndex(0)
            self.ip_socket_widget.hide()
            # Limpiar campos del puerto serial
            self.port_name.clear()
            self.baud_rate.setCurrentIndex(0)
            self.data_bits.setCurrentIndex(0)
            self.parity.setCurrentIndex(0)
            self.stop_bits.setCurrentIndex(0)
            self.socket_mode.setCurrentIndex(0)  # Restablecer el valor de socket_mode

        else:
            self.socket_widget.hide()
            self.serial_widget.show()
            # Limpiar campos del socket
            self.ip_input.clear()
            self.socket_input1.clear()
            self.socket_input2.clear()
            self.socket_function1.setCurrentIndex(0)
            self.socket_function2.setCurrentIndex(0)
            self.socket_mode.setCurrentIndex(0)  # Restablecer el valor de socket_mode

        self.check_fields()

    def on_direction_type_changed(self, index):
        if index == 0:
            self.ip_socket_widget.hide()
        else:
            self.ip_socket_widget.show()
            if self.direction_type.currentText() == "Bidireccional":
                self.socket2_widget.show()
                self.ip_socket_layout.labelForField(self.socket2_widget).show()
            else:
                self.socket2_widget.hide()
                self.ip_socket_layout.labelForField(self.socket2_widget).hide()
        self.check_fields()

    def fill_socket_functions(self):
        functions = ["Escoja una opción", "Connect_Socket1", "Connect_Socket2"]
        self.socket_function1.addItems(functions)
        self.socket_function2.addItems(functions)
        self.socket_function1.setCurrentIndex(0)
        self.socket_function2.setCurrentIndex(0)

    def check_fields(self):
        errors = self.validate_inputs()
        self.save_button.setEnabled(len(errors) == 0)

    def check_socket_functions(self):
        if (self.socket_function1.currentText() == self.socket_function2.currentText() and
                self.socket_function1.currentText() != "Escoja una opción" and
                self.direction_type.currentText() == "Bidireccional"):
            QMessageBox.warning(self, "Error", "Las funciones de Socket 1 y Socket 2 no pueden ser iguales.")
        else:
            self.check_fields()

    def validate_inputs(self):
        errors = []
        self.remove_field_highlights()  # Limpia los resaltados anteriores

        if not self.user_input.text().strip():
            errors.append("El campo Usuario no puede estar vacío.")
            self.highlight_field(self.user_input)
        if not self.password_input.text().strip():
            errors.append("El campo Contraseña no puede estar vacío.")
            self.highlight_field(self.password_input)
        if not self.equipment_name_input.text().strip():
            errors.append("El campo Nombre equipo no puede estar vacío.")
            self.highlight_field(self.equipment_name_input)

        if self.connection_type.currentText() == "Escoja una opción":
            errors.append("Debe seleccionar un tipo de conexión.")
            self.highlight_field(self.connection_type)
        elif self.connection_type.currentText() == "Socket":

            if self.socket_mode.currentText() == "Escoja una opción":
                errors.append("Debe seleccionar un modo para la conexión Socket.")
                self.highlight_field(self.socket_mode)



            if self.direction_type.currentText() == "Escoja una opción":
                errors.append("Debe seleccionar una dirección para la conexión Socket.")
                self.highlight_field(self.direction_type)


            if self.socket_type1.currentText() == "Escoja una opción":
                errors.append("Debe seleccionar un tipo para Socket 1.")
                self.highlight_field(self.socket_type1)

            if not self.ip_input.text().strip():
                errors.append("El campo IP no puede estar vacío.")
                self.highlight_field(self.ip_input)
            elif not self.is_valid_ip(self.ip_input.text().strip()):
                errors.append("La dirección IP no es válida.")
                self.highlight_field(self.ip_input)
            if not self.socket_input1.text().strip():
                errors.append("El campo Socket 1 no puede estar vacío.")
                self.highlight_field(self.socket_input1)
            elif not self.is_valid_port(self.socket_input1.text()):
                errors.append("El puerto del Socket 1 no es válido.")
                self.highlight_field(self.socket_input1)
            if self.socket_function1.currentText() == "Escoja una opción":
                errors.append("Debe seleccionar una función para Socket 1.")
                self.highlight_field(self.socket_function1)
            if self.direction_type.currentText() == "Bidireccional":

                if self.socket_type2.currentText() == "Escoja una opción":
                    errors.append("Debe seleccionar un tipo para Socket 2.")
                    self.highlight_field(self.socket_type2)

                if not self.socket_input2.text().strip():
                    errors.append("El campo Socket 2 no puede estar vacío para conexión bidireccional.")
                    self.highlight_field(self.socket_input2)
                elif not self.is_valid_port(self.socket_input2.text()):
                    errors.append("El puerto del Socket 2 no es válido.")
                    self.highlight_field(self.socket_input2)
                if self.socket_function2.currentText() == "Escoja una opción":
                    errors.append("Debe seleccionar una función para Socket 2.")
                    self.highlight_field(self.socket_function2)
                if self.socket_input1.text() == self.socket_input2.text():
                    errors.append("Los puertos de Socket 1 y Socket 2 no pueden ser iguales.")
                    self.highlight_field(self.socket_input1)
                    self.highlight_field(self.socket_input2)

                if (self.socket_function1.currentText() != "Escoja una opción" and
                        self.socket_function2.currentText() != "Escoja una opción" and
                        self.socket_function1.currentText() == self.socket_function2.currentText()):
                    errors.append("Las funciones de Socket 1 y Socket 2 no pueden ser iguales.")
                    self.highlight_field(self.socket_function1)
                    self.highlight_field(self.socket_function2)
        elif self.connection_type.currentText() == "Puerto Serial":
            if not self.port_name.text().strip():
                errors.append("El campo Puerto no puede estar vacío.")
                self.highlight_field(self.port_name)

        return errors

    @staticmethod
    def highlight_field(field):
        field.setStyleSheet("border: 2px solid red;")

    @staticmethod
    def is_valid_ip(ip):
        try:
            parts = ip.split(".")
            if len(parts) != 4:
                return False
            for item in parts:
                int_item = int(item)
                if not 0 <= int_item <= 255:
                    print(f"Part {int_item} is not between 0 and 255")
                    return False
            return True
        except ValueError as e:
            print(f"Error validating IP: {e}")
            return False

    @staticmethod
    def is_valid_port(port):
        try:
            port_num = int(port)
            return 0 < port_num < 65536
        except ValueError:
            return False

    def on_save_button_clicked(self):
        errors = self.validate_inputs()
        if errors:
            error_message = "\n".join(errors)
            QMessageBox.warning(self, "Error de validación", error_message)
        else:
            dialog = SaveDialog(self)
            dialog.exec_()
            self.save_parametrization()
            QMessageBox.information(self, "Éxito", "Los parámetros se han guardado correctamente.")
            self.remove_field_highlights()

    def highlight_empty_fields(self):
        style = "border: 1px solid red;"

        if not self.user_input.text().strip():
            self.user_input.setStyleSheet(style)
        if not self.password_input.text().strip():
            self.password_input.setStyleSheet(style)
        if not self.equipment_name_input.text().strip():
            self.equipment_name_input.setStyleSheet(style)

        if self.connection_type.currentText() == "Escoja una opción":
            self.connection_type.setStyleSheet(style)
        elif self.connection_type.currentText() == "Socket":
            if self.direction_type.currentText() == "Escoja una opción":
                self.direction_type.setStyleSheet(style)
            if not self.ip_input.text().strip():
                self.ip_input.setStyleSheet(style)
            if not self.socket_input1.text().strip():
                self.socket_input1.setStyleSheet(style)
            if self.direction_type.currentText() == "Bidireccional":
                if not self.socket_input2.text().strip():
                    self.socket_input2.setStyleSheet(style)
                if self.socket_input1.text() == self.socket_input2.text():
                    self.highlight_field(self.socket_input1)
                    self.highlight_field(self.socket_input2)

        elif self.connection_type.currentText() == "Puerto Serial":
            if not self.port_name.text().strip():
                self.port_name.setStyleSheet(style)

    def remove_field_highlights(self):
        fields = [
            self.user_input, self.password_input, self.equipment_name_input,
            self.connection_type, self.direction_type, self.ip_input,
            self.socket_input1, self.socket_input2, self.socket_function1,
            self.socket_function2, self.port_name, self.baud_rate,
            self.data_bits, self.parity, self.stop_bits,self.socket_mode,
            self.socket_type1, self.socket_type2
        ]
        for field in fields:
            field.setStyleSheet("")

    def save_parametrization(self):
        params = (
            self.user_input.text(),
            self.password_input.text(),
            self.equipment_name_input.text(),
            self.connection_type.currentText(),
            self.direction_type.currentText() if self.connection_type.currentText() == "Socket" else "",
            self.ip_input.text() if self.connection_type.currentText() == "Socket" else "",
            self.socket_input1.text() if self.connection_type.currentText() == "Socket" else "",
            self.socket_function1.currentText() if self.connection_type.currentText() == "Socket" else "",
            self.socket_type1.currentText() if self.connection_type.currentText() == "Socket" else "",
            self.socket_input2.text() if self.connection_type.currentText() == "Socket" and self.direction_type.currentText() == "Bidireccional" else "",
            self.socket_function2.currentText() if self.connection_type.currentText() == "Socket" and self.direction_type.currentText() == "Bidireccional" else "",
            self.socket_type2.currentText() if self.connection_type.currentText() == "Socket" and self.direction_type.currentText() == "Bidireccional" else "",
            self.socket_mode.currentText() if self.connection_type.currentText() == "Socket" else "",
            self.port_name.text() if self.connection_type.currentText() == "Puerto Serial" else "",
            self.baud_rate.currentText() if self.connection_type.currentText() == "Puerto Serial" else "",
            self.data_bits.currentText() if self.connection_type.currentText() == "Puerto Serial" else "",
            self.parity.currentText() if self.connection_type.currentText() == "Puerto Serial" else "",
            self.stop_bits.currentText() if self.connection_type.currentText() == "Puerto Serial" else ""
        )

        self.sql_config.save_parametrization(self.conn, params)

    def load_saved_parametrization(self):
        params = self.sql_config.load_parametrization(self.conn)
        print(params)
        if params:
            self.user_input.setText(params[0])
            self.password_input.setText(params[1])
            self.equipment_name_input.setText(params[2])
            self.connection_type.setCurrentText(params[3])

            if params[3] == "Socket":
                self.direction_type.setCurrentText(params[4])
                self.ip_input.setText(params[5])
                self.socket_input1.setText(params[6])
                self.socket_function1.setCurrentText(params[7])
                self.socket_type1.setCurrentText(params[8])
                self.socket_input2.setText(params[9])
                self.socket_function2.setCurrentText(params[10])
                self.socket_type2.setCurrentText(params[11])
                self.socket_mode.setCurrentText(params[12])

            elif params[3] == "Puerto Serial":
                self.port_name.setText(params[13])
                self.baud_rate.setCurrentText(params[14])
                self.data_bits.setCurrentText(params[15])
                self.parity.setCurrentText(params[16])
                self.stop_bits.setCurrentText(params[17])

            self.check_fields()

    def closeEvent(self, event):
        if self.conn:
            self.conn.close()
        super().closeEvent(event)
