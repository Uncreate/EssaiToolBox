import configparser
import os
import re
from datetime import datetime, timedelta
import json
import matplotlib.pyplot as plt


def load_config():
    """Load the configuration file."""
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config

def get_directory(config):
    """Get the directory to search from the configuration file."""
    return config['PATHS']['tool_t_path']

def get_graph_storage(config):
    return config['PATHS']['graph_storage']

def plotOffsets(filename):
    data = extract_data(filename)
    create_figure(data)
    plt.show()


def extract_data(filename):
    lines = read_file(filename)
    threshold_date = get_threshold_date()
    data = extract_values(lines, threshold_date)
    directory = os.path.dirname(filename)
    json_path = os.path.join(directory, 'data.json')
    if not os.path.exists(json_path):
        open(json_path, "x").close()
    with open(json_path, "r+") as f:
        f.seek(0, 2)
        if f.tell() > 0:
            f.write(',')
        json.dump(data, f)
    return data


def read_file(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
    return lines

def get_threshold_date():
    current_date = datetime.now().date()
    return current_date - timedelta(days=60)

def extract_values(lines, threshold_date):
    data = {"DR": [], "DL": []}

    for line in lines[2:]:
        date_obj = get_date_object(line)
        if date_obj and date_obj > threshold_date:
            line_data = line.split()
            name, dl, dr = line_data[1], float(line_data[5]), float(line_data[6])
            if abs(dr) != 0:
                data["DR"].append({"name": name, "value": dr})
            elif abs(dl) != 0:
                data["DL"].append({"name": name, "value": dl}) 
    return data

def get_date_object(line):
    if date_str := get_date_string(line):
        if re.search(r"\d{2}\.\d{2}\.\d{4}", date_str):
            return datetime.strptime(date_str, '%d.%m.%Y').date()
        elif re.search(r"\d{4}\.\d{2}\.\d{2}", date_str):
            return datetime.strptime(date_str, '%Y.%m.%d').date()
    return None

def get_date_string(line):
    match1 = re.search(r"\d{2}\.\d{2}\.\d{4}", line)
    match2 = re.search(r"\d{4}\.\d{2}\.\d{2}", line)
    if match1:
        return match1.group()
    elif match2:
        return match2.group()
    return None



def create_figure(data):
    # Create a figure with 2 subplots (1 row, 2 columns)
    fig, axs = plt.subplots(1, 2, figsize=(20, 7))

    # Plotting DR values on the first subplot
    dr_names = [d["name"] for d in data["DR"]]
    dr_values = [d["value"] for d in data["DR"]]
    axs[0].set_xticklabels(dr_names, rotation=45, ha="right")
    axs[0].bar(dr_names, dr_values)
    axs[0].set_xlabel('Name')
    axs[0].set_ylabel('DR')
    axs[0].set_title('DR values for the last 60 days')
    for i, v in enumerate(dr_values):
        axs[0].text(i - 0.5, v, str(v), color='black')

    # Plotting DL values on the second subplot
    dl_names = [d["name"] for d in data["DL"]]
    dl_values = [d["value"] for d in data["DL"]]
    axs[1].set_xticklabels(dl_names, rotation=45, ha="right")
    axs[1].bar(dl_names, dl_values)
    axs[1].set_xlabel('Name')
    axs[1].set_ylabel('DL')
    axs[1].set_title('DL values for the last 60 days')
    for i, v in enumerate(dl_values):
        axs[1].text(i - 0.5, v, str(v), color='black')

    plt.tight_layout()


def main():
    config = load_config()
    directory = get_directory(config)
    graph_storage = get_graph_storage(config)
    filenames = os.listdir(directory)
    number_of_days = timedelta(days=90)
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".t"):
                full_path = os.path.join(root, file)
                plotOffsets(full_path)


if __name__ == '__main__':
    main()