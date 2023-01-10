'''
Just a quick script to write TNCcmd files for downloading Tool.t Files from the controller - AR 1/23
'''
import configparser
import json

config = configparser.ConfigParser()
config.read('config.ini')
root_dir = config['PATHS']['tool_t_path']
machines_section = config['IP Adressess']
machines_json = machines_section['machines']
machines = json.loads(machines_json)

for machine in machines:
    name = machine["Name"]
    ip = machine["IP"]
    controller = machine["Controller"]

    with open(f".\\Data\\tnccmd\\{name}.tnccmd", "w") as f:
        f.write(f":{name}\n")
        f.write(f"ping {ip}\n")
        f.write(f"connect I {ip} -F\n")
        f.write(":FILE\n")
        if controller == "HEID_530":
          f.write(f"get TNC:\\Tool.t {root_dir}{name}-tool.t\n")
        else:
          f.write(f"get TNC:\\table\\Tool.t {root_dir}{name}-tool.t\n")
        f.write("sleep 900\n")
        f.write("on always goto FILE\n")