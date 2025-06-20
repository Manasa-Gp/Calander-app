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
    print("Welcome, select from the following options. You can enter the option number or name \n")
    schedule = Scheduler()
    while True:

        Option = input("1.Create Event\t 2.List events\t3.Show Free slots\t4.quit\noption: ").strip()

        if Option == "1" or Option.lower() == "create event":
            name = input("Enter event title: ")
            if not name:
                print("Event title cannot be empty.")
                continue
            start_time = parse_datetime("Enter start time as MM-DD-YYYY HH:MM AM/PM: ")
            end_time = parse_datetime("Enter end time as MM-DD-YYYY HH:MM AM/PM: ")

            # Start time must be in the future
            if start_time < datetime.now():
                print("Cannot create an event in the past.")
                continue
            
            # End time must be after start time
            if end_time <= start_time:
                print("End time must be after start time.")
                continue

            new_event = Event(name,start_time,end_time)
            print("event_name:",new_event.title)
            schedule.addEvent(new_event)
        
        elif Option == "2" or Option.lower() == "list events":
            sub = input("a. All today  b. Remaining today  c. Specific date\nchoice: ").lower().strip()
            if sub == "a":
                schedule.list_events_by_date(datetime.today().strftime("%m-%d-%Y"))
            elif sub == "b":
                schedule.list_remaining_events_today()
            elif sub == "c":
                date_input = input("Enter date (MM-DD-YYYY): ")
                try:
                    datetime.strptime(date_input, "%m-%d-%Y")  
                except ValueError:
                    print("Invalid date format. Please use MM-DD-YYYY.")
                    continue
                schedule.list_events_by_date(date_input)

        elif Option == "3" or Option.lower() == "show free slots":
            while True:
                date = input("Enter date (MM-DD-YYYY) or press enter for today: ").strip()
                if not date:
                    date = datetime.now().strftime("%m-%d-%Y")
                    break
                try:
                    datetime.strptime(date, "%m-%d-%Y")  
                    break  
                except ValueError:
                    print("Invalid date format. Please use MM-DD-YYYY.")
                    continue  
            
            while True:
                try:
                    duration = int(input("Enter required duration in minutes: "))
                    if duration <= 0:
                        print("Please enter a positive integer.")
                        continue
                    break
                except ValueError:
                    print("Invalid input. Please enter a number.")
            
            schedule.find_next_available_slot(date, duration)

        elif Option == "4" or Option.lower() == "quit":
            break
        else:
            print("Invalid option. Please choose 1, 2, 3, or 4 or enter the option name.")

    print("Thank you")

main();
    

        