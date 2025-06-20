from eventClass import Event;
from eventScheduler import Scheduler;
from datetime import datetime
def parse_datetime(prompt):
    while True:
        user_input = input(prompt).strip()
        try:
            # Normalize AM/PM to uppercase before parsing
            user_input = user_input[:-2] + user_input[-2:].upper()
            return datetime.strptime(user_input, "%m-%d-%Y %I:%M %p")
        except ValueError:
            print("Invalid format. Use MM-DD-YYYY HH:MM AM/PM.")



def main():
    print("Welcome, select from the following options \n")
    schedule = Scheduler()
    while True:

        Option = input("1.Create Event\t 2.List events\t3.Show Free slots\t4.quit\noption: ").strip()

        if Option == "1" or Option.lower() == "Create Event":
            name = input("Enter event title: ")
            start_time = parse_datetime("Enter start time as MM-DD-YYYY HH:MM AM/PM: ")
            end_time = parse_datetime("Enter end time as MM-DD-YYYY HH:MM AM/PM: ")

            # Validation 1: Start time must be in the future
            if start_time < datetime.now():
                print("Cannot create an event in the past.")
                continue
            
            # Validation 2: End time must be after start time
            if end_time <= start_time:
                print("End time must be after start time.")
                continue

            new_event = Event(name,start_time,end_time)
            print("event_name:",new_event.title)
            schedule.addEvent(new_event)
        
        if Option == "2" or Option.lower() == "list events":
            sub = input("a. All today  b. Remaining today  c. Specific date\nchoice: ").lower().strip()
            if sub == "a":
                schedule.list_events_by_date(datetime.today().strftime("%m-%d-%Y"))
            elif sub == "b":
                schedule.list_remaining_events_today()
            elif sub == "c":
                date_input = input("Enter date (MM-DD-YYYY): ")
                schedule.list_events_by_date(date_input)

        if Option == "3" or Option.lower() == "show free slots":
            date = input("Enter date (MM-DD-YYYY) or press enter for today: ").strip()
            if not date:
                date = datetime.now().strftime("%m-%d-%Y")
            duration = int(input("Enter required duration in minutes: "))
            schedule.find_next_available_slot(date, duration)

        if Option == "4" or Option == "quit":
            break
    print("Thank you")

main();
    

        