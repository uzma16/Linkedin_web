import json

def save_tracking_data(data, file_path='tracking_data.json'):
    with open(file_path, 'a') as f:
        json.dump(data, f)
        f.write('\n')

def load_tracking_data(file_path='tracking_data.json'):
    with open(file_path, 'r') as f:
        data = [json.loads(line) for line in f]
    return data