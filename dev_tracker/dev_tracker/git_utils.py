import subprocess

def get_last_commit_message():
    try:
        commit_message = subprocess.check_output(['git', 'log', '-1', '--pretty=%B']).strip().decode('utf-8')
        return commit_message
    except subprocess.CalledProcessError:
        return ""

def classify_change(commit_message):
    if "fix" in commit_message.lower():
        return "Bug Fix"
    elif "add" in commit_message.lower() or "new" in commit_message.lower():
        return "New Feature"
    elif "delete" in commit_message.lower():
        return "Deleted"
    return "Other"
