from .monitor import start_monitoring
import argparse

def main():
    parser = argparse.ArgumentParser(description="Developer Activity Tracker")
    parser.add_argument("directory", help="Directory to monitor for file changes")
    args = parser.parse_args()

    directory_to_monitor = args.directory
    print("Directory",directory_to_monitor)
    start_monitoring(directory_to_monitor)

if __name__ == "__main__":
    main()
