import os
import difflib
import ast
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from data_storage import save_tracking_data
from git_utils import classify_change

class IntelligentHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.last_event_time = {}
        self.file_snapshots = {}

    def on_any_event(self, event):
        if not event.is_directory:
            file_name = event.src_path
            
            # Ignore changes to tracking_data.json
            if file_name.endswith('tracking_data.json'):
                return
            
            current_time = time.time()
            time_spent = current_time - self.last_event_time.get(file_name, current_time)
            self.last_event_time[file_name] = current_time

            # Capture more detailed information
            change_type = classify_change(file_name)
            change_size, change_summary = self.calculate_change_size(file_name)
            change_context = self.analyze_context(file_name)

            data = {
                'file_name': file_name,
                'time_spent': time_spent,
                'change_type': change_type,
                'change_size': change_size,
                'change_summary': change_summary,
                'change_context': change_context,
            }
            save_tracking_data(data)

    def calculate_change_size(self, file_name):
        """Calculate the size of the change by comparing the file before and after modification, and summarize the change."""
        if file_name in self.file_snapshots:
            with open(file_name, 'r') as f:
                current_content = f.readlines()

            previous_content = self.file_snapshots[file_name]

            # Use difflib to find differences
            diff = list(difflib.unified_diff(previous_content, current_content, lineterm=''))
            change_size = len(diff)

            additions = []
            deletions = []
            modifications = []

            for i, line in enumerate(diff):
                if line.startswith('+') and not line.startswith('+++'):
                    additions.append({'line_number': i, 'content': line[1:].strip()})
                elif line.startswith('-') and not line.startswith('---'):
                    deletions.append({'line_number': i, 'content': line[1:].strip()})
                # Modifications can be considered as pairs of deletions and additions
                elif line.startswith(' ') and (i > 0 and (diff[i-1].startswith('-') or diff[i-1].startswith('+'))):
                    modifications.append({'line_number': i, 'content': line[1:].strip()})

            change_summary = {
                'additions': len(additions),
                'deletions': len(deletions),
                'modifications': len(modifications),
                'details': {
                    'added_lines': additions,
                    'deleted_lines': deletions,
                    'modified_lines': modifications,
                }
            }

            # Update the snapshot
            self.file_snapshots[file_name] = current_content
        else:
            # First time tracking this file, store the snapshot
            with open(file_name, 'r') as f:
                self.file_snapshots[file_name] = f.readlines()
            change_size = 0  # No previous snapshot to compare with
            change_summary = {'additions': 0, 'deletions': 0, 'modifications': 0, 'details': {}}

        return change_size, change_summary


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
