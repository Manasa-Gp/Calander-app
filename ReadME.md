# Simple Calendar Application

## Overview

This is a command-line based Calendar and Event Manager that allows users to:

* Create non-overlapping events
* List all or remaining events for today
* View events on any specified date
* Find the next available free time slot of a specified duration for a given day

All data is stored in a `storage.json` file — no database is used.


##  Project Structure

```
calendar_app/
├── cli.py                  # Command-line interface
├── eventClass.py           # Event class (title, start_time, end_time, logic)
├── eventScheduler.py       # Scheduler class (event logic, I/O with storage.json)
├── storage.json            # Stores saved events
test events
├── README.md               # This file
├── presentation.pdf        # Design & usage walkthrough
```



## ▶️ How to Run

1. Ensure Python 3 is installed.
2. Clone the repo and navigate into the directory:

   ```bash
   git clone Calander-app
   cd calendar_app
   ```
3. Run the app:

   ```bash
   python cli.py
   ```



##  Input Format

All date/time inputs must follow this format:

```
MM-DD-YYYY HH:MM AM/PM
```

Example:

```
06-20-2025 02:30 PM
```



##  Features

* Prevents overlapping events
* Stores events in JSON
* Load and list events by date
* Lists only remaining events for today
* Finds next available time slot of specified duration



## 🧪 Example Usage

```
Welcome, select from the following options
1.Create Event	 2.List events	3.Show Free slots	4.quit
option: 1
Enter event title: Lunch
Enter start time as MM-DD-YYYY HH:MM AM/PM: 06-20-2025 01:00 PM
Enter end time as MM-DD-YYYY HH:MM AM/PM: 06-20-2025 02:00 PM
```

```
option: 3
Enter date (MM-DD-YYYY) or press enter for today: 06-20-2025
Enter required duration in minutes: 30
Available slot: 06-20-2025 02:00 PM - 06-20-2025 02:30 PM
```



## Design Overview 

* **Event Class:** Encapsulates event data and conflict logic
* **Scheduler Class:** Handles logic for event addition, time slot detection, and date filtering
* **CLI:** Input handling and interface flow



##  Notes

* All time comparisons are done using `datetime` objects internally
* Format validation and logic validation are separated cleanly


##  Future Enhancements

* Add multiple events
* Use natural language parsing
* Add GUI or web interface


## Author

* Manasa Pavushetty (GitHub: [@Manasa-Gp](https://github.com/Manasa-Gp))
