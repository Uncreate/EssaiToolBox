import os
import json
import re
from datetime import datetime, timedelta

def read_and_parse_file(file_path):
    """
    Reads the content of a file and returns a list of dictionaries
    containing the data from each line.
    """
    data = []
    sixty_days_ago = datetime.now() - timedelta(days=14)
    with open(file_path) as f:
        lines = f.readlines()
        for line in lines[2:]:
            line_data = line.split()
            if len(line_data) > 1:
                name, dl, dr = line_data[1], float(line_data[5]), float(line_data[6])
                if match := re.search(r'\d{4}\.\d{2}\.\d{2}', line):
                    date = datetime.strptime(match.group(), "%Y.%m.%d")
                    if date > sixty_days_ago and (
                        abs(dl) != 0 or abs(dr) != 0
                    ):
                        data.append({"name": name, "DL": dl, "DR": dr, "last_used": date})
    return data
def read_json_file(json_path):
    """
    Read the JSON file.
    """
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            json_data = json.load(f)
    else:
        json_data = {}
    return json_data

def write_json_file(json_data, json_path):
    """
    Write the JSON data to file.
    """
    with open(json_path, "w") as f:
        json.dump(json_data, f, indent=4)


def process_files(path):
    """
    Iterates through all the .t files in the specified directory,
    reads and parses their content, and updates the 'offsets.json' file.
    """
    json_path = os.path.join(path, 'offsets.json')
    json_data = read_json_file(json_path)

    for file in os.listdir(path):
        if file.endswith(".t"):
            file_path = os.path.join(path, file)
            data = read_and_parse_file(file_path)
            for line in data:
                machine_name = file[:5]
                if machine_name not in json_data:
                    json_data[machine_name] = {}
                if line['name'] not in json_data[machine_name]:
                    json_data[machine_name][line['name']] = {line['last_used'].strftime("%Y-%m-%d"): {"DL": line['DL'], "DR": line['DR']}}
                elif line['last_used'].strftime("%Y-%m-%d") not in json_data[machine_name][line['name']]:
                    json_data[machine_name][line['name']][line['last_used'].strftime("%Y-%m-%d")] = {"DL": line['DL'], "DR": line['DR']}
                elif json_data[machine_name][line['name']][line['last_used'].strftime("%Y-%m-%d")]['DL'] != line['DL'] or json_data[machine_name][line['name']][line['last_used'].strftime("%Y-%m-%d")]['DR'] != line['DR']:
                    json_data[machine_name][line['name']][line['last_used'].strftime("%Y-%m-%d")] = {"DL": line['DL'], "DR": line['DR']}
    write_json_file(json_data, json_path)

# call the process_files function to start processing the files
process_files('./Data/tooldott')