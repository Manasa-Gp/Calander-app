import json
import os
from eventClass import Event;
from datetime import datetime,timedelta
class Scheduler:
    # Initialize the scheduler with existing events from storage.json file if it exists, 
    # otherwise create a new one.  If storage.json file is invalid, it will be created with an empty list of events
    def __init__(self):
        self.path = "storage.json"
        self.events = []

        if not os.path.exists(self.path):
            with open(self.path, 'w') as f:
                json.dump([], f)

        with open(self.path, 'r') as file:
            try:
                data = json.load(file)
                for e in data:
                    try:
                        self.events.append(Event.from_dict(e))
                    except Exception as err:
                        print(f"Skipping invalid event: {e}\nReason: {err}")
            except json.JSONDecodeError:
                print("Invalid JSON structure. Starting with empty event list.")
                self.events = []

    # Convert all events to dict before writing it to storage.json file
    def addEvent(self, event_new):
        for event in self.events:
            if event_new.eventOverlap(event):
                print(f"Event {event_new.title} overlaps with event {event.title}.")
                return 
        self.events.append(event_new)

        # Convert all events to dict just before writing
        with open(self.path, 'w') as file:
            json.dump([e.to_dict() for e in self.events], file, indent=2)

        return "Event added successfully."

    # List all events for a given date, sorted by start time
    def list_events_by_date(self, date_str):
        found = False
        try:
            date_obj = datetime.strptime(date_str, "%m-%d-%Y").date()
        except ValueError:
            print("Invalid date format. Use MM-DD-YYYY.")
            return

        # Filter events for the date
        events_by_date = [
            event for event in self.events
            if isinstance(event, Event) and event.start_time.date() <= date_obj <= event.end_time.date()
        ]

        # Sort by start time
        events_by_date.sort(key=lambda e: e.start_time)

        for event in events_by_date:
            found = True
            print(f"Event: {event.title}")

            if event.start_time.date() == event.end_time.date():
                print(f"Start Time: {event.start_time.strftime('%I:%M %p')}")
                print(f"End Time:   {event.end_time.strftime('%I:%M %p')}")
            else:
                print(f"Start Time: {event.start_time.strftime('%m-%d-%Y %I:%M %p')}")
                print(f"End Time:   {event.end_time.strftime('%m-%d-%Y %I:%M %p')}")
                print("Note: This is an overnight event.")
            print("-" * 30)

        if not found:
            print(f"No events scheduled for {date_str}.")


    # List all remaining events for today, sorted by start time
    def list_remaining_events_today(self):
        now = datetime.now()
        remaining_today = [
            e for e in self.events
            if e.start_time.date() == now.date() and e.start_time.time() > now.time()
        ]

        if not remaining_today:
            print("No remaining events for today.")
            return

        # Sort remaining events by start_time
        remaining_today.sort(key=lambda e: e.start_time)

        for event in remaining_today:
            print(f"Event: {event.title}")
            print(f"Start Time: {event.start_time.strftime('%I:%M %p')}")
            if event.end_time.date() > event.start_time.date():
                # Overnight event – show date as well
                print(f"End Time: {event.end_time.strftime('%m-%d-%Y %I:%M %p')} (overnight)")
            else:
                print(f"End Time: {event.end_time.strftime('%I:%M %p')}")
            print("-" * 30)


    # Find the next available slot for a given date and duration
    def find_next_available_slot(self, date_str, duration_minutes):
        
        # Normalize time to start at midnight and ignore seconds and microseconds to avoid rounding errors
        now = datetime.now().replace(second=0, microsecond=0)
        date_obj = datetime.strptime(date_str, "%m-%d-%Y").date()  
        is_today = date_obj == now.date()  # Check if the date is today or not
        required_duration = timedelta(minutes=duration_minutes) # Convert duration to timedelta object

        # Filter and sort events for the specified date
        events_on_date = sorted(
            [e for e in self.events if e.start_time.date() <= date_obj <= e.end_time.date()],
            key=lambda e: e.start_time
        )

        # Start checking for a timeslot from now (if today) or from midnight (if another day)
        start_check = now if is_today else datetime.strptime(date_str + " 12:00 AM", "%m-%d-%Y %I:%M %p")


        # Check slot before first event 
        if not events_on_date or (events_on_date[0].start_time - start_check >= required_duration):
            print(f"Available slot: {start_check.strftime('%m-%d-%Y %I:%M %p')} - {(start_check + required_duration).strftime('%m-%d-%Y %I:%M %p')}")
            return

        # Check gaps between events to find a suitable slot
        for i in range(len(events_on_date) - 1):
            end_current = events_on_date[i].end_time.replace(second=0, microsecond=0)
            start_next = events_on_date[i + 1].start_time.replace(second=0, microsecond=0)

            if end_current < start_check:
                continue  # skip past events

            gap_start = max(end_current, start_check)
            gap = start_next - gap_start

            if gap >= required_duration:
                print(f"Available slot: {gap_start.strftime('%m-%d-%Y %I:%M %p')} - {(gap_start + required_duration).strftime('%m-%d-%Y %I:%M %p')}")
                return

        # Check for slot after last event
        last_end = events_on_date[-1].end_time.replace(second=0, microsecond=0)
        if last_end < start_check:
            last_end = start_check

        # Final check after last event
        if (last_end + required_duration).date() > date_obj:
            print(f"No free slot available on {date_str}.")
        print(f"Available slot: {last_end.strftime('%m-%d-%Y %I:%M %p')} - {(last_end + required_duration).strftime('%m-%d-%Y %I:%M %p')}")

                


