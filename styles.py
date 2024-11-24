import tkinter as tk
from tkinter import ttk, messagebox
from n_queens import generate_optimal_schedule

def apply_styles(root):
    # Set the title and geometry of the root window
    root.title("Meeting Room Scheduler")
    root.geometry("1000x800")
    
    # Create a style object to configure the look and feel of ttk widgets
    style = ttk.Style()
    
    # Define modern color scheme for various ttk widgets
    style.configure('TFrame', background='#f0f5f9')  # Light blue for frames
    style.configure('TLabelframe', background='#f0f5f9')  # Light blue for label frames
    style.configure('TLabel', font=('Arial', 11), background='#f0f5f9')  # Arial font, light blue background for labels
    style.configure('TButton', 
                   font=('Arial', 11, 'bold'),
                   padding=12,
                   background='#1e88e5')  # Bold Arial font, padding, and blue background for buttons
    style.configure('Schedule.TButton',
                   padding=12,
                   font=('Arial', 11, 'bold'),
                   background='#4caf50')  # Custom style for 'Schedule' buttons
    style.configure('Refresh.TButton',
                   padding=12,
                   font=('Arial', 11, 'bold'),
                   background='#ff9800')  # Custom style for 'Refresh' buttons
    return style

def create_dashboard(root, scheduler):
    # Apply styles to the root window
    style = apply_styles(root)
    schedule_cells = {}
    
    def update_schedule_display():
        """Update the grid display with current meetings"""
        # Reset all cells to white before updating
        for cell in schedule_cells.values():
            cell.configure(background='white')
        
        # Iterate through each room and time slot to update the display
        for room in scheduler.rooms:
            for i, time_slot in enumerate(scheduler.time_slots):
                if time_slot in scheduler.meetings[room]:
                    cell = schedule_cells.get((room, i))
                    if cell:
                        cell.configure(background='#bbdefb')  # Light blue for scheduled meetings

    def schedule_meeting():
        """Handle scheduling a new meeting"""
        try:
            # Get the duration from the spinbox
            dur = int(duration.get())
            # Validate the duration
            if dur < 1 or dur > len(scheduler.time_slots):
                messagebox.showerror("Error", 
                    f"Please enter a valid duration (1-{len(scheduler.time_slots)} hours)")
                return
            # Set the duration for the scheduler
            scheduler.set_duration(dur)
            # Get the start time from the combobox
            start_time = time_var.get()
            
            if not start_time:
                messagebox.showerror("Error", "Please select a start time")
                return
            
            # Attempt to schedule the meeting
            room, time = scheduler.schedule_meeting(dur)
            if room:
                messagebox.showinfo("Success", 
                    f"Meeting scheduled in {room} at {time} for {dur} hour(s)")
                update_schedule_display()  # Update the display after scheduling
            else:
                messagebox.showerror("Error", 
                    "No available slots for this duration")
        except ValueError:
            messagebox.showerror("Error", 
                f"Please enter a valid duration (1-{len(scheduler.time_slots)} hours)")

    def refresh_schedule():
        """Clear all meetings and reset the display"""
        # Clear all meetings from the scheduler
        scheduler.clear_meetings()
        # Update the display to reflect the cleared schedule
        update_schedule_display()
        # Reset the duration and time selection
        duration.set("1")
        time_var.set("")
        messagebox.showinfo("Success", "Schedule cleared successfully!")

    def show_optimal_schedule():
        """Generate and display optimal schedule"""
        # Generate the optimal schedule
        generate_optimal_schedule(scheduler)
        # Update the display to reflect the optimal schedule
        update_schedule_display()

    # Now create the UI elements
    header_frame = ttk.Frame(root, style='Header.TFrame')
    header_frame.pack(fill=tk.X, pady=0)

    # Create a centered label for the header
    header_label = ttk.Label(header_frame, 
                            text="Meeting Room Scheduler", 
                            font=('Arial', 24, 'bold'),
                            foreground='white',
                            background='#1976d2',
                            padding=15)
    header_label.pack(fill=tk.X)

    # Configure text alignment to center
    header_label.configure(anchor='center', justify='center')

    # You can also add this style configuration
    style.configure('Header.TLabel',
                    anchor='center',
                    justify='center')

    # Create main container
    container = ttk.Frame(root)
    container.pack(fill=tk.BOTH, expand=True)

    # Create sidebar
    sidebar = ttk.Frame(container, style='Sidebar.TFrame')
    sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=0)
    
    # Sidebar content
    ttk.Label(sidebar, 
             text="Controls", 
             font=('Arial', 16, 'bold'),
             background='#f5f5f5',
             padding=10).pack(fill=tk.X)

    # Move duration and time controls to sidebar
    dur_frame = ttk.LabelFrame(sidebar, text="Meeting Duration", padding=10)
    dur_frame.pack(fill=tk.X, padx=10, pady=5)
    duration = ttk.Spinbox(dur_frame, 
                          from_=1, 
                          to=13,  # Maximum duration matches number of time slots
                          width=10, 
                          font=('Arial', 12))
    duration.set("1")
    duration.pack(fill=tk.X)

    time_frame = ttk.LabelFrame(sidebar, text="Start Time", padding=10)
    time_frame.pack(fill=tk.X, padx=10, pady=5)
    time_var = tk.StringVar()
    time_combo = ttk.Combobox(time_frame, 
                             textvariable=time_var,
                             values=scheduler.time_slots,
                             width=10, 
                             font=('Arial', 12))
    time_combo.pack(fill=tk.X)

    # Action buttons in sidebar
    button_frame = ttk.Frame(sidebar)
    button_frame.pack(fill=tk.X, padx=10, pady=10)
    
    ttk.Button(button_frame, 
               text="Schedule Meeting",
               command=schedule_meeting,
               style='Action.TButton').pack(fill=tk.X, pady=5)
    
    ttk.Button(button_frame,
               text="🔄 Refresh",
               command=refresh_schedule,
               style='Refresh.TButton').pack(fill=tk.X, pady=5)
    
    ttk.Button(button_frame,
               text="Generate Optimal",
               command=show_optimal_schedule,
               style='Schedule.TButton').pack(fill=tk.X, pady=5)

    # Main content area
    main_content = ttk.Frame(container)
    main_content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Schedule grid (existing code modified)
    schedule_frame = ttk.Frame(main_content)
    schedule_frame.pack(fill=tk.BOTH, expand=True)
    
    # Time headers with new style
    time_frame = ttk.Frame(schedule_frame)
    time_frame.grid(row=0, column=1, columnspan=len(scheduler.time_slots), sticky='ew')
    for i, time in enumerate(scheduler.time_slots):
        ttk.Label(time_frame, 
                 text=time,
                 font=('Arial', 10, 'bold'),
                 padding=5).grid(row=0, column=i, padx=1)

    # Create footer
    footer_frame = ttk.Frame(root, style='Footer.TFrame')
    footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
    ttk.Label(footer_frame,
             text="© 2024 Meeting Room Scheduler",
             font=('Arial', 10),
             padding=10).pack()

    # Add new styles
    style.configure('Header.TFrame', background='#1976d2')
    style.configure('Sidebar.TFrame', background='#f5f5f5')
    style.configure('Footer.TFrame', background='#f5f5f5')
    style.configure('Action.TButton', 
                   font=('Arial', 12, 'bold'),
                   padding=10,
                   background='#2196f3')
    
    # Update cell styling for better visibility
    for i, room in enumerate(scheduler.rooms):
        ttk.Label(schedule_frame, 
                 text=room,
                 font=('Arial', 10, 'bold'),
                 padding=5).grid(row=i+1, column=0, padx=5, pady=2)
        for j in range(len(scheduler.time_slots)):
            cell = ttk.Label(schedule_frame, 
                           width=8,  # Reduced width for more slots
                           relief='solid',
                           background='white',
                           font=('Arial', 9))
            cell.grid(row=i+1, column=j+1, padx=1, pady=1, ipadx=2, ipady=2)
            schedule_cells[(room, j)] = cell
    
    # Initial display
    update_schedule_display()
