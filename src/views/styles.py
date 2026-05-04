LIGHT_STYLE = """
/* Global Styles */
QMainWindow, QDialog, QMessageBox, QWidget#centralWidget {
    background-color: #f3f3f3;
    color: #000000;
}

QWidget {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 12px;
    color: #000000; /* Force black text globally */
}

/* Specific background for dialogs to prevent dark issues */
QDialog, QMessageBox, QMenu {
    background-color: #ffffff;
    color: #000000;
    border: 1px solid #bcbcbc;
}

/* Labels */
QLabel {
    color: #000000;
    background-color: transparent;
}

/* Inputs */
QLineEdit, QTextEdit, QComboBox, QDoubleSpinBox {
    background-color: #ffffff;
    color: #000000;
    border: 1px solid #bcbcbc;
    border-radius: 2px;
    padding: 4px;
    selection-background-color: #0078d7;
    selection-color: #ffffff;
}

QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
    border: 1px solid #0078d7;
}

/* Dropdown list styling */
QComboBox QAbstractItemView {
    background-color: #ffffff;
    color: #000000;
    border: 1px solid #bcbcbc;
    selection-background-color: #0078d7;
    selection-color: #ffffff;
}

QComboBox QAbstractItemView::item {
    background-color: #ffffff;
    color: #000000;
    padding: 4px;
}

/* Buttons */
QPushButton {
    background-color: #e1e1e1;
    color: #000000;
    border: 1px solid #adadad;
    border-radius: 2px;
    padding: 4px 12px;
    min-height: 24px;
}

QPushButton:hover {
    background-color: #e5f1fb;
    border: 1px solid #0078d7;
}

QPushButton:pressed {
    background-color: #cce4f7;
}

QPushButton#submitBtn {
    background-color: #0078d7;
    color: #ffffff;
    border: 1px solid #005a9e;
}

QPushButton#submitBtn:hover {
    background-color: #1984d8;
}

/* Accent for Add Task Button */
QPushButton#addBtn {
    background-color: #28a745;
    color: #ffffff;
    border: 1px solid #218838;
}

QPushButton#addBtn:hover {
    background-color: #218838;
}

QPushButton#deleteBtn {
    background-color: #ffffff;
    border: 1px solid #adadad;
    color: #e81123;
    min-width: 60px;
}

/* Table styling */
QTableWidget {
    background-color: #ffffff;
    color: #000000;
    border: 1px solid #bcbcbc;
    gridline-color: #f0f0f0;
}

QHeaderView::section {
    background-color: #ffffff;
    color: #000000;
    padding: 4px;
    border: 1px solid #dcdcdc;
}

/* Progress Bar */
QProgressBar {
    border: 1px solid #bcbcbc;
    text-align: center;
    background-color: #ffffff;
    color: #000000;
    height: 15px;
}

QProgressBar::chunk {
    background-color: #06b025;
}

/* Group Boxes */
QGroupBox {
    color: #000000;
    font-weight: bold;
    border: 1px solid #dcdcdc;
    margin-top: 10px;
    padding-top: 10px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 8px;
    padding: 0 4px;
}

/* Menu Bar */
QMenuBar {
    background-color: #ffffff;
    color: #000000;
    border-bottom: 1px solid #dcdcdc;
}

QMenuBar::item {
    background-color: transparent;
    color: #000000;
}

QMenuBar::item:selected {
    background-color: #91c9f7;
}
"""
