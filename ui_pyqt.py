from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QMessageBox, QTabWidget, QScrollArea
)
from PyQt5.QtGui import QFont
from alert_dialog import AlertDialog
from motivation_engine import get_motivation_message
from voice_alert import speak_alert, speak_confirmation
from notification_manager import NotificationManager
from graph_viewer import show_graph


class IntentDriftUI(QWidget):
    def __init__(self, backend):
        super().__init__()
        self.backend = backend
        self.notification_manager = NotificationManager()
        self.init_ui()

        self.timer = QTimer()
        self.timer.timeout.connect(self.auto_check)
        self.timer.start(5000)

    def init_ui(self):
        self.setWindowTitle("Intent Drift Alert System")
        self.setFixedSize(500, 450)
        self.setWindowFlags(Qt.Window | Qt.MSWindowsFixedSizeDialogHint)

        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: white;
                font-family: Segoe UI;
            }
            QPushButton {
                background-color: #1E88E5;
                border: none;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
                color: white;
            }
            QPushButton:hover {
                background-color: #1565C0;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
            QLabel {
                color: white;
            }
            QTabWidget {
                background-color: #121212;
            }
            QTabBar::tab {
                background-color: #1E1E1E;
                color: white;
                padding: 8px;
                border: 1px solid #333;
            }
            QTabBar::tab:selected {
                background-color: #1E88E5;
            }
        """)

        tabs = QTabWidget()

        # Tab 1: Control Panel
        control_tab = self.create_control_tab()
        tabs.addTab(control_tab, "Control Panel")

        # Tab 2: Statistics
        stats_tab = self.create_stats_tab()
        tabs.addTab(stats_tab, "Statistics")

        main_layout = QVBoxLayout()
        main_layout.addWidget(tabs)
        self.setLayout(main_layout)

        self.center_window()

    def create_control_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        title = QLabel("Intent Drift Alert System")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #1E88E5;")

        self.status = QLabel("Current Intent: None")
        status_font = QFont()
        status_font.setPointSize(12)
        self.status.setFont(status_font)

        self.monitor = QLabel("Monitoring: Inactive")
        self.monitor.setStyleSheet("color: #FF9800; font-weight: bold;")

        self.focus_score = QLabel("Focus Score: 0%")
        self.focus_score.setStyleSheet("color: #4CAF50;")

        self.focus_time = QLabel("Focused Time: 0 minutes")
        self.focus_time.setStyleSheet("color: #90CAF9;")

        # Intent Selection
        intent_label = QLabel("Select Your Intent:")
        intent_label.setStyleSheet("color: #BBBBBB; font-weight: bold;")

        self.study_btn = QPushButton("📚 Study")
        self.coding_btn = QPushButton("💻 Coding")
        self.browse_btn = QPushButton("🌐 Browsing")

        self.study_btn.clicked.connect(lambda: self.set_intent("study"))
        self.coding_btn.clicked.connect(lambda: self.set_intent("coding"))
        self.browse_btn.clicked.connect(lambda: self.set_intent("browsing"))

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.study_btn)
        btn_layout.addWidget(self.coding_btn)
        btn_layout.addWidget(self.browse_btn)

        # Action Buttons
        action_label = QLabel("Actions:")
        action_label.setStyleSheet("color: #BBBBBB; font-weight: bold;")

        graph_btn = QPushButton("📊 View Graph")
        exit_btn = QPushButton("❌ Exit")
        pause_btn = QPushButton("⏸ Pause Monitoring")

        graph_btn.clicked.connect(self.show_graph_window)
        exit_btn.setStyleSheet("""
            QPushButton {
                background-color: #F44336;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #D32F2F;
            }
        """)
        exit_btn.clicked.connect(self.exit_app)
        pause_btn.clicked.connect(self.toggle_pause)

        action_layout = QHBoxLayout()
        action_layout.addWidget(graph_btn)
        action_layout.addWidget(pause_btn)
        action_layout.addWidget(exit_btn)

        layout.setSpacing(12)
        layout.addWidget(title)
        layout.addWidget(self.status)
        layout.addWidget(self.monitor)
        layout.addWidget(self.focus_score)
        layout.addWidget(self.focus_time)
        layout.addSpacing(10)
        layout.addWidget(intent_label)
        layout.addLayout(btn_layout)
        layout.addSpacing(10)
        layout.addWidget(action_label)
        layout.addLayout(action_layout)
        layout.addStretch()

        tab.setLayout(layout)
        return tab

    def create_stats_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        stats_title = QLabel("Session Statistics")
        stats_title_font = QFont()
        stats_title_font.setPointSize(16)
        stats_title_font.setBold(True)
        stats_title.setFont(stats_title_font)
        stats_title.setStyleSheet("color: #1E88E5;")

        self.stats_text = QLabel(
            "No active session yet.\n\n"
            "Select an intent to start monitoring and collect statistics."
        )
        self.stats_text.setStyleSheet("color: #BBBBBB; line-height: 1.6;")
        self.stats_text.setWordWrap(True)

        layout.addWidget(stats_title)
        layout.addWidget(self.stats_text)
        layout.addStretch()

        tab.setLayout(layout)
        return tab

    def center_window(self):
        frame = self.frameGeometry()
        screen = self.screen().availableGeometry().center()
        frame.moveCenter(screen)
        self.move(frame.topLeft())

    def set_intent(self, intent):
        self.backend.set_intent(intent)
        self.status.setText(f"Current Intent: {intent.upper()}")
        self.monitor.setText("Monitoring: Active")
        self.monitor.setStyleSheet("color: #4CAF50; font-weight: bold;")
        
        # Voice confirmation and notification
        speak_confirmation(intent)
        self.notification_manager.send_notification(
            "🎯 Intent Set",
            f"Monitoring {intent.upper()} mode. Stay focused!",
            duration=3
        )

    def toggle_pause(self):
        self.backend.monitoring_paused = not self.backend.monitoring_paused
        if self.backend.monitoring_paused:
            self.monitor.setText("Monitoring: Paused")
            self.monitor.setStyleSheet("color: #FF9800; font-weight: bold;")
        else:
            self.monitor.setText("Monitoring: Active")
            self.monitor.setStyleSheet("color: #4CAF50; font-weight: bold;")

    def auto_check(self):
        # Update stats
        focus_score = self.backend.get_focus_score()
        focus_mins = self.backend.get_focused_minutes()
        self.focus_score.setText(f"Focus Score: {focus_score}%")
        self.focus_time.setText(f"Focused Time: {focus_mins} minutes")

        activity = self.backend.check_drift()
        if activity:
            self.show_alert(activity)

    def show_alert(self, activity):
        if self.backend.popup_open:
            return

        self.backend.popup_open = True

        focused_mins = self.backend.get_focused_minutes()
        motivation = get_motivation_message(focused_mins)

        # Send system notification immediately
        self.notification_manager.send_alert(
            "⚠ DISTRACTION DETECTED!",
            f"You drifted to {activity}",
            activity,
            motivation,
            sound=True
        )

        # Speak alert message
        speak_alert(focused_mins, motivation)

        # Show dialog
        dialog = AlertDialog(self, activity, focused_mins, motivation)
        dialog.exec_()

        self.backend.popup_open = False
        self.backend.distraction_start = None

        if dialog.choice == "ignore":
            self.backend.monitoring_paused = True
            self.monitor.setText("Monitoring: Paused")
            self.monitor.setStyleSheet("color: #FF9800; font-weight: bold;")
            self.notification_manager.send_notification(
                "⏸ Monitoring Paused",
                "You've paused focus monitoring",
                duration=3
            )

        elif dialog.choice == "change":
            self.status.setText("Current Intent: None")
            self.backend.current_intent = None
            self.monitor.setText("Monitoring: Inactive")
            self.monitor.setStyleSheet("color: #FF9800; font-weight: bold;")
            self.notification_manager.send_notification(
                "↻ Intent Changed",
                "Select a new intent to continue",
                duration=3
            )

    def show_graph_window(self):
        try:
            show_graph("focus_log.csv")
        except FileNotFoundError:
            QMessageBox.warning(self, "No Data", "No focus log data available yet.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to display graph: {str(e)}")

    def exit_app(self):
        reply = QMessageBox.question(
            self, "Confirm Exit",
            "Are you sure you want to exit?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.close()