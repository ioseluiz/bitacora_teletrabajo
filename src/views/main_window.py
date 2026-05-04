from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QGroupBox, QProgressBar, QMessageBox, QTextEdit,
    QComboBox, QFileDialog, QDialog, QFormLayout, QDialogButtonBox,
    QMenuBar, QMenu
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread
import datetime

class StandardTaskDialog(QDialog):
    def __init__(self, parent=None, tasks=None):
        super().__init__(parent)
        self.setWindowTitle("Gestionar Tareas Predefinidas")
        self.setMinimumSize(600, 400)
        from src.views.styles import LIGHT_STYLE
        self.setStyleSheet(LIGHT_STYLE)
        self._init_ui(tasks)

    def _init_ui(self, tasks):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        form_group = QGroupBox("Añadir Nueva Tarea Predefinida")
        form_layout = QFormLayout()
        self.input_desc = QLineEdit()
        self.input_duration = QLineEdit()
        self.input_duration.setPlaceholderText("Ej: 2.0 (Opcional)")
        self.input_resources = QLineEdit()
        
        form_layout.addRow("Descripción:", self.input_desc)
        form_layout.addRow("Horas Defecto:", self.input_duration)
        form_layout.addRow("Recursos Defecto:", self.input_resources)
        
        self.btn_save = QPushButton("Guardar Tarea")
        form_layout.addRow("", self.btn_save)
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Descripción", "Horas", "Recursos", "Acción"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        
        self.refresh_table(tasks)
        layout.addWidget(self.table)
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def refresh_table(self, tasks):
        self.table.setRowCount(0)
        if tasks:
            for task in tasks:
                row = self.table.rowCount()
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(task['description']))
                self.table.setItem(row, 1, QTableWidgetItem(str(task['duration'] or "")))
                self.table.setItem(row, 2, QTableWidgetItem(task['resources'] or ""))
                btn_del = QPushButton("Eliminar")
                btn_del.setObjectName("deleteBtn")
                self.table.setCellWidget(row, 3, btn_del)

    def get_new_task_data(self):
        try:
            dur = float(self.input_duration.text()) if self.input_duration.text() else None
        except:
            dur = None
        return {
            'description': self.input_desc.text().strip(),
            'duration': dur,
            'resources': self.input_resources.text().strip()
        }

class EmployeeDialog(QDialog):
    def __init__(self, parent=None, employees=None):
        super().__init__(parent)
        self.setWindowTitle("Gestionar Empleados")
        self.setMinimumSize(800, 600)
        from src.views.styles import LIGHT_STYLE
        self.setStyleSheet(LIGHT_STYLE)
        self.selected_id = None
        self._init_ui(employees)

    def _init_ui(self, employees):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Form section
        form_group = QGroupBox("Datos del Empleado")
        form_layout = QFormLayout()
        self.input_name = QLineEdit()
        self.input_ip = QLineEdit()
        self.input_office = QLineEdit()
        self.input_title = QLineEdit()
        self.input_supervisor = QLineEdit()
        self.input_supervisor_title = QLineEdit()
        self.input_supervisor_email = QLineEdit()
        self.input_schedule = QLineEdit("08:00 - 17:00")
        self.input_lunch = QLineEdit("12:00 - 13:00")
        
        form_layout.addRow("Nombre Completo:", self.input_name)
        form_layout.addRow("IP:", self.input_ip)
        form_layout.addRow("Oficina (Siglas):", self.input_office)
        form_layout.addRow("Puesto:", self.input_title)
        form_layout.addRow("Supervisor:", self.input_supervisor)
        form_layout.addRow("Título Supervisor:", self.input_supervisor_title)
        form_layout.addRow("Email Supervisor:", self.input_supervisor_email)
        form_layout.addRow("Horario:", self.input_schedule)
        form_layout.addRow("Almuerzo:", self.input_lunch)
        
        # Internal buttons for the form
        btn_layout = QHBoxLayout()
        self.btn_save = QPushButton("Guardar/Actualizar")
        self.btn_clear = QPushButton("Limpiar Formulario")
        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_clear)
        form_layout.addRow("", btn_layout)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)

        # Table section
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Puesto", "Acción"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.refresh_table(employees)
        layout.addWidget(self.table)
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def refresh_table(self, employees):
        self.table.setRowCount(0)
        if employees:
            for emp in employees:
                row = self.table.rowCount()
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(str(emp['id'])))
                self.table.setItem(row, 1, QTableWidgetItem(emp['name']))
                self.table.setItem(row, 2, QTableWidgetItem(emp['job_title']))
                
                btn_del = QPushButton("Eliminar")
                btn_del.setObjectName("deleteBtn")
                self.table.setCellWidget(row, 3, btn_del)

    def get_data(self):
        return {
            'name': self.input_name.text().strip(),
            'ip': self.input_ip.text().strip(),
            'office': self.input_office.text().strip(),
            'job_title': self.input_title.text().strip(),
            'supervisor_name': self.input_supervisor.text().strip(),
            'supervisor_title': self.input_supervisor_title.text().strip(),
            'supervisor_email': self.input_supervisor_email.text().strip(),
            'schedule': self.input_schedule.text().strip(),
            'lunch_period': self.input_lunch.text().strip()
        }

    def fill_form(self, data):
        self.selected_id = data['id']
        self.input_name.setText(data['name'])
        self.input_ip.setText(data['ip'] or "")
        self.input_office.setText(data['office'])
        self.input_title.setText(data['job_title'])
        self.input_supervisor.setText(data['supervisor_name'])
        self.input_supervisor_title.setText(data.get('supervisor_title', ""))
        self.input_supervisor_email.setText(data['supervisor_email'] or "")
        self.input_schedule.setText(data['schedule'])
        self.input_lunch.setText(data['lunch_period'])

    def clear_form(self):
        self.selected_id = None
        self.input_name.clear()
        self.input_ip.clear()
        self.input_office.clear()
        self.input_title.clear()
        self.input_supervisor.clear()
        self.input_supervisor_title.clear()
        self.input_supervisor_email.clear()
        self.input_schedule.setText("08:00 - 17:00")
        self.input_lunch.setText("12:00 - 13:00")

class HistoryDialog(QDialog):
    def __init__(self, parent=None, reports=None):
        super().__init__(parent)
        self.setWindowTitle("Consulta de Registros")
        self.setMinimumSize(900, 500)
        from src.views.styles import LIGHT_STYLE
        self.setStyleSheet(LIGHT_STYLE)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        filter_group = QGroupBox("Filtros")
        filter_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por empleado o fecha...")
        filter_layout.addWidget(QLabel("Buscar:"))
        filter_layout.addWidget(self.search_input)
        filter_group.setLayout(filter_layout)
        layout.addWidget(filter_group)
        
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(["ID", "Fecha", "Empleado", "Periodo", "Horas", "Supervisor"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.refresh_table(reports)
        layout.addWidget(self.table)
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def refresh_table(self, reports):
        self.table.setRowCount(0)
        if reports:
            for rep in reports:
                row = self.table.rowCount()
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(str(rep['id'])))
                self.table.setItem(row, 1, QTableWidgetItem(rep['date']))
                self.table.setItem(row, 2, QTableWidgetItem(rep['employee_name']))
                self.table.setItem(row, 3, QTableWidgetItem(rep['pay_period']))
                self.table.setItem(row, 4, QTableWidgetItem(str(rep['total_hours'])))
                self.table.setItem(row, 5, QTableWidgetItem(rep['supervisor_name']))

class ReportWorker(QThread):
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(bool, str)

    def __init__(self, exporter, mailer, db, report_data, tasks):
        super().__init__()
        self.exporter = exporter
        self.mailer = mailer
        self.db = db
        self.report_data = report_data
        self.tasks = tasks

    def run(self):
        try:
            self.progress.emit(10, "Guardando...")
            self.db.save_report(self.report_data, self.tasks)
            self.progress.emit(40, "Generando archivos...")
            xlsx_path, pdf_path = self.exporter.export(self.report_data, self.tasks)
            self.progress.emit(80, "Enviando correo...")
            self.mailer.send_report(self.report_data, [xlsx_path, pdf_path])
            self.progress.emit(100, "Completado")
            self.finished.emit(True, "Reporte enviado con éxito.")
        except Exception as e:
            self.finished.emit(False, str(e))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bitácora de Trabajo")
        self.setMinimumSize(800, 600)
        self.resize(950, 650)
        self.tasks = []
        self._init_menu()
        self._init_ui()

    def _init_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("Archivo")
        self.action_history = file_menu.addAction("Consultar Registros")
        self.action_exit = file_menu.addAction("Salir")
        config_menu = menubar.addMenu("Configuración")
        self.action_manage_employees = config_menu.addAction("Gestionar Empleados")
        self.action_manage_tasks = config_menu.addAction("Gestionar Tareas Predefinidas")
        self.action_change_dir = config_menu.addAction("Cambiar Carpeta de Destino")

    def _init_ui(self):
        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(8)

        # 0. Selection
        selection_layout = QHBoxLayout()
        selection_layout.addWidget(QLabel("Empleado:"))
        self.combo_employees = QComboBox()
        self.combo_employees.addItem("--- Seleccione ---", None)
        selection_layout.addWidget(self.combo_employees, 1)
        self.lbl_current_emp = QLabel("No seleccionado")
        self.lbl_current_emp.setStyleSheet("font-weight: bold; color: #0078d7;")
        selection_layout.addWidget(self.lbl_current_emp)
        main_layout.addLayout(selection_layout)

        # 1. Report Info
        report_info_group = QGroupBox("Datos del Reporte")
        report_info_layout = QGridLayout()
        report_info_layout.setContentsMargins(8, 8, 8, 8)
        self.input_date = QLineEdit(datetime.date.today().strftime("%d-%m-%Y"))
        self.input_pp = QLineEdit()
        self.input_pp.setReadOnly(True)
        self.input_pp.setMaximumWidth(100)
        report_info_layout.addWidget(QLabel("Fecha:"), 0, 0)
        report_info_layout.addWidget(self.input_date, 0, 1)
        report_info_layout.addWidget(QLabel("Periodo:"), 0, 2)
        report_info_layout.addWidget(self.input_pp, 0, 3)
        report_info_group.setLayout(report_info_layout)
        main_layout.addWidget(report_info_group)

        # 2. Task Entry
        task_group = QGroupBox("Añadir Actividad")
        task_layout = QVBoxLayout()
        task_layout.setContentsMargins(8, 8, 8, 8)
        task_layout.setSpacing(4)
        
        top_task_layout = QHBoxLayout()
        top_task_layout.addWidget(QLabel("Predefinida:"))
        self.combo_std_tasks = QComboBox()
        self.combo_std_tasks.addItem("--- Seleccione ---", None)
        top_task_layout.addWidget(self.combo_std_tasks, 1)
        task_layout.addLayout(top_task_layout)

        entry_grid = QGridLayout()
        entry_grid.setSpacing(4)
        self.task_desc = QTextEdit()
        self.task_desc.setPlaceholderText("Descripción...")
        self.task_desc.setMaximumHeight(50)
        self.task_duration = QLineEdit()
        self.task_duration.setPlaceholderText("Hrs")
        self.task_duration.setMaximumWidth(60)
        self.task_resources = QTextEdit()
        self.task_resources.setPlaceholderText("Recursos...")
        self.task_resources.setMaximumHeight(50)
        
        entry_grid.addWidget(QLabel("Desc:"), 0, 0)
        entry_grid.addWidget(self.task_desc, 0, 1)
        entry_grid.addWidget(QLabel("Hrs:"), 0, 2)
        entry_grid.addWidget(self.task_duration, 0, 3)
        entry_grid.addWidget(QLabel("Rec:"), 1, 0)
        entry_grid.addWidget(self.task_resources, 1, 1, 1, 3)
        
        self.btn_add_task = QPushButton("Añadir")
        self.btn_add_task.setObjectName("addBtn")
        task_layout.addLayout(entry_grid)
        task_layout.addWidget(self.btn_add_task, alignment=Qt.AlignmentFlag.AlignRight)
        task_group.setLayout(task_layout)
        main_layout.addWidget(task_group)

        # 3. Table
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Descripción", "Hrs", "Recursos", "Acción"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        main_layout.addWidget(self.table)

        # 4. Footer
        footer_layout = QHBoxLayout()
        self.lbl_total = QLabel("Total: 0.0 hrs")
        self.lbl_total.setStyleSheet("font-size: 14px; color: #0078d7; font-weight: bold;")
        self.btn_submit = QPushButton("Finalizar y Enviar Reporte")
        self.btn_submit.setObjectName("submitBtn")
        self.btn_submit.setMinimumWidth(200)
        self.btn_submit.setMinimumHeight(30)
        footer_layout.addWidget(self.lbl_total)
        footer_layout.addStretch()
        footer_layout.addWidget(self.btn_submit)
        main_layout.addLayout(footer_layout)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.lbl_status = QLabel("")
        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(self.lbl_status)

    def update_total_hours(self, total):
        self.lbl_total.setText(f"Total: {total:.1f} hrs")

    def show_message(self, title, message, icon=QMessageBox.Icon.Information):
        msg = QMessageBox(self)
        from src.views.styles import LIGHT_STYLE
        msg.setStyleSheet(LIGHT_STYLE)
        msg.setWindowTitle(title)
        msg.setText(message)
        if isinstance(icon, int):
            icon_map = {0: QMessageBox.Icon.NoIcon, 1: QMessageBox.Icon.Information, 
                       2: QMessageBox.Icon.Warning, 3: QMessageBox.Icon.Critical}
            icon = icon_map.get(icon, QMessageBox.Icon.Information)
        msg.setIcon(icon)
        msg.exec()

    def set_loading(self, loading, status=""):
        self.btn_submit.setEnabled(not loading)
        self.progress_bar.setVisible(loading)
        self.lbl_status.setText(status)
        if not loading: self.progress_bar.setValue(0)
