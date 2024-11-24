class MeetingScheduler:
    def __init__(self, root):
        """
        Initialize the MeetingScheduler with the root window.
        Store the root window, define available time slots and rooms,
        initialize a dictionary to keep track of scheduled meetings,
        and set a default meeting duration.
        """
        self.root = root  # Store root window
        self.time_slots = [
            "8:00", "9:00", "10:00", "11:00", "12:00", 
            "13:00", "14:00", "15:00", "16:00", "17:00",
            "18:00", "19:00", "20:00"
        ]
        self.rooms = [
            "Room A", "Room B", "Room C", "Room D",
            "Room E", "Room F", "Room G", "Room H",
            "Conference Hall 1", "Conference Hall 2",
            "Meeting Room 1", "Meeting Room 2"
        ]
        self.meetings = {room: [] for room in self.rooms}  # Initialize meetings dictionary
        self.current_duration = "1"  # Default duration

    def schedule_meeting(self, duration):
        """
        Attempt to schedule a meeting with the given duration.
        Check if the duration is valid, then try to find an available time slot
        in each room. If a suitable time slot is found, schedule the meeting.
        """
        # First check if duration is valid for available time slots
        if duration > len(self.time_slots):
            print(f"Duration {duration} exceeds available time slots")
            return None, None
        
        print(f"Attempting to schedule meeting with duration {duration}")
        
        for room in self.rooms:
            for i, start_time in enumerate(self.time_slots):
                if i + duration <= len(self.time_slots):  # Check if there's enough time slots
                    # Check if all required slots are available
                    slots_needed = self.time_slots[i:i + duration]
                    if all(slot not in self.meetings[room] for slot in slots_needed):
                        # Schedule the meeting
                        self.meetings[room].extend(slots_needed)
                        print(f"Scheduled meeting in {room} starting at {start_time}")
                        return room, start_time
        
        print("No available slots found")
        return None, None

    def is_slot_available(self, room, start_index, duration):
        """
        Check if consecutive slots are available in a given room.
        """
        if start_index + duration > len(self.time_slots):
            return False
        
        needed_slots = self.time_slots[start_index:start_index + duration]
        return all(slot not in self.meetings[room] for slot in needed_slots)

    def clear_meetings(self):
        """
        Clear all scheduled meetings from the meetings dictionary.
        """
        self.meetings = {room: [] for room in self.rooms}

    def set_duration(self, duration):
        """
        Set the current meeting duration.
        """
        self.current_duration = str(duration)
