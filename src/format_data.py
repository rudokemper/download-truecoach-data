import os
import json
import re

from datetime import datetime, timedelta

def format_workout(workout, workout_items):
    warmup = workout.get('warmup')
    workout_item_ids = workout.get('workout_item_ids', [])
    if not warmup and not workout_item_ids:
        return ""

    due_date = datetime.strptime(workout['due'], "%Y-%m-%d")
    day_of_week = due_date.strftime('%A')

    markdown = "# {}, {}: \"{}\"\n\n".format(day_of_week, workout['due'], workout['title'])

    short_description = workout['short_description']
    match = re.search("<p class='name-and-info'>(.*?)</p>", short_description)
    if match:
        short_description = match.group(1).replace('<br/>', '\n')

    if warmup:
        markdown += "## Warmup\n{}\n\n".format(warmup.replace('\n', '  \n'))

    if workout_item_ids:
        markdown += "## Workouts\n"
        short_description_items = short_description.split('\n')

        for i, workout_item_id in enumerate(workout_item_ids):
            for item in workout_items:
                if item['id'] == workout_item_id:
                    prefix = short_description_items[i].split(' ')[0] if i < len(short_description_items) else ''
                    markdown += "### {} {}\n".format(prefix, item['name'])
                    markdown += "{}\n".format(item['info'].replace('\n', '  \n'))
                    if item['result']:
                        result = '\n'.join(f"*{line}*" for line in item['result'].split('\n'))
                        markdown += "\n##### Result\n{}\n".format(result)
                    markdown += "\n"
    return markdown

def generate_markdown():
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Get the path to the 'data' directory
    data_dir = os.path.join(script_dir, '..', 'data')

    # Create the data directory if it doesn't exist
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # Get the path to the 'outputs' directory
    outputs_dir = os.path.join(script_dir, '..', 'outputs')

    # List the JSON files in the 'data' directory
    json_files = sorted([f for f in os.listdir(data_dir) if f.endswith('.json')])

    all_workouts = []
    all_workout_items = []
    for json_file in json_files:
        with open(f'data/{json_file}') as file:
            data = json.load(file)
            all_workout_items.extend(data['workout_items'])
            all_workouts.extend(data['workouts'])

    all_workouts.sort(key=lambda x: datetime.strptime(x['due'], "%Y-%m-%d"))
    workouts_by_week = {}
    for workout in all_workouts:
        workout_date = datetime.strptime(workout['due'], "%Y-%m-%d")
        # Calculate the start of the week (Monday)
        start_of_week = workout_date - timedelta(days=workout_date.weekday())
        if start_of_week not in workouts_by_week:
            workouts_by_week[start_of_week] = []
        workouts_by_week[start_of_week].append(workout)

    markdowns = {}
    for start_of_week, workouts in workouts_by_week.items():
        workouts.sort(key=lambda x: datetime.strptime(x['due'], "%Y-%m-%d"))  # Sort workouts by date within each week
        for workout in workouts:
            if start_of_week not in markdowns:
                markdowns[start_of_week] = ""
            markdowns[start_of_week] += format_workout(workout, all_workout_items)

    for start_of_week, markdown in markdowns.items():
        end_of_week = start_of_week + timedelta(days=6)  # Calculate the end of the week (Sunday)
        filename = f'{start_of_week.year} - {start_of_week.strftime("%m.%d")} to {end_of_week.strftime("%m.%d")}.md'
        file_path = os.path.join(outputs_dir, filename)
        if not os.path.exists(outputs_dir):
            os.makedirs(outputs_dir)
        with open(file_path, 'w') as md_file:
            md_file.write(markdown)
            
generate_markdown()