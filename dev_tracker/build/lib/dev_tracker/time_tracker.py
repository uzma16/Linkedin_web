import time

# Dictionary to store start times of files
start_times = {}

def start_tracking(file_name):
    # Record the start time
    start_times[file_name] = time.time()

def stop_tracking(file_name):
    # Record the stop time and calculate time spent
    if file_name in start_times:
        start_time = start_times.pop(file_name)
        stop_time = time.time()
        time_spent = stop_time - start_time
        return time_spent
    return 0.0
