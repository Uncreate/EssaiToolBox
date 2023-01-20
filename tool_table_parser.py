import os
import json
import re
from datetime import datetime, timedelta
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

tool_t_path = config['PATHS']['tool_t_path']
offsets_json = config['PATHS']['json_path']

# Now you can use the tool_t_path and json_path variables in your script

def read_and_parse_file(file_path):
    """
    Reads the content of a file and returns a list of dictionaries
    containing the data from each line.
    """
    data = []
    sixty_days_ago = datetime.now() - timedelta(days=30)
    with open(file_path) as f:
        lines = f.readlines()
        for line in lines[2:]:
            line_data = line.split()
            if len(line_data) > 1:
                name, dl, dr = line_data[0], float(line_data[5]), float(line_data[6])
                if match := re.search(r'\d{2}:\d{2}', line):
                    time = match.group()
                    if match := re.search(r'\d{4}\.\d{2}\.\d{2}', line):
                        date = datetime.strptime(match.group(), "%Y.%m.%d")
                        if date > sixty_days_ago and (abs(dl) != 0 or abs(dr) != 0):
                            timestamp = datetime.combine(date, datetime.strptime(time, "%H:%M").time())
                            data.append({"name": name, "DL": dl, "DR": dr, "Timestamp": timestamp})
                    elif match2 := re.search(r'\d{2}\.\d{2}\.\d{4}', line):
                        date = datetime.strptime(match2.group(), "%d.%m.%Y")
                        if date > sixty_days_ago and (abs(dl) != 0 or abs(dr) != 0):
                            timestamp = datetime.combine(date, datetime.strptime(time, "%H:%M").time())
                            data.append({"name": name, "DL": dl, "DR": dr, "Timestamp": timestamp})
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
    json_path = os.path.join(path, offsets_json)
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
                    json_data[machine_name][line['name']] = [{"DL": line['DL'], "DR": line['DR'], "Timestamp":line['Timestamp'].strftime("%Y-%m-%d %H:%M")}]
                else:
                    latest_dl = json_data[machine_name][line['name']][-1]['DL']
                    latest_dr = json_data[machine_name][line['name']][-1]['DR']
                    if latest_dl != line['DL'] or latest_dr != line['DR']:
                        json_data[machine_name][line['name']].append({"DL": line['DL'], "DR": line['DR'], "Timestamp":line['Timestamp'].strftime("%Y-%m-%d %H:%M")})
    write_json_file(json_data, json_path)




if __name__ == "__main__":
    # call the process_files function to start processing the files
    process_files(tool_t_path)