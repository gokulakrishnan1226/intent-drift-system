from backend_controller import BackendController

def main():
    print("=== Intent Drift Alert System (CLI) ===")

    backend = BackendController()

    intent = input("Select your purpose (study/coding/browsing): ")
    backend.set_intent(intent)

    try:
        while True:
            drift_activity = backend.check_drift()
            if drift_activity:
                print(f"⚠️  Detected possible drift to: {drift_activity}")
                # Log and pause monitoring for this demo
                backend.log_event(drift_activity, motivation=None)
            else:
                print("✓ Activity matches your purpose or monitoring paused")

            cont = input("Continue? (y/n): ")
            if cont.lower() != 'y':
                print("Exiting program...")
                break
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting.")

if __name__ == "__main__":
    main()