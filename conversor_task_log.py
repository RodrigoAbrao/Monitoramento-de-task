import csv
from collections import defaultdict
from datetime import datetime, timedelta


def sum_daily_tasks(file_name):
    daily_tasks = defaultdict(float)

    with open(file_name, 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            daily_tasks[row['date']] += float(row['elapsed_time'])

    return dict(daily_tasks)


def seconds_to_hours_minutes(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    return hours, minutes


def convert_csv_format(input_file, output_file):
    daily_tasks = sum_daily_tasks(input_file)

    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['date', 'elapsed_time_hours', 'elapsed_time_minutes']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for day, elapsed_time in daily_tasks.items():
            hours, minutes = seconds_to_hours_minutes(elapsed_time)
            writer.writerow(
                {'date': day, 'elapsed_time_hours': hours, 'elapsed_time_minutes': minutes})


input_file = 'task_log.csv'
output_file = 'converted_task_log.csv'
convert_csv_format(input_file, output_file)
