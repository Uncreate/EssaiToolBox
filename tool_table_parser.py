import os
import re
import configparser
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

def extract_data(filename):
    """Extract the tool names, DR values, and DL values from the file, ignoring rows where both values are zero."""
    with open(filename, 'r') as f:
        lines = f.readlines()[2:]
    pattern = re.compile(r'^(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)')
    dr_names = []
    dl_names = []
    drs = []
    dls = []
    for line in lines:
        if match := pattern.match(line):
            name = match[1]
            dr = float(match[5])
            dl = float(match[6])
            if abs(dr) != 0:
                dr_names.append(name)
                drs.append(dr)
            elif abs(dl) != 0:
                dl_names.append(name)
                dls.append(dl)    
    return dr_names,dl_names, drs, dls

def plot_data(graph_storage, filename, dr_names, dl_names, drs, dls):
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
    plt.suptitle(filename)
    fig.savefig(os.path.join(graph_storage, f"{filename}.png"))

    
    plt.close()
def main():
    config = load_config()
    directory = get_directory(config)
    graph_storage = get_graph_storage(config)
    filenames = os.listdir(directory)
    for filename in filenames:
        full_path = os.path.join(directory, filename)
        dr_names, dl_names, drs, dls = extract_data(full_path)
        plot_data(graph_storage, filename, dr_names, dl_names, drs, dls)

if __name__ == '__main__':
    main()
