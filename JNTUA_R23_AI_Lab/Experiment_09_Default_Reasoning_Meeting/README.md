# Experiment 9: Meeting Scheduling Using Default Reasoning

**Artificial Intelligence Lab | Subject Code 23A31301P | JNTUA R23 | B.Tech AI & DS**

## Aim

To schedule a meeting among five busy people (find a day, time and place) using default reasoning, and to document the assumptions.

## Theory

**Default reasoning** draws conclusions that are true *normally* unless contradicted. It is **non-monotonic**: adding new information can remove a conclusion that was previously valid.

**Default rule used:** *a person (or room) is AVAILABLE unless marked BUSY.* Only the busy periods are stored; everything else is assumed free. A meeting slot is accepted if no participant is marked busy and some room is not booked. When new busy information arrives, the earlier conclusion is **withdrawn** and a new slot is searched.

**Assumptions:** working days Monday-Friday; working hours 09:00-17:00; one-hour time slots; 12:00-13:00 is lunch for everybody; all five people and one room are required for the whole duration; the earliest suitable slot is chosen; sample busy schedules are invented for demonstration.

## Algorithm / Procedure

1. Store the busy periods (day, start hour, end hour) of the five people and of three rooms.
2. Ask for the meeting duration (1-3 hours).
3. For each day (Monday to Friday) and each start hour in working time:
   1. Skip the slot if it overlaps lunch.
   2. Apply the default rule: the slot is acceptable if nobody is marked busy during any hour of the meeting.
   3. Find a room that is not booked for the whole meeting.
   4. The first acceptable slot found is the earliest.
4. Print the day, time and place; verify the answer against all busy entries.
5. **Non-monotonic step:** mark one participant busy at the chosen time, withdraw the old conclusion, and search again.

## Source Code

The complete program is in [`main.py`](main.py) and is reproduced here.

```python
"""
Experiment 9: Meeting Scheduling Using Default Reasoning
Subject: Artificial Intelligence Lab (23A31301P) - JNTUA R23

Default reasoning = draw a conclusion unless there is information to the contrary.
  DEFAULT RULE : "a person (or room) is AVAILABLE unless marked BUSY."
This is non-monotonic: new information (a new busy entry) can WITHDRAW a
conclusion that was reached earlier. The program shows this at the end.

ASSUMPTIONS (documented on purpose):
  1. Working days are Monday-Friday; working hours are 09:00-17:00.
  2. Time is split into whole-hour slots (09-10, 10-11, ...).
  3. 12:00-13:00 is a lunch break for everybody, so no meeting is scheduled then.
  4. A meeting needs ALL five people and ONE free room for its full duration.
  5. Anything not listed as busy is assumed free (the default rule).
  6. The earliest suitable slot (first day, first hour) is chosen.
"""

PEOPLE = ["Alice", "Bob", "Charlie", "Diana", "Eve"]
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
WORK_START, WORK_END = 9, 17
LUNCH = (12, 13)

# Explicitly known busy periods: (day, start hour, end hour)
BUSY = {
    "Alice":   [("Monday", 9, 12), ("Monday", 14, 17), ("Tuesday", 9, 11), ("Wednesday", 13, 15)],
    "Bob":     [("Monday", 10, 12), ("Monday", 13, 17), ("Tuesday", 10, 13), ("Tuesday", 15, 17)],
    "Charlie": [("Monday", 9, 11), ("Monday", 14, 16), ("Tuesday", 9, 10), ("Tuesday", 11, 14)],
    "Diana":   [("Monday", 9, 17), ("Tuesday", 13, 14), ("Tuesday", 16, 17)],
    "Eve":     [("Monday", 11, 13), ("Tuesday", 9, 10), ("Tuesday", 14, 16), ("Wednesday", 9, 10)],
}

# Rooms (places) and their booked periods
ROOM_BUSY = {
    "Conference Room A": [("Monday", 9, 17), ("Tuesday", 9, 12), ("Wednesday", 9, 11)],
    "Seminar Hall":      [("Tuesday", 9, 11), ("Tuesday", 14, 17), ("Wednesday", 9, 10)],
    "AI Lab":            [("Monday", 9, 17), ("Tuesday", 9, 10), ("Wednesday", 9, 10)],
}


def ask(prompt, default):
    try:
        text = input(prompt).strip()
    except EOFError:
        return default
    return text if text else default


def is_marked_busy(schedule, day, hour):
    """True only if the hour lies inside an explicitly listed busy period."""
    return any(d == day and start <= hour < end for d, start, end in schedule)


def is_available(schedule, day, hour):
    """DEFAULT RULE: available unless there is a busy entry for that hour."""
    return not is_marked_busy(schedule, day, hour)


def find_meeting(busy, room_busy, duration):
    """
    Return (day, start_hour, room) for the earliest slot where all five people
    are available and a room is free for `duration` consecutive hours; else None.
    """
    for day in DAYS:
        for start in range(WORK_START, WORK_END - duration + 1):
            hours = range(start, start + duration)
            if any(LUNCH[0] <= h < LUNCH[1] for h in hours):
                continue                                    # lunch break
            if not all(is_available(busy[p], day, h) for p in PEOPLE for h in hours):
                continue
            for room, booked in room_busy.items():
                if all(is_available(booked, day, h) for h in hours):
                    return day, start, room
    return None


def print_availability_table(busy, duration_hours=1):
    """Table: how many of the 5 people are available in each hour (5 = everyone)."""
    hours = range(WORK_START, WORK_END)
    print("People available per hour (5 = everyone free; L = lunch):")
    print("          " + " ".join(f"{h:02d}:00" for h in hours))
    for day in DAYS:
        cells = []
        for h in hours:
            if LUNCH[0] <= h < LUNCH[1]:
                cells.append("  L  ")
            else:
                count = sum(is_available(busy[p], day, h) for p in PEOPLE)
                cells.append(f"  {count}  ")
        print(f"{day:<10}" + " ".join(cells))


def report(result, duration):
    if result is None:
        print("No common slot found: nobody can attend together under the assumptions.")
        return
    day, start, room = result
    print(f"Meeting scheduled -> Day: {day} | Time: {start:02d}:00-{start + duration:02d}:00 "
          f"| Place: {room}")


def verify(result, busy, room_busy, duration):
    """Re-check the answer slot against every busy entry."""
    day, start, room = result
    hours = range(start, start + duration)
    people_ok = all(not is_marked_busy(busy[p], day, h) for p in PEOPLE for h in hours)
    room_ok = all(not is_marked_busy(room_busy[room], day, h) for h in hours)
    lunch_ok = not any(LUNCH[0] <= h < LUNCH[1] for h in hours)
    return people_ok and room_ok and lunch_ok and WORK_START <= start and start + duration <= WORK_END


def main():
    print("=" * 60)
    print("EXPERIMENT 9: MEETING SCHEDULING USING DEFAULT REASONING")
    print("=" * 60)
    print("Participants:", ", ".join(PEOPLE))
    print("Rooms       :", ", ".join(ROOM_BUSY))
    print("Default rule: a person/room is AVAILABLE unless marked BUSY.\n")

    while True:
        text = ask("Meeting duration in hours (1-3) [1]: ", "1")
        if text in ("1", "2", "3"):
            duration = int(text)
            break
        print("  Please enter 1, 2 or 3.")

    print("\nKnown busy schedules:")
    for person in PEOPLE:
        periods = ", ".join(f"{d[:3]} {s:02d}-{e:02d}" for d, s, e in BUSY[person])
        print(f"  {person:<8}: {periods}")
    print()
    print_availability_table(BUSY)

    print("\nStep 1 - reason with the default rule:")
    result = find_meeting(BUSY, ROOM_BUSY, duration)
    report(result, duration)
    if result is None:
        return
    print("Verification against all busy entries:", verify(result, BUSY, ROOM_BUSY, duration))

    # Non-monotonic reasoning: new information retracts the earlier conclusion.
    day, start, _ = result
    victim = PEOPLE[-1]
    print(f"\nStep 2 - NEW INFORMATION: {victim} is marked busy on {day} "
          f"{start:02d}:00-{start + duration:02d}:00.")
    updated = {p: list(s) for p, s in BUSY.items()}
    updated[victim].append((day, start, start + duration))
    print(f"The default conclusion 'all five can meet at {day} {start:02d}:00' is WITHDRAWN.")
    new_result = find_meeting(updated, ROOM_BUSY, duration)
    report(new_result, duration)
    if new_result:
        print("Verification against updated busy entries:",
              verify(new_result, updated, ROOM_BUSY, duration))


if __name__ == "__main__":
    main()
```

## Sample Input

Duration 1 hour (press Enter). You can also enter 2 or 3. The sample busy schedules are printed by the program.

## Expected Output

The outputs below were produced by actually running `main.py` (Python 3.12) with the inputs shown; text after each prompt is the input that was typed.

**Default duration (1 hour)**

```text
============================================================
EXPERIMENT 9: MEETING SCHEDULING USING DEFAULT REASONING
============================================================
Participants: Alice, Bob, Charlie, Diana, Eve
Rooms       : Conference Room A, Seminar Hall, AI Lab
Default rule: a person/room is AVAILABLE unless marked BUSY.

Meeting duration in hours (1-3) [1]: 

Known busy schedules:
  Alice   : Mon 09-12, Mon 14-17, Tue 09-11, Wed 13-15
  Bob     : Mon 10-12, Mon 13-17, Tue 10-13, Tue 15-17
  Charlie : Mon 09-11, Mon 14-16, Tue 09-10, Tue 11-14
  Diana   : Mon 09-17, Tue 13-14, Tue 16-17
  Eve     : Mon 11-13, Tue 09-10, Tue 14-16, Wed 09-10

People available per hour (5 = everyone free; L = lunch):
          09:00 10:00 11:00 12:00 13:00 14:00 15:00 16:00
Monday      2     1     1     L     3     1     1     2  
Tuesday     2     3     3     L     3     4     3     3  
Wednesday   4     5     5     L     4     4     5     5  
Thursday    5     5     5     L     5     5     5     5  
Friday      5     5     5     L     5     5     5     5  

Step 1 - reason with the default rule:
Meeting scheduled -> Day: Wednesday | Time: 10:00-11:00 | Place: Seminar Hall
Verification against all busy entries: True

Step 2 - NEW INFORMATION: Eve is marked busy on Wednesday 10:00-11:00.
The default conclusion 'all five can meet at Wednesday 10:00' is WITHDRAWN.
Meeting scheduled -> Day: Wednesday | Time: 11:00-12:00 | Place: Conference Room A
Verification against updated busy entries: True
```

**Duration 3 hours**

```text
============================================================
EXPERIMENT 9: MEETING SCHEDULING USING DEFAULT REASONING
============================================================
Participants: Alice, Bob, Charlie, Diana, Eve
Rooms       : Conference Room A, Seminar Hall, AI Lab
Default rule: a person/room is AVAILABLE unless marked BUSY.

Meeting duration in hours (1-3) [1]: 3

Known busy schedules:
  Alice   : Mon 09-12, Mon 14-17, Tue 09-11, Wed 13-15
  Bob     : Mon 10-12, Mon 13-17, Tue 10-13, Tue 15-17
  Charlie : Mon 09-11, Mon 14-16, Tue 09-10, Tue 11-14
  Diana   : Mon 09-17, Tue 13-14, Tue 16-17
  Eve     : Mon 11-13, Tue 09-10, Tue 14-16, Wed 09-10

People available per hour (5 = everyone free; L = lunch):
          09:00 10:00 11:00 12:00 13:00 14:00 15:00 16:00
Monday      2     1     1     L     3     1     1     2  
Tuesday     2     3     3     L     3     4     3     3  
Wednesday   4     5     5     L     4     4     5     5  
Thursday    5     5     5     L     5     5     5     5  
Friday      5     5     5     L     5     5     5     5  

Step 1 - reason with the default rule:
Meeting scheduled -> Day: Thursday | Time: 09:00-12:00 | Place: Conference Room A
Verification against all busy entries: True

Step 2 - NEW INFORMATION: Eve is marked busy on Thursday 09:00-12:00.
The default conclusion 'all five can meet at Thursday 09:00' is WITHDRAWN.
Meeting scheduled -> Day: Thursday | Time: 13:00-16:00 | Place: Conference Room A
Verification against updated busy entries: True
```

**Invalid duration then 2**

```text
============================================================
EXPERIMENT 9: MEETING SCHEDULING USING DEFAULT REASONING
============================================================
Participants: Alice, Bob, Charlie, Diana, Eve
Rooms       : Conference Room A, Seminar Hall, AI Lab
Default rule: a person/room is AVAILABLE unless marked BUSY.

Meeting duration in hours (1-3) [1]: 7
  Please enter 1, 2 or 3.
Meeting duration in hours (1-3) [1]: 2

Known busy schedules:
  Alice   : Mon 09-12, Mon 14-17, Tue 09-11, Wed 13-15
  Bob     : Mon 10-12, Mon 13-17, Tue 10-13, Tue 15-17
  Charlie : Mon 09-11, Mon 14-16, Tue 09-10, Tue 11-14
  Diana   : Mon 09-17, Tue 13-14, Tue 16-17
  Eve     : Mon 11-13, Tue 09-10, Tue 14-16, Wed 09-10

People available per hour (5 = everyone free; L = lunch):
          09:00 10:00 11:00 12:00 13:00 14:00 15:00 16:00
Monday      2     1     1     L     3     1     1     2  
Tuesday     2     3     3     L     3     4     3     3  
Wednesday   4     5     5     L     4     4     5     5  
Thursday    5     5     5     L     5     5     5     5  
Friday      5     5     5     L     5     5     5     5  

Step 1 - reason with the default rule:
Meeting scheduled -> Day: Wednesday | Time: 10:00-12:00 | Place: Seminar Hall
Verification against all busy entries: True

Step 2 - NEW INFORMATION: Eve is marked busy on Wednesday 10:00-12:00.
The default conclusion 'all five can meet at Wednesday 10:00' is WITHDRAWN.
Meeting scheduled -> Day: Wednesday | Time: 15:00-17:00 | Place: Conference Room A
Verification against updated busy entries: True
```

## Result

For a 1-hour meeting the program schedules Wednesday 10:00-11:00 in the Seminar Hall; all busy entries are respected. When Eve is then marked busy, the conclusion is withdrawn and a new slot (Wednesday 11:00-12:00, Conference Room A) is found - illustrating non-monotonic default reasoning.

## How to Run

```bat
cd Experiment_09_Default_Reasoning_Meeting
python main.py
```

From the project root you can also run `run_experiment.bat 9`.
