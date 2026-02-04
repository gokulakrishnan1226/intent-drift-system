from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
)

class AlertDialog(QDialog):
    def __init__(self, parent, activity, focused_minutes, motivation):
        super().__init__(parent)
        self.activity = activity
        self.focused_minutes = focused_minutes
        # Handle both string and callable motivation
        self.motivation = motivation if isinstance(motivation, str) else motivation()
        self.choice = None
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Distraction Detected")
        self.setFixedSize(420, 280)

        self.setWindowFlags(
            Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint
        )
        self.setModal(True)
        self.raise_()
        self.activateWindow()

        # Main alert title
        title = QLabel("⚠ You are distracted!")
        title.setStyleSheet("font-size:18px; font-weight:bold; color:#FF6B6B;")

        # Focus minutes message
        focus_message = QLabel(f"You have focused for {self.focused_minutes} minutes")
        focus_message.setStyleSheet("font-size:16px; font-weight:bold; color:#4CAF50;")
        
        # Activity detection
        activity_lbl = QLabel(f"Current Activity: {self.activity.capitalize()}")
        activity_lbl.setStyleSheet("font-size:12px; color:#BBBBBB;")

        # Motivation message
        motivation_lbl = QLabel(f"💡 {self.motivation}")
        motivation_lbl.setWordWrap(True)
        motivation_lbl.setStyleSheet("font-size:13px; color:#90CAF9; font-style:italic; margin-top:10px;")

        # Buttons
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

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(focus_message)
        layout.addWidget(activity_lbl)
        layout.addWidget(motivation_lbl)
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