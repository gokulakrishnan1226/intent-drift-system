from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton,
    QVBoxLayout, QMessageBox
)
from alert_dialog import AlertDialog
from motivation_engine import get_motivation_message
from voice_alert import speak, speak_distraction_alert
class IntentDriftUI(QWidget):
    def __init__(self, backend):
        super().__init__()
        self.backend = backend
        self.monitoring = True
        self.pause_monitoring = False  # Flag to pause alerts during intent change
        self.init_ui()
        self.motivation_engine = get_motivation_message
        self.timer = QTimer()
        self.timer.timeout.connect(self.auto_check)
        self.timer.start(5000)   

    def get_motivation(self):
        focused_minutes = self.backend.focus_tracker.get_focused_minutes()  
        return get_motivation_message(focused_minutes)
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
        self.pause_monitoring = False  # Resume monitoring after intent is set

    def auto_check(self):
        if not self.monitoring or self.pause_monitoring:
            return
        activity = self.backend.check_drift()
        if activity is not None:
            focused_minutes = self.backend.focus_tracker.get_focused_minutes()
            self.show_alert(activity, focused_minutes)

    def show_alert(self, activity, focused_minutes):
        motivation_msg = self.get_motivation()
        
        # Speak the alert message with TTS
        speak_distraction_alert(focused_minutes, motivation_msg)
        
        # Show dialog
        dialog = AlertDialog(self, activity, focused_minutes, motivation_msg)
        dialog.exec_()

        choice = dialog.choice

        if choice == "continue":
            # Reset the distraction timer so the user gets a grace period
            try:
                self.backend.reset_distraction_timer()
            except Exception:
                # Fallback: clear last alert marker
                self.backend.last_alert_activity = None
            # Minimize and keep monitoring
            speak("Continue monitoring your focus")
            self.showMinimized()

        elif choice == "ignore":
            # Stop monitoring and close app
            speak("Monitoring stopped")
            self.monitoring = False
            self.close()

        elif choice == "change":
            # Pause monitoring and show main window for intent change
            self.pause_monitoring = True  # Pause alerts while user selects new intent
            self.backend.last_alert_activity = None  # Reset to allow new alerts
            speak("Select your new intent")
            self.showNormal()
            self.raise_()
            self.activateWindow()