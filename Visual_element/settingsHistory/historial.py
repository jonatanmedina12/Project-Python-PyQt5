from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QTableWidget, QTableWidgetItem, QLineEdit,
                             QPushButton, QHeaderView, QDateEdit, QFrame, QToolButton,
                             QDialog, QSizePolicy, QTextEdit)
from PyQt5.QtCore import Qt, QDate, QTimer
from SqlLiteData.sqlLogic import sqlConfiguration

import qtawesome as qta


def parse_hl7_message(message):
    segments = message.strip().split('\r\n')
    parsed_data = []
    for segment in segments:
        if segment.strip():  # Asegurarse de que el segmento no esté vacío
            fields = segment.split('|')

            # Eliminar campos vacíos en cualquier posición
            fields = [field for field in fields if field.strip() != '']

            if fields:  # Solo añadir si quedan campos no vacíos
                parsed_data.append(fields)
    return parsed_data


class DetailDialog(QDialog):
    def __init__(self, parent=None, details=None, hl7_data=None, raw_hl7=None):
        super().__init__(parent)
        self.setWindowTitle("Detalles de la Trama")
        self.setMinimumSize(900, 700)
        self.hl7_data = hl7_data
        self.raw_hl7 = raw_hl7
        self.is_table_view = True

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Estilo general
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
                font-family: Arial, sans-serif;
            }
            QTableWidget {
                border: 1px solid #d0d0d0;
                border-radius: 5px;
                background-color: white;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #e0e0e0;
                padding: 5px;
                border: 1px solid #d0d0d0;
                font-weight: bold;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px 15px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
               QScrollBar:vertical {
                border: none;
                background: #f0f0f0;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #4CAF50;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical {
                height: 0px;
            }
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
            QScrollBar:horizontal {
                border: none;
                background: #f0f0f0;
                height: 10px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:horizontal {
                background: #4CAF50;
                min-width: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:horizontal {
                width: 0px;
            }
            QScrollBar::sub-line:horizontal {
                width: 0px;
            }
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: none;
            }
        """)

        # Detalles básicos
        self.details_table = QTableWidget(3, 2)
        self.details_table.setHorizontalHeaderLabels(["Campo", "Valor"])
        self.details_table.verticalHeader().setVisible(False)
        self.details_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.details_table.setMaximumHeight(150)
        self.details_table.setStyleSheet("QTableWidget { margin-bottom: 15px; }")
        self.details_table.setEditTriggers(QTableWidget.NoEditTriggers)  # Hacer la tabla no editable

        details_list = details.split('\n')
        for i, detail in enumerate(details_list[:3]):
            key, value = detail.split(': ', 1)
            key_item = QTableWidgetItem(key)
            value_item = QTableWidgetItem(value)
            key_item.setFlags(key_item.flags() & ~Qt.ItemIsEditable)
            value_item.setFlags(value_item.flags() & ~Qt.ItemIsEditable)
            self.details_table.setItem(i, 0, key_item)
            self.details_table.setItem(i, 1, value_item)
            self.details_table.item(i, 0).setBackground(QColor("#e0e0e0"))

        main_layout.addWidget(self.details_table)

        # Botón para cambiar la vista
        self.toggle_view_button = QPushButton("Ver Trama Completa")
        self.toggle_view_button.clicked.connect(self.toggle_view)
        main_layout.addWidget(self.toggle_view_button)

        # Contenedor para la vista de trama HL7
        self.hl7_view_container = QWidget()
        self.hl7_layout = QVBoxLayout(self.hl7_view_container)
        main_layout.addWidget(self.hl7_view_container, 1)

        # Inicializar con la vista de tabla
        self.show_table_view()

        # Botón de cerrar
        close_button = QPushButton("Cerrar")
        close_button.clicked.connect(self.close)
        close_button.setStyleSheet("background-color: #f44336;")
        main_layout.addWidget(close_button)

    def show_table_view(self):
        for i in reversed(range(self.hl7_layout.count())):
            self.hl7_layout.itemAt(i).widget().setParent(None)

        self.hl7_table = QTableWidget()
        self.hl7_table.setFont(QFont("Courier", 10))
        self.hl7_table.setEditTriggers(QTableWidget.NoEditTriggers)  # Hacer la tabla no editable
        self.populate_hl7_table(self.hl7_data)
        self.hl7_layout.addWidget(self.hl7_table)

    def show_raw_view(self):
        for i in reversed(range(self.hl7_layout.count())):
            self.hl7_layout.itemAt(i).widget().setParent(None)

        self.hl7_text = QTextEdit()
        self.hl7_text.setFont(QFont("Courier", 10))
        self.hl7_text.setPlainText(self.raw_hl7)
        self.hl7_text.setReadOnly(True)
        self.hl7_layout.addWidget(self.hl7_text)

    def toggle_view(self):
        self.is_table_view = not self.is_table_view
        if self.is_table_view:
            self.show_table_view()
            self.toggle_view_button.setText("Ver Trama Completa")
        else:
            self.show_raw_view()
            self.toggle_view_button.setText("Ver en Tabla")

    def populate_hl7_table(self, hl7_data):
        if not hl7_data:
            return

        max_cols = max(len(row) for row in hl7_data)
        self.hl7_table.setColumnCount(max_cols)
        self.hl7_table.setRowCount(len(hl7_data))

        headers = ['Tipo'] + [f'Datos Obtenidos {i}' for i in range(1, max_cols)]
        self.hl7_table.setHorizontalHeaderLabels(headers)

        for row, segment in enumerate(hl7_data):
            for col, field in enumerate(segment):
                item = QTableWidgetItem(field.strip())
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Hacer cada celda no editable
                self.hl7_table.setItem(row, col, item)
                if col == 0:  # Colorear la columna 'Tipo'
                    item.setBackground(QColor("#e0e0e0"))

        self.hl7_table.resizeColumnsToContents()
        self.hl7_table.resizeRowsToContents()
class Historial(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.sql_config = sqlConfiguration("desarrollo4", "Colcan2024*")
        self.conn = None
        self.current_page = 0
        self.items_per_page = 50
        self.search_text = ""
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("""
           QWidget {
            background-color: white;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 14px;
        }

        QLabel {
            color: #333333;
            margin-right: 5px;
        }

        QPushButton {
            background-color: #007BFF;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #0056b3;
        }

        QPushButton:disabled {
            background-color: #CCCCCC;
            color: #666666;
        }

        QLineEdit, QDateEdit {
            padding: 10px;
            border: 1px solid #E0E0E0;
            border-radius: 4px;
            background-color: white;
        }

        QLineEdit:focus, QDateEdit:focus {
            border-color: #007BFF;
        }

        QDateEdit {
            min-width: 110px;
        }

        QDateEdit::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: center right;
            width: 20px;
            border-left: 1px solid #E0E0E0;
            border-top-right-radius: 3px;
            border-bottom-right-radius: 3px;
        }

          QDateEdit::down-arrow {
            width: 16px;
            height: 16px;
        }

        QTableWidget {
            border: 1px solid #E0E0E0;
            background-color: white;
            alternate-background-color: #F5F5F5;
            gridline-color: #E0E0E0;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        QTableWidget::item {
            padding: 5px;
        }

        QHeaderView::section {
            background-color: white;
            padding: 5px;
            border: 2px solid #E0E0E0;
            font-weight: bold;
            text-transform: uppercase;
        }

        QFrame {
            border: 1px solid white;
            border-radius: 4px;
            background-color: white;
        }

        QVBoxLayout {
            margin-top: 20px;
            margin-bottom: 20px;
            margin-left: 40px;
            margin-right: 40px;
           background-color: black;
        }

        QHBoxLayout {
            spacing: 20px;
            background-color: white;
        }
        QLineEdit:focus, QDateEdit:focus {
            box-shadow: 0 4px 8px rgba(0, 123, 255, 0.2);
        }
        QLineEdit, QDateEdit {
            padding: 12px;
            border: 1px solid #BDBDBD;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        QDateEdit::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: center right;
            width: 24px;
            border-left: none;
            border-top-right-radius: 6px;
            border-bottom-right-radius: 6px;
            background-color: #007BFF;
        }

        QDateEdit::down-arrow {
            width: 16px;
            height: 16px;
        }

        QScrollBar:vertical {
            background-color: #F5F5F5;
            width: 12px;
            margin: 16px 0;
        }

        QScrollBar::handle:vertical {
            background-color: #E0E0E0;
            min-height: 20px;
            border-radius: 6px;
        }

        QScrollBar::handle:vertical:hover { 
            background-color: #BDBDBD;
        }

        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {
            background: none;
            height: 0;
        }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Título
        title_label = QLabel("Historial de acciones")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #333333; margin-bottom: 10px;")
        main_layout.addWidget(title_label)

        # Frame para búsqueda y filtros de fecha
        search_date_frame = QFrame()
        search_date_frame.setStyleSheet("background-color: white; padding: 10px; border-radius: 8px;")
        search_date_layout = QHBoxLayout(search_date_frame)
        search_date_layout.setSpacing(10)

        # Barra de búsqueda
        self.search_bar = QLineEdit()
        self.search_bar.returnPressed.connect(self.update_search)
        self.search_bar.textChanged.connect(self.start_search_timer)
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.setInterval(500)  # Tiempo de espera en milisegundos
        self.search_timer.timeout.connect(self.do_search)

        search_icon = qta.icon('fa5s.search', color='#3498DB')
        self.search_bar.addAction(search_icon, QLineEdit.LeadingPosition)
        search_date_layout.addWidget(self.search_bar, 1)

        # Filtros de fecha
        date_layout = QHBoxLayout()
        date_layout.setSpacing(5)

        from_date_layout = QHBoxLayout()
        from_date_layout.setSpacing(5)
        from_date_layout.addWidget(QLabel("Desde:"))
        self.date_from = QDateEdit()
        self.date_from.setDisplayFormat("dd/MM/yyyy")
        self.date_from.setCalendarPopup(True)
        self.date_from.setDate(QDate.currentDate().addDays(-30))
        self.date_from.dateChanged.connect(self.apply_filters)
        from_date_layout.addWidget(self.date_from)

        # Icono para "Desde"
        from_calendar_icon = QPushButton()
        from_calendar_icon.setIcon(qta.icon('fa5s.calendar-alt', color='#3498DB'))
        from_calendar_icon.setStyleSheet("""
                QPushButton {
                    border: none;
                    padding: 0px;
                    background-color: transparent;
                }
            """)
        from_calendar_icon.clicked.connect(self.date_from.calendarWidget().show)
        from_date_layout.addWidget(from_calendar_icon)
        date_layout.addLayout(from_date_layout)

        to_date_layout = QHBoxLayout()
        to_date_layout.setSpacing(5)
        to_date_layout.addWidget(QLabel("Hasta:"))
        self.date_to = QDateEdit()
        self.date_to.setDisplayFormat("dd/MM/yyyy")
        self.date_to.setCalendarPopup(True)
        self.date_to.setDate(QDate.currentDate())
        self.date_to.dateChanged.connect(self.apply_filters)
        to_date_layout.addWidget(self.date_to)

        to_calendar_icon = QPushButton()
        to_calendar_icon.setIcon(qta.icon('fa5s.calendar-alt', color='#3498DB'))
        to_calendar_icon.setStyleSheet("""
              QPushButton {
                  border: none;
                  padding: 0px;
                  background-color: transparent;
              }
          """)
        to_calendar_icon.clicked.connect(self.date_to.calendarWidget().show)
        to_date_layout.addWidget(to_calendar_icon)

        date_layout.addLayout(to_date_layout)

        search_date_layout.addLayout(date_layout)
        main_layout.addWidget(search_date_frame)

        # Tabla de historial
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(4)  # Añadimos una columna extra para el botón
        self.history_table.setHorizontalHeaderLabels(["Fecha", "Acción", "Detalles", ""])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.history_table.setAlternatingRowColors(True)
        self.history_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.history_table.setSelectionMode(QTableWidget.SingleSelection)
        main_layout.addWidget(self.history_table)

        # Botones de navegación
        nav_layout = QHBoxLayout()
        self.prev_button = QPushButton("Anterior")
        self.prev_button.setIcon(qta.icon('fa5s.chevron-left'))
        self.prev_button.clicked.connect(self.load_previous_page)
        self.next_button = QPushButton("Siguiente")
        self.next_button.setIcon(qta.icon('fa5s.chevron-right'))
        self.next_button.clicked.connect(self.load_next_page)
        nav_layout.addWidget(self.prev_button)
        nav_layout.addWidget(self.next_button)
        main_layout.addLayout(nav_layout)

        self.setLayout(main_layout)
        self.set_sql_config()
        # Configurar el icono del calendario para QDateEdit
        calendar_icon = qta.icon('fa5s.calendar-alt', color='white')
        self.date_from.setCalendarPopup(True)
        self.date_from.calendarWidget().setWindowIcon(calendar_icon)
        self.date_to.setCalendarPopup(True)
        self.date_to.calendarWidget().setWindowIcon(calendar_icon)

        # Establecer el icono en el botón desplegable
        self.date_from.findChild(QToolButton).setIcon(calendar_icon)
        self.date_to.findChild(QToolButton).setIcon(calendar_icon)

    def load_history(self):
        try:
            if not self.conn or self.conn.total_changes == -1:
                self.conn = self.sql_config.create_connection()
                self.sql_config.create_history_table(self.conn)
            offset = self.current_page * self.items_per_page
            date_from = self.date_from.date().toString("yyyy-MM-dd")
            date_to = self.date_to.date().addDays(1).toString("yyyy-MM-dd")
            history_entries = self.sql_config.load_history(self.conn, self.items_per_page, offset, self.search_text,
                                                           date_from, date_to)
            self.history_table.setRowCount(len(history_entries))
            for row, entry in enumerate(history_entries):
                for col, value in enumerate(entry[:3]):  # Solo los primeros 3 campos visibles
                    item = QTableWidgetItem(str(value))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self.history_table.setItem(row, col, item)

                # Guardamos details_observer como datos del botón
                detail_button = QPushButton()
                detail_button.setIcon(qta.icon('fa5s.search'))
                detail_button.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        border: none;
                        padding: 5px;
                        border-radius: 15px;
                        transition: all 0.3s ease;
                        cursor: default;
                    }
                    QPushButton:hover {
                        background-color: #3E9AF0;
                        cursor: pointer;
                        transform: scale(1.1);
                        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                    }
                """)
                detail_button.clicked.connect(lambda _, r=row: self.show_details(r))
                detail_button.setProperty("details_observer", entry[3] if len(entry) > 3 else "")
                self.history_table.setCellWidget(row, 3, detail_button)

            self.prev_button.setEnabled(self.current_page > 0)
            self.next_button.setEnabled(len(history_entries) == self.items_per_page)
        except Exception as e:
            print(f"Error al cargar el historial: {e}")
            if self.conn:
                self.conn.close()
            self.conn = None

    def show_details(self, row):
        date = self.history_table.item(row, 0).text()
        action = self.history_table.item(row, 1).text()
        details = self.history_table.item(row, 2).text()
        details_observer = self.history_table.cellWidget(row, 3).property("details_observer")

        basic_details = f"Fecha: {date}\nAcción: {action}\nDetalles: {details}"

        # Parsear la trama HL7
        parsed_hl7 = parse_hl7_message(details_observer)

        dialog = DetailDialog(self, basic_details, parsed_hl7, details_observer)
        dialog.exec_()

    def start_search_timer(self, text):
        self.search_text = text
        self.search_timer.start()

    def do_search(self):
        self.current_page = 0
        self.load_history()

    def update_search(self):
        self.do_search()

    def apply_filters(self):
        self.current_page = 0
        self.load_history()

    def load_next_page(self):
        self.current_page += 1
        self.load_history()

    def load_previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.load_history()

    def closeEvent(self, event):
        if self.conn:
            self.conn.close()
        super().closeEvent(event)

    def set_sql_config(self):
        self.conn = self.sql_config.create_connection()
        if self.conn:
            self.sql_config.create_history_table(self.conn)
            self.sql_config.insert_test_data(self.conn)
            self.conn.close()
        self.conn = None
        self.current_page = 0
        self.load_history()

    def showEvent(self, event):
        super().showEvent(event)
        self.load_history()