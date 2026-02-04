from tkinter import dialog
from turtle import title
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton,
    QVBoxLayout, QMessageBox
)
from PyQt5.QtCore import QTimer
from alert_dialog import AlertDialog
from motivation_engine import get_motivation_message
from voice_alert import speak
class IntentDriftUI(QWidget):
    def __init__(self, backend):
        super().__init__()
        self.backend = backend
        self.init_ui()

        self.timer = QTimer()
        self.timer.timeout.connect(self.auto_check)
        self.timer.start(5000)   

    def init_ui(self):
        self.setWindowTitle("Intent Drift Alert System")
        self.setFixedSize(420, 320)
        self.setWindowFlags(Qt.Window | Qt.MSWindowsFixedSizeDialogHint)

        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: white;
                font-family: Segoe UI;
            }
            QPushButton {
                background-color: #1E88E5;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1565C0;
            }
        """)

        title = QLabel("Intent Drift Alert System")
        title.setStyleSheet("font-size:20px; font-weight:bold;")

        self.status = QLabel("Current Intent: None")
        self.monitor = QLabel("Monitoring: Active")
        self.monitor.setStyleSheet("color:#4CAF50")

        self.study_btn = QPushButton("Study")
        self.browse_btn = QPushButton("Browsing")

        self.study_btn.clicked.connect(lambda: self.set_intent("study"))
        self.browse_btn.clicked.connect(lambda: self.set_intent("browsing"))
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.addWidget(title)
        layout.addWidget(self.study_btn)
        layout.addWidget(self.browse_btn)
        layout.addWidget(self.status)
        layout.addWidget(self.monitor)
        self.setLayout(layout)
        self.center_window()
    
    def center_window(self):
        frame = self.frameGeometry()
        screen = self.screen().availableGeometry().center()
        frame.moveCenter(screen)
        self.move(frame.topLeft())

    def set_intent(self, intent):
        self.backend.set_intent(intent)
        self.status.setText(f"Current Intent: {intent}")
        self.monitor.setText("Monitoring: Active")
        self.monitor.setStyleSheet("color:green")

    def auto_check(self):
        activity = self.backend.check_drift()
        if activity:
            self.show_alert(activity)

    def show_alert(self, activity):
        if(self.backend.popup_open):
            return
        
        self.backend.popup_open = True

        focused_mins = self.backend.get_focused_minutes()
        motivation = get_motivation_message(focused_mins)

        from voice_alert import speak
        speak(f"You were focused for {focused_mins} minutes. {motivation}")

        dialog = AlertDialog(self, activity, focused_mins, motivation)
        dialog.exec_()
        
        self.backend.popup_open = False
        self.backend.distraction_start = None
        if dialog.choice == "ignore":
            self.backend.monitoring_paused = True
            self.close()

        elif dialog.choice == "change":
            self.status.setText("Current Intent: None")
            self.backend.current_intent = None