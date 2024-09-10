# import time
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler
# from .time_tracker import start_tracking, stop_tracking
# from .data_storage import save_tracking_data
# from .git_utils import classify_change

# class MyHandler(FileSystemEventHandler):
#     def on_modified(self, event):
#         if not event.is_directory:
#             file_name = event.src_path
#             start_tracking(file_name)
#             time.sleep(1)  # Simulate time spent working on the file
#             time_spent = stop_tracking(file_name)
            
#             change_type = classify_change(file_name)
#             data = {
#                 'file_name': file_name,
#                 'time_spent': time_spent,
#                 'change_type': change_type
#             }
#             save_tracking_data(data)

# def start_monitoring(directory_to_monitor):
#     event_handler = MyHandler()
#     observer = Observer()
#     observer.schedule(event_handler, path=directory_to_monitor, recursive=True)
#     observer.start()
#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         observer.stop()
#     observer.join()

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .time_tracker import start_tracking, stop_tracking
from .data_storage import save_tracking_data
from .git_utils import classify_change
import os
import difflib
import ast

class IntelligentHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.last_event_time = {}
        self.file_snapshots = {}

    def on_any_event(self, event):
        if not event.is_directory:
            file_name = event.src_path
            current_time = time.time()
            
            if file_name in self.last_event_time:
                time_spent = current_time - self.last_event_time[file_name]
            else:
                time_spent = 0.0
            
            self.last_event_time[file_name] = current_time

            # Capture more detailed information
            change_type = classify_change(file_name)
            change_size = self.calculate_change_size(file_name)
            change_context = self.analyze_context(file_name)

            data = {
                'file_name': file_name,
                'time_spent': time_spent,
                'change_type': change_type,
                'change_size': change_size,
                'change_context': change_context,
            }
            save_tracking_data(data)

    def calculate_change_size(self, file_name):
        """Calculate the size of the change by comparing the file before and after modification."""
        if file_name in self.file_snapshots:
            with open(file_name, 'r') as f:
                current_content = f.readlines()

            previous_content = self.file_snapshots[file_name]

            # Use difflib to find differences
            diff = list(difflib.unified_diff(previous_content, current_content))
            change_size = len(diff)
            

            self.file_snapshots[file_name] = current_content
        else:
            # First time tracking this file, store the snapshot
            with open(file_name, 'r') as f:
                self.file_snapshots[file_name] = f.readlines()
            change_size = 0  # No previous snapshot to compare with

        return change_size

    def analyze_context(self, file_name):
        """Analyze the context of the change, such as which function or class was modified."""
        with open(file_name, 'r') as f:
            file_content = f.read()

        try:
            tree = ast.parse(file_content)
            context_info = []

            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                    context_info.append({
                        'type': 'Function' if isinstance(node, ast.FunctionDef) else 'Class',
                        'name': node.name,
                        'start_line': node.lineno,
                        'end_line': node.body[-1].lineno if node.body else node.lineno
                    })

            # This could be extended to more detailed context analysis
            return context_info

        except SyntaxError:
            # If the file content is not valid Python code
            return "Invalid Python code"

# You can now use this handler with the observer
def start_intelligent_monitoring(directory_to_monitor):
    event_handler = IntelligentHandler()
    observer = Observer()
    observer.schedule(event_handler, path=directory_to_monitor, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
