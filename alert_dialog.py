from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
)
from PyQt5.QtGui import QFont


class AlertDialog(QDialog):
    def __init__(self, parent, activity, focused_minutes, motivation):
        super().__init__(parent)
        self.activity = activity
        self.focused_minutes = focused_minutes
        self.motivation = motivation
        self.choice = None
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("⚠ DISTRACTION DETECTED!")
        self.setFixedSize(420, 280)

        self.setWindowFlags(
            Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint
        )
        self.setModal(True)
        
        # Set dark theme with red accent
        self.setStyleSheet("""
            QDialog {
                background-color: #1a1a1a;
                border: 3px solid #F44336;
                border-radius: 15px;
            }
            QLabel {
                color: white;
            }
            QPushButton {
                border-radius: 8px;
                padding: 8px;
                font-size: 12px;
                font-weight: bold;
                border: 2px solid;
            }
        """)
        
        self.raise_()
        self.activateWindow()

        # Title
        title = QLabel("⚠ YOU ARE DISTRACTED!")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #F44336; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)

        # Focus time badge
        focus_badge = QLabel(f"⏱ Focused: {self.focused_minutes} min")
        focus_badge.setStyleSheet("color: #4CAF50; font-size: 14px; font-weight: bold;")
        focus_badge.setAlignment(Qt.AlignCenter)

        # Activity detected
        activity_lbl = QLabel(f"📱 Activity: {self.activity.upper()}")
        activity_lbl.setStyleSheet("color: #FF9800; font-size: 13px; background-color: #2a2a2a; padding: 8px; border-radius: 5px;")
        activity_lbl.setAlignment(Qt.AlignCenter)

        # Motivation message
        motivation_lbl = QLabel(f"💡 {self.motivation}")
        motivation_lbl.setWordWrap(True)
        motivation_lbl.setStyleSheet("color: #90CAF9; font-size: 12px; font-style: italic;")
        motivation_lbl.setAlignment(Qt.AlignCenter)

        # Buttons
        btn_continue = QPushButton("✓ Continue Focused")
        btn_ignore = QPushButton("✕ Ignore & Pause")
        btn_change = QPushButton("↻ Change Intent")

        btn_continue.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                border-color: #45a049;
                color: white;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        btn_ignore.setStyleSheet("""
            QPushButton {
                background-color: #F44336;
                border-color: #da190b;
                color: white;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        
        btn_change.setStyleSheet("""
            QPushButton {
                background-color: #1E88E5;
                border-color: #1565C0;
                color: white;
            }
            QPushButton:hover {
                background-color: #1565C0;
            }
        """)

        btn_continue.clicked.connect(lambda: self.select("continue"))
        btn_ignore.clicked.connect(lambda: self.select("ignore"))
        btn_change.clicked.connect(lambda: self.select("change"))

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(btn_continue)
        btn_layout.addWidget(btn_ignore)
        btn_layout.addWidget(btn_change)

        # Main layout
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.addWidget(title)
        layout.addWidget(focus_badge)
        layout.addWidget(activity_lbl)
        layout.addWidget(motivation_lbl)
        layout.addStretch()
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def select(self, choice):
        """Select an option and close dialog."""
        self.choice = choice
        self.accept()