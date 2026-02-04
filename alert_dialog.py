from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
)

class AlertDialog(QDialog):
    def __init__(self, parent, activity, focused_minutes, motivation):
        super().__init__(parent)
        self.activity = activity
        self.focused_minutes = focused_minutes
        self.motivation = motivation
        self.choice = None
        self.init_ui()
        
    def init_ui(self):
        focus_lbl = QLabel(f"Focused time before distraction: {self.focused_minutes} minutes")
        focus_lbl.setStyleSheet("font-size:13px; color:#BBBBBB;")
        
        motivation_lbl = QLabel(f"💡 {self.motivation}")
        motivation_lbl.setWordWrap(True)
        motivation_lbl.setStyleSheet("font-size:13px; color:#90CAF9; font-style:italic;")
        
        self.setWindowTitle("Distraction Detected")
        self.setFixedSize(380, 230)

        self.setWindowFlags(
            Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint
        )
        self.setModal(True)
        self.raise_()
        self.activateWindow()

        title = QLabel("⚠ You are distracted!")
        title.setStyleSheet("font-size:17px; font-weight:bold;")

        activity_lbl = QLabel(f"Activity: {self.activity}")
        activity_lbl.setStyleSheet("font-size:13px;")

        btn_continue = QPushButton("Continue")
        btn_ignore = QPushButton("Ignore & Exit")
        btn_change = QPushButton("Change Intent")

        btn_continue.setStyleSheet(self.btn_style("#4CAF50"))
        btn_ignore.setStyleSheet(self.btn_style("#F44336"))
        btn_change.setStyleSheet(self.btn_style("#1E88E5"))

        btn_continue.clicked.connect(lambda: self.select("continue"))
        btn_ignore.clicked.connect(lambda: self.select("ignore"))
        btn_change.clicked.connect(lambda: self.select("change"))

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(btn_continue)
        btn_layout.addWidget(btn_ignore)
        btn_layout.addWidget(btn_change)

        layout = QVBoxLayout()
        layout.addWidget(motivation_lbl)
        layout.addWidget(focus_lbl)
        layout.addWidget(title)
        layout.addWidget(activity_lbl)
        layout.addStretch()
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def select(self, choice):
        self.choice = choice
        self.accept()

    def btn_style(self, color):
        return f"""
        QPushButton {{
            background-color: {color};
            color: white;
            border-radius: 8px;
            padding: 8px;
            font-size: 13px;
        }}
        QPushButton:hover {{
            opacity: 0.85;
        }}
        """