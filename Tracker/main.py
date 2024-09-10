from monitor import start_intelligent_monitoring
import argparse

def main():
    # parser = argparse.ArgumentParser(description="Developer Activity Tracker")
    # parser.add_argument("directory", help="Directory to monitor for file changes")
    # args = parser.parse_args()

    # directory_to_monitor = args.directory
    directory_to_monitor = r"C:\Users\Dell\Desktop\Tracker"
    print("Directory",directory_to_monitor)
    start_intelligent_monitoring(directory_to_monitor)

if __name__ == "__main__":
    main()
