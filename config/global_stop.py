import threading

# Global stop event
stop_event = threading.Event()

def wait_for_enter():
    """Waits for the Enter key press to stop the operation."""
    input("Press Enter to stop...\n\n")
    stop_event.set()
    print("STOP instruction received. Working to quit...")
