import pandas as pd
from .data_storage import load_tracking_data

def generate_report(file_path='tracking_data.json'):
    print("Generating detailed report...")

    # Load the data
    data = load_tracking_data(file_path)
    df = pd.DataFrame(data)

    if 'file_name' in df.columns and 'change_type' in df.columns and 'time_spent' in df.columns:
        # Group by file name and change type, then sum the time spent
        report = df.groupby(['file_name', 'change_type'])['time_spent'].sum().reset_index()

        print("\nDetailed Report:")
        print(report)

        # Additional insights, like total time spent per file or overall time spent
        total_time_per_file = df.groupby('file_name')['time_spent'].sum().reset_index()
        print("\nTotal Time Spent Per File:")
        print(total_time_per_file)

        overall_time_spent = df['time_spent'].sum()
        print(f"\nOverall Time Spent on All Files: {overall_time_spent:.2f} seconds")

    else:
        print("One or more required columns ('file_name', 'change_type', 'time_spent') not found in data.")
        print("Available columns:", df.columns)
        print("Data preview:")
        print(df.head())

# Example usage
if __name__ == "__main__":
    generate_report('tracking_data.json')
