import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_path='data/bitacora.db'):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Table for reports
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    pay_period TEXT NOT NULL,
                    employee_name TEXT NOT NULL,
                    ip TEXT,
                    office TEXT NOT NULL,
                    job_title TEXT NOT NULL,
                    supervisor_name TEXT NOT NULL,
                    supervisor_title TEXT,
                    supervisor_email TEXT,
                    schedule TEXT NOT NULL,
                    lunch_period TEXT NOT NULL,
                    total_hours REAL DEFAULT 0
                )
            ''')
            # Table for tasks
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    report_id INTEGER NOT NULL,
                    description TEXT NOT NULL,
                    duration REAL NOT NULL,
                    resources TEXT,
                    FOREIGN KEY (report_id) REFERENCES reports (id) ON DELETE CASCADE
                )
            ''')
            # Table for employees
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    ip TEXT,
                    office TEXT NOT NULL,
                    job_title TEXT NOT NULL,
                    supervisor_name TEXT NOT NULL,
                    supervisor_title TEXT,
                    supervisor_email TEXT,
                    schedule TEXT NOT NULL,
                    lunch_period TEXT NOT NULL
                )
            ''')
            # Table for standard tasks
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS standard_tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT NOT NULL,
                    duration REAL,
                    resources TEXT
                )
            ''')
            
            # Migration check for existing DBs
            cursor.execute("PRAGMA table_info(reports)")
            columns = [col[1] for col in cursor.fetchall()]
            if 'ip' not in columns:
                cursor.execute("ALTER TABLE reports ADD COLUMN ip TEXT")
            if 'supervisor_email' not in columns:
                cursor.execute("ALTER TABLE reports ADD COLUMN supervisor_email TEXT")
            if 'supervisor_title' not in columns:
                cursor.execute("ALTER TABLE reports ADD COLUMN supervisor_title TEXT")
                
            cursor.execute("PRAGMA table_info(employees)")
            columns_emp = [col[1] for col in cursor.fetchall()]
            if 'supervisor_email' not in columns_emp:
                cursor.execute("ALTER TABLE employees ADD COLUMN supervisor_email TEXT")
            if 'supervisor_title' not in columns_emp:
                cursor.execute("ALTER TABLE employees ADD COLUMN supervisor_title TEXT")
            
            conn.commit()

    def get_standard_tasks(self):
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM standard_tasks ORDER BY description ASC')
            return cursor.fetchall()

    def save_standard_task(self, task_data):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO standard_tasks (description, duration, resources)
                VALUES (?, ?, ?)
            ''', (task_data['description'], task_data['duration'], task_data['resources']))
            conn.commit()

    def delete_standard_task(self, task_id):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM standard_tasks WHERE id = ?', (task_id,))
            conn.commit()

    def get_employees(self):
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM employees ORDER BY name ASC')
            return cursor.fetchall()

    def save_employee(self, emp_data):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO employees (
                    name, ip, office, job_title, supervisor_name, supervisor_title, supervisor_email, schedule, lunch_period
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                emp_data['name'], emp_data['ip'], emp_data['office'],
                emp_data['job_title'], emp_data['supervisor_name'], 
                emp_data.get('supervisor_title', ""),
                emp_data['supervisor_email'],
                emp_data['schedule'], emp_data['lunch_period']
            ))
            conn.commit()
            return cursor.lastrowid

    def update_employee(self, emp_id, emp_data):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE employees SET 
                    name=?, ip=?, office=?, job_title=?, supervisor_name=?, 
                    supervisor_title=?, supervisor_email=?, schedule=?, lunch_period=?
                WHERE id=?
            ''', (
                emp_data['name'], emp_data['ip'], emp_data['office'],
                emp_data['job_title'], emp_data['supervisor_name'], 
                emp_data.get('supervisor_title', ""),
                emp_data['supervisor_email'],
                emp_data['schedule'], emp_data['lunch_period'],
                emp_id
            ))
            conn.commit()

    def delete_employee(self, emp_id):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM employees WHERE id = ?', (emp_id,))
            conn.commit()

    def save_report(self, report_data, tasks):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            try:
                # Insert report
                cursor.execute('''
                    INSERT INTO reports (
                        date, pay_period, employee_name, ip, office, job_title, 
                        supervisor_name, supervisor_title, supervisor_email, schedule, lunch_period, total_hours
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    report_data['date'], report_data['pay_period'], 
                    report_data['employee_name'], report_data['ip'],
                    report_data['office'], 
                    report_data['job_title'], report_data['supervisor_name'],
                    report_data.get('supervisor_title', ""),
                    report_data['supervisor_email'],
                    report_data['schedule'], report_data['lunch_period'], 
                    report_data['total_hours']
                ))
                report_id = cursor.lastrowid

                # Insert tasks
                for task in tasks:
                    cursor.execute('''
                        INSERT INTO tasks (report_id, description, duration, resources)
                        VALUES (?, ?, ?, ?)
                    ''', (report_id, task['description'], task['duration'], task['resources']))
                
                conn.commit()
                return report_id
            except Exception as e:
                conn.rollback()
                raise e

    def get_last_report_info(self):
        """Helper to pre-fill common fields from the last report."""
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM reports ORDER BY id DESC LIMIT 1')
            return cursor.fetchone()

    def get_all_reports(self):
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM reports ORDER BY date DESC')
            return cursor.fetchall()
