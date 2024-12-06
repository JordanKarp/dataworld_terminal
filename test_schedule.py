import random
from datetime import timedelta, datetime

# Define the activities
activities = ["Home", "Travel", "Work", "Gym", "Shopping", "Friends", "Other"]


# Function to get a random time delta
def random_time_delta(min_minutes, max_minutes):
    return timedelta(minutes=random.randint(min_minutes, max_minutes))


# Generate a schedule for a person
def generate_schedule():
    schedule = []

    # Starting at home
    start_time = datetime.strptime("00:00", "%H:%M")
    end_time = start_time + timedelta(hours=8)
    schedule.append(("Home", start_time, end_time))

    # Travel to work
    start_time = end_time
    end_time = start_time + random_time_delta(15, 45)
    schedule.append(("Travel to Work", start_time, end_time))

    # Working hours
    start_time = end_time
    end_time = start_time + timedelta(hours=8)
    schedule.append(("Work", start_time, end_time))

    # Optionally visit 1-3 other places
    num_activities = random.randint(1, 3)
    for _ in range(num_activities):
        # Travel to next place
        start_time = end_time
        end_time = start_time + random_time_delta(15, 45)
        schedule.append(("Travel", start_time, end_time))

        # Random activity duration
        start_time = end_time
        activity = random.choice(activities[2:])  # Exclude Home and Work for variety
        end_time = start_time + random_time_delta(30, 120)
        schedule.append((activity, start_time, end_time))

    # Travel back home
    start_time = end_time
    end_time = start_time + random_time_delta(15, 45)
    schedule.append(("Travel Home", start_time, end_time))

    # End the day at home
    start_time = end_time
    schedule.append(("Home", start_time, datetime.strptime("23:59", "%H:%M")))

    return schedule


# Pretty print the schedule
def print_schedule(schedule):
    for activity, start, end in schedule:
        print(f"{activity}: {start.strftime('%H:%M')} - {end.strftime('%H:%M')}")


# Generate and print a schedule
schedule = generate_schedule()
print_schedule(schedule)
