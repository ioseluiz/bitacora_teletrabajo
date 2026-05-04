from src.models.database import DatabaseManager
from src.services.exporter import ReportExporter
from src.services.mailer import Mailer
from src.utils.pay_period import calcular_periodo_pago
from src.views.main_window import MainWindow, ReportWorker, EmployeeDialog, HistoryDialog, StandardTaskDialog
from PyQt6.QtWidgets import QTableWidgetItem, QPushButton, QFileDialog
from PyQt6.QtCore import Qt

class MainController:
    def __init__(self, view: MainWindow):
        self.view = view
        self.db = DatabaseManager()
        self.exporter = ReportExporter()
        self.mailer = Mailer()
        
        self.tasks_list = []
        self.current_employee = None
        
        self._setup_connections()
        self._load_initial_data()

    def _setup_connections(self):
        # UI Actions
        self.view.btn_add_task.clicked.connect(self._add_task)
        self.view.btn_submit.clicked.connect(self._submit_report)
        self.view.combo_employees.currentIndexChanged.connect(self._on_employee_selected)
        self.view.combo_std_tasks.currentIndexChanged.connect(self._on_std_task_selected)
        
        # Menu actions
        self.view.action_manage_employees.triggered.connect(self._open_employee_manager)
        self.view.action_manage_tasks.triggered.connect(self._open_task_manager)
        self.view.action_history.triggered.connect(self._open_history)
        self.view.action_change_dir.triggered.connect(self._select_output_directory)
        self.view.action_exit.triggered.connect(self.view.close)

    def _load_initial_data(self):
        pp, _ = calcular_periodo_pago()
        self.view.input_pp.setText(pp)
        self._refresh_employee_list()
        self._refresh_std_task_list()

    def _refresh_employee_list(self):
        self.view.combo_employees.blockSignals(True)
        self.view.combo_employees.clear()
        self.view.combo_employees.addItem("--- Seleccione un empleado ---", None)
        for emp in self.db.get_employees():
            self.view.combo_employees.addItem(emp['name'], dict(emp))
        self.view.combo_employees.blockSignals(False)

    def _refresh_std_task_list(self):
        self.view.combo_std_tasks.blockSignals(True)
        self.view.combo_std_tasks.clear()
        self.view.combo_std_tasks.addItem("--- Seleccione una tarea ---", None)
        for task in self.db.get_standard_tasks():
            self.view.combo_std_tasks.addItem(task['description'], dict(task))
        self.view.combo_std_tasks.blockSignals(False)

    def _on_employee_selected(self, index):
        data = self.view.combo_employees.itemData(index)
        if data:
            self.current_employee = dict(data)
            self.view.lbl_current_emp.setText(data['name'])
        else:
            self.current_employee = None
            self.view.lbl_current_emp.setText("No seleccionado")

    def _open_employee_manager(self):
        employees = self.db.get_employees()
        dialog = EmployeeDialog(self.view, employees)
        
        # Internal handlers for the dialog
        def handle_selection(row, col):
            emp_id = int(dialog.table.item(row, 0).text())
            all_emps = self.db.get_employees()
            target = next((e for e in all_emps if e['id'] == emp_id), None)
            if target:
                dialog.fill_form(dict(target))

        def handle_save():
            data = dialog.get_data()
            if not data['name']: 
                self.view.show_message("Error", "Nombre obligatorio.", 2)
                return
            
            if dialog.selected_id:
                self.db.update_employee(dialog.selected_id, data)
            else:
                self.db.save_employee(data)
            
            dialog.refresh_table(self.db.get_employees())
            self._reconnect_emp_dialog(dialog, handle_selection, handle_save, handle_delete)
            self._refresh_employee_list()
            dialog.clear_form()

        def handle_delete(row_idx):
            emp_id = int(dialog.table.item(row_idx, 0).text())
            self.db.delete_employee(emp_id)
            dialog.refresh_table(self.db.get_employees())
            self._reconnect_emp_dialog(dialog, handle_selection, handle_save, handle_delete)
            self._refresh_employee_list()
            dialog.clear_form()

        # Connect signals
        self._reconnect_emp_dialog(dialog, handle_selection, handle_save, handle_delete)
        dialog.btn_clear.clicked.connect(dialog.clear_form)
        dialog.exec()

    def _reconnect_emp_dialog(self, dialog, sel_cb, save_cb, del_cb):
        try: dialog.table.cellDoubleClicked.disconnect()
        except: pass
        dialog.table.cellDoubleClicked.connect(sel_cb)
        
        try: dialog.btn_save.clicked.disconnect()
        except: pass
        dialog.btn_save.clicked.connect(save_cb)
        
        for row in range(dialog.table.rowCount()):
            btn = dialog.table.cellWidget(row, 3)
            if btn:
                try: btn.clicked.disconnect()
                except: pass
                btn.clicked.connect(lambda checked, r=row: del_cb(r))

    def _open_task_manager(self):
        tasks = self.db.get_standard_tasks()
        dialog = StandardTaskDialog(self.view, tasks)
        
        def handle_delete(row_idx):
            task_desc = dialog.table.item(row_idx, 0).text()
            all_tasks = self.db.get_standard_tasks()
            target = next((t for t in all_tasks if t['description'] == task_desc), None)
            if target:
                self.db.delete_standard_task(target['id'])
                dialog.refresh_table(self.db.get_standard_tasks())
                self._reconnect_dialog_btns(dialog, handle_delete)
                self._refresh_std_task_list()

        self._reconnect_dialog_btns(dialog, handle_delete)
        dialog.btn_save.clicked.connect(lambda: self._save_std_task(dialog, handle_delete))
        dialog.exec()

    def _reconnect_dialog_btns(self, dialog, delete_callback):
        for row in range(dialog.table.rowCount()):
            btn = dialog.table.cellWidget(row, 3)
            if btn:
                try: btn.clicked.disconnect()
                except: pass
                btn.clicked.connect(lambda checked, r=row: delete_callback(row))

    def _save_std_task(self, dialog, delete_callback):
        data = dialog.get_new_task_data()
        if not data['description']: return
        self.db.save_standard_task(data)
        dialog.refresh_table(self.db.get_standard_tasks())
        self._reconnect_dialog_btns(dialog, delete_callback)
        self._refresh_std_task_list()
        dialog.input_desc.clear()
        dialog.input_duration.clear()
        dialog.input_resources.clear()

    def _open_history(self):
        reports = self.db.get_all_reports()
        dialog = HistoryDialog(self.view, reports)
        dialog.exec()

    def _select_output_directory(self):
        new_dir = QFileDialog.getExistingDirectory(self.view, "Seleccionar Carpeta")
        if new_dir:
            self.exporter.set_output_dir(new_dir)
            self.view.show_message("Éxito", f"Carpeta actualizada: {new_dir}")

    def _on_std_task_selected(self, index):
        data = self.view.combo_std_tasks.itemData(index)
        if data:
            self.view.task_desc.setPlainText(data['description'])
            if data['duration']: self.view.task_duration.setText(str(data['duration']))
            if data['resources']: self.view.task_resources.setPlainText(data['resources'])

    def _add_task(self):
        desc = self.view.task_desc.toPlainText().strip()
        dur_str = self.view.task_duration.text().strip()
        res = self.view.task_resources.toPlainText().strip()
        if not desc: return self.view.show_message("Error", "Descripción obligatoria.", 2)
        try: dur = float(dur_str)
        except: return self.view.show_message("Error", "Duración numérica.", 2)
        
        self.tasks_list.append({'description': desc, 'duration': dur, 'resources': res})
        self._update_table()
        self.view.task_desc.clear()
        self.view.task_duration.clear()
        self.view.task_resources.clear()
        self.view.combo_std_tasks.setCurrentIndex(0)

    def _update_table(self):
        self.view.table.setRowCount(0)
        total = 0
        for i, task in enumerate(self.tasks_list):
            row = self.view.table.rowCount()
            self.view.table.insertRow(row)
            self.view.table.setItem(row, 0, QTableWidgetItem(task['description']))
            self.view.table.setItem(row, 1, QTableWidgetItem(str(task['duration'])))
            self.view.table.setItem(row, 2, QTableWidgetItem(task['resources']))
            btn = QPushButton("Eliminar")
            btn.setObjectName("deleteBtn")
            btn.clicked.connect(lambda checked, idx=i: self._remove_task(idx))
            self.view.table.setCellWidget(row, 3, btn)
            total += task['duration']
        self.view.update_total_hours(total)

    def _remove_task(self, index):
        if index < len(self.tasks_list):
            self.tasks_list.pop(index)
            self._update_table()

    def _submit_report(self):
        if not self.current_employee: return self.view.show_message("Error", "Seleccione empleado.", 2)
        if not self.tasks_list: return self.view.show_message("Error", "Añada tareas.", 2)
        
        data = {
            'date': self.view.input_date.text(),
            'pay_period': self.view.input_pp.text(),
            'employee_name': self.current_employee['name'],
            'ip': self.current_employee['ip'],
            'office': self.current_employee['office'],
            'job_title': self.current_employee['job_title'],
            'supervisor_name': self.current_employee['supervisor_name'],
            'supervisor_title': self.current_employee.get('supervisor_title', ""),
            'supervisor_email': self.current_employee['supervisor_email'],
            'schedule': self.current_employee['schedule'],
            'lunch_period': self.current_employee['lunch_period'],
            'total_hours': sum(t['duration'] for t in self.tasks_list)
        }
        
        self.view.set_loading(True, "Enviando...")
        self.worker = ReportWorker(self.exporter, self.mailer, self.db, data, self.tasks_list)
        self.worker.progress.connect(lambda v, t: self.view.progress_bar.setValue(v) or self.view.lbl_status.setText(t))
        self.worker.finished.connect(self._on_worker_finished)
        self.worker.start()

    def _on_worker_finished(self, success, message):
        self.view.set_loading(False)
        if success:
            self.view.show_message("Éxito", message)
            self.tasks_list = []
            self._update_table()
        else:
            self.view.show_message("Error", message, 3)
