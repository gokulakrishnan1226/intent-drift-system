import sys
from PyQt5.QtWidgets import QApplication
from ui_pyqt import IntentDriftUI
from backend_controller import BackendController

app = QApplication(sys.argv)
backend = BackendController()
window = IntentDriftUI(backend)
window.show()
sys.exit(app.exec_())