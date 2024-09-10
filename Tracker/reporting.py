import pandas as pd
from data_storage import load_tracking_data

def generate_report(file_path='tracking_data.json'):
    print("Generating detailed report...")

    # Load the data
    data = load_tracking_data(file_path)
    df = pd.DataFrame(data)

    required_columns = ['file_name', 'change_type', 'time_spent', 'change_size', 'change_context', 'change_summary']
    
    if all(col in df.columns for col in required_columns):
        # Group by file name and change type, then sum the time spent
        report = df.groupby(['file_name', 'change_type'])[['time_spent', 'change_size']].sum().reset_index()

        print("\nDetailed Report:")
        print(report)

        # Additional insights: total time spent per file and overall time spent
        total_time_per_file = df.groupby('file_name').agg({
            'time_spent': 'sum',
            'change_size': 'sum'
        }).reset_index()

        print("\nTotal Time Spent and Change Size Per File:")
        print(total_time_per_file)

        overall_time_spent = df['time_spent'].sum()
        overall_change_size = df['change_size'].sum()

        print(f"\nOverall Time Spent on All Files: {overall_time_spent:.2f} seconds")
        print(f"Overall Change Size across All Files: {overall_change_size} lines")

        # Contextual analysis
        print("\nContextual Information and Change Details for Each File:")
        for file_name, group in df.groupby('file_name'):
            print(f"\nFile: {file_name}")
            for index, row in group.iterrows():
                print(f"  - Change Type: {row['change_type']}")
                print(f"  - Time Spent: {row['time_spent']:.2f} seconds")
                print(f"  - Change Size: {row['change_size']} lines")
                
                if isinstance(row['change_summary'], dict):
                    print(f"  - Summary: Additions: {row['change_summary']['additions']}, "
                          f"Deletions: {row['change_summary']['deletions']}, "
                          f"Modifications: {row['change_summary']['modifications']}")
                    
                    details = row['change_summary'].get('details', {})
                    
                    # if details:
                    #     print("    - Added Lines:")
                    #     for line in details.get('added_lines', []):
                    #         print(f"      Line {line['line_number'] + 1}: {line['content']}")

                    #     print("    - Deleted Lines:")
                    #     for line in details.get('deleted_lines', []):
                    #         print(f"      Line {line['line_number'] + 1}: {line['content']}")

                    #     print("    - Modified Lines:")
                    #     for line in details.get('modified_lines', []):
                    #         print(f"      Line {line['line_number'] + 1}: {line['content']}")

                if isinstance(row['change_context'], list):
                    for context in row['change_context']:
                        print(f"    - {context['type']} '{context['name']}' from line {context['start_line']} to {context['end_line']}")

    else:
        print("One or more required columns not found in data.")
        print("Available columns:", df.columns)
        print("Data preview:")
        print(df.head())

# Example usage
if __name__ == "__main__":
    generate_report('tracking_data.json')
