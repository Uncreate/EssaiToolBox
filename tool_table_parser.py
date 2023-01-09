import configparser
import datetime
import os
import re

import matplotlib.pyplot as plt


def load_config():
    """Load the configuration file."""
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config

def extract_data(filename):
    """Extract the tool names, DR values, DL values, and Last_used dates from the file, ignoring rows where both DR and DL values are zero and tools that have not been used in the last six months."""
    with open(filename, 'r') as f:
        lines = f.readlines()[2:]
    pattern = re.compile(r'^(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)')
    dr_names = []
    dl_names = []
    drs = []
    dls = []
    last_used_dates = []
    for line in lines:
        if match := pattern.match(line):
            name = match[1]
            dr = float(match[5])
            dl = float(match[6])
            last_used = datetime.datetime.strptime(match[22], '%Y.%m.%d %H:%M')
            now = datetime.datetime.now()
            diff = now - last_used
            if abs(dr) != 0 and diff.days < 180:
                dr_names.append(name)
                drs.append(dr)
                
            elif abs(dl) != 0 and diff.days < 180:
                dl_names.append(name)
                dls.append(dl)
                
    return dr_names, dl_names, drs, dls

def process_files(config):
    # Get the directory to search
    base_dir = config['PATHS']['tool_t_path']
    # Get the storage location for the graphs
    graph_storage = config['PATHS']['graph_storage']

    # Search for T files in the subdirectories of base_dir
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.T'):
                full_path = os.path.join(root, file)
                print(full_path)
                dr_names, dl_names, drs, dls = extract_data(full_path)
                plot_data(graph_storage, file, dr_names, dl_names, drs, dls)

def plot_data(graph_storage, file, dr_names, dl_names, drs, dls):
    # sourcery skip: extract-duplicate-method
    # Create a figure and axis
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 9), layout='constrained')

    # Plot the DR values
    ax1.bar(dr_names, drs)
    ax1.set_xlabel("Tool")
    ax1.set_ylabel("DR")
    for i, v in enumerate(drs):
        ax1.text(i, v, f"{v:.4f}", ha="center", va="bottom", rotation= 90)

    # Plot the DL values
    ax2.bar(dl_names, dls)
    ax2.set_xlabel("Tool")
    ax2.set_ylabel("DL")
    for i, v in enumerate(dls):
        ax2.text(i, v, f"{v:.4f}", ha="center", va="bottom", rotation= 90)

    # Tighten layout and show plot
    plt.xticks(rotation = 45)
    plt.suptitle(file)
    fig.savefig(os.path.join(graph_storage, f"{file}.png"))

    
    plt.close()
def main():
    config = load_config()
    process_files(config)

if __name__ == '__main__':
    main()
