import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .time_tracker import start_tracking, stop_tracking
from .data_storage import save_tracking_data
from .git_utils import classify_change

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            file_name = event.src_path
            start_tracking(file_name)
            time.sleep(1)  # Simulate time spent working on the file
            time_spent = stop_tracking(file_name)
            
            change_type = classify_change(file_name)
            data = {
                'file_name': file_name,
                'time_spent': time_spent,
                'change_type': change_type
            }
            save_tracking_data(data)

def start_monitoring(directory_to_monitor):
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=directory_to_monitor, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
