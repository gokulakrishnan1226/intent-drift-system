from intent_manager import IntentManager
from activity_monitor import ActivityMonitor
from drift_detector import DriftDetector
from alert_system import AlertSystem

def main():
    print("=== Intent Drift Alert System (Basic Model) ===")

    intent_manager = IntentManager()
    activity_monitor = ActivityMonitor()
    drift_detector = DriftDetector()
    alert_system = AlertSystem()

    intent = input("Select your purpose (study/coding/browsing): ")
    intent_manager.set_intent(intent)

    while True:
        activity = activity_monitor.get_activity()
        current_intent = intent_manager.get_intent()

        if drift_detector.is_drift(current_intent, activity):
            alert_system.show_alert(current_intent, activity)
        else:
            print("✓ Activity matches your purpose")

        cont = input("Continue? (y/n): ")
        if cont.lower() != 'y':
            print("Exiting program...")
            break

if __name__ == "__main__":
    main()