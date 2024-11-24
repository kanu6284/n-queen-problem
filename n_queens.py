import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class NQueensSolver:
    """Class to solve the N-Queens problem for meeting scheduling"""
    def __init__(self):
        self.solutions = []  # Store potential solutions


    def is_safe(self, board, row, col, n):
        """Check if a queen can be placed on board[row][col]"""
        # Check row on left side
        for i in range(col):
            if board[row][i] == 1:
                return False

        # Check upper diagonal on left side
        for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
            if board[i][j] == 1:
                return False

        # Check lower diagonal on left side
        for i, j in zip(range(row, n, 1), range(col, -1, -1)):
            if board[i][j] == 1:
                return False

        return True

    def solve_n_queens(self, board, col, n):
        """Recursive function to solve N-Queens problem"""
        # Base case: If all queens are placed, return True
        if col >= n:
            return True

        # Consider this column and try placing this queen in all rows one by one
        for i in range(n):
            if self.is_safe(board, i, col, n):
                board[i][col] = 1  # Place the queen
                
                # Recur to place rest of the queens
                if self.solve_n_queens(board, col + 1, n):
                    return True
                
                # If placing queen doesn't lead to a solution, backtrack
                board[i][col] = 0

        return False

    def solve(self, n):
        """Initialize board and solve N-Queens"""
        board = np.zeros((n, n), dtype=int)  # Create empty board
        if self.solve_n_queens(board, 0, n):
            return board
        return None

def show_solution_visualization(solution, scheduler):
    """Display the N-Queens solution as a meeting schedule visualization"""
    # Create new window for visualization
    viz_window = tk.Toplevel(scheduler.root)
    viz_window.title("Meeting Schedule Visualization")
    viz_window.geometry("800x800")

    # Create matplotlib figure
    fig, ax = plt.subplots(figsize=(10, 8))
    n = len(scheduler.rooms)
    time_slots = len(scheduler.time_slots)
    
    # Clear any existing plots
    plt.clf()
    ax = plt.gca()
    
    # Create checkerboard pattern
    for i in range(n):
        for j in range(time_slots):
            # Alternate colors for checkerboard
            color = 'lightgray' if (i + j) % 2 == 0 else 'white'
            ax.add_patch(plt.Rectangle((j, n-1-i), 1, 1, facecolor=color))

    # Add meetings based on actual schedule
    for i, room in enumerate(scheduler.rooms):
        meetings = scheduler.meetings[room]
        if meetings:  # If there are meetings in this room
            start_time = meetings[0]  # Get first meeting time
            start_index = scheduler.time_slots.index(start_time)
            
            # Fill all slots from start to end with light blue
            for j in range(start_index, time_slots):
                rect = plt.Rectangle((j, n-1-i), 1, 1, 
                                  facecolor='lightblue', 
                                  alpha=0.6)
                ax.add_patch(rect)
            
            # Add blue circle to mark meeting start
            circle = plt.Circle((start_index + 0.5, n-0.5-i), 
                              0.3, 
                              color='blue', 
                              alpha=0.8)
            ax.add_patch(circle)

    # Set axis properties
    ax.set_xlim(0, time_slots)
    ax.set_ylim(0, n)
    
    # Set ticks and labels
    ax.set_xticks(np.arange(time_slots) + 0.5)
    ax.set_yticks(np.arange(n) + 0.5)
    ax.set_xticklabels(scheduler.time_slots, rotation=45)
    ax.set_yticklabels(list(reversed(scheduler.rooms)))
    
    ax.grid(True)
    plt.title(f"Meeting Schedule Visualization\nDuration: {scheduler.current_duration} hours")

    # Add padding around plot
    plt.tight_layout()

    # Create canvas and add to window
    canvas = FigureCanvasTkAgg(fig, master=viz_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # Add close button
    ttk.Button(
        viz_window, 
        text="Close", 
        command=viz_window.destroy
    ).pack(pady=10)

def generate_optimal_schedule(scheduler):
    """Generate an optimal schedule using N-Queens algorithm"""
    n = len(scheduler.rooms)  # Use number of rooms for N-Queens
    solver = NQueensSolver()
    solution = solver.solve(n)
    
    if solution is not None:
        scheduler.clear_meetings()  # Clear existing meetings
        
        # Schedule meetings based on the solution and duration
        for row in range(n):
            for col in range(len(scheduler.time_slots)):
                if solution[row][col] == 1:
                    room = scheduler.rooms[row]
                    # Schedule meeting for the specified duration
                    for i in range(min(int(scheduler.current_duration), 
                                    len(scheduler.time_slots) - col)):
                        time_slot = scheduler.time_slots[col + i]
                        scheduler.meetings[room].append(time_slot)
                    break  # Move to next room after scheduling
        
        show_solution_visualization(solution, scheduler)
        return True
    return False
