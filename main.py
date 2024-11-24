import tkinter as tk  # Import tkinter for GUI creation
from meeting_scheduler import MeetingScheduler  # Import MeetingScheduler class
from styles import create_dashboard  # Import create_dashboard function for styling

def main():
    # Create the main window of the application
    root = tk.Tk()
    # Initialize the MeetingScheduler with the root window
    scheduler = MeetingScheduler(root)
    # Create the dashboard with the scheduler
    create_dashboard(root, scheduler)
    # Start the main event loop of the application
    root.mainloop()

# Check if the script is being run directly (not imported)
if __name__ == "__main__":
    # Call the main function to start the application
    main()
