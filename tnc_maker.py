'''
Just a quick script to write TNCcmd files for downloading Tool.t Files from the controller - AR 1/23
'''
machines =[{
      "location": "Phoenix",
      "Controller": "HEID_530",
      "Name": "HP-01",
      "IP": "192.168.201.203"
    },
    {
      "location": "Phoenix",
      "Controller": "HEID_530",
      "Name": "HP-02",
      "IP": "192.168.201.204"
    },
    {
      "location": "Phoenix",
      "Controller": "HEID_530",
      "Name": "HP-03",
      "IP": "192.168.201.202"
    },
    {
      "location": "Phoenix",
      "Controller": "HEID_530",
      "Name": "HP-04",
      "IP": "192.168.201.201"
    },
    {
      "location": "Phoenix",
      "Controller": "HEID_530",
      "Name": "HP-05",
      "IP": "192.168.202.203"
    },
    {
      "location": "Phoenix",
      "Controller": "HEID_530",
      "Name": "HP-06",
      "IP": "192.168.202.204"
    },
    {
      "location": "Phoenix",
      "Controller": "HEID_530",
      "Name": "Hp-07",
      "IP": "192.168.202.202"
    },
    {
      "location": "Phoenix",
      "Controller": "HEID_530",
      "Name": "HP-08",
      "IP": "192.168.202.201"
    },
    {
      "location": "Phoenix",
      "Controller": "HEID_640",
      "Name": "HP-09",
      "IP": "192.168.203.201"
    },
    {
      "location": "Phoenix",
      "Controller": "HEID_640",
      "Name": "HP-10",
      "IP": "192.168.203.202"
    },
    {
      "location": "Phoenix",
      "Controller": "HEID_640",
      "Name": "HP-11",
      "IP": "192.168.203.203"
    },
    {
      "location": "Phoenix",
      "Controller": "HEID_640",
      "Name": "HP-12",
      "IP": "192.168.203.204"
    },
    {
      "location": "Phoenix",
      "Controller": "HEID_640",
      "Name": "HP-13",
      "IP": "192.168.203.212"
    },
    {
      "location": "Phoenix",
      "Controller": "HEID_640",
      "Name": "HP-14",
      "IP": "192.168.203.211"
    },
    {
      "location": "Phoenix",
      "Controller": "HEID_640",
      "Name": "HP-15",
      "IP": "192.168.203.210"
    },
    {
      "location": "Phoenix",
      "Controller": "HEID_640",
      "Name": "HP-16",
      "IP": "192.168.203.213"
    },
    {
      "location": "Phoenix",
      "Controller": "HEID_640",
      "Name": "HP-17",
      "IP": "192.168.203.214"
    },
    {
      "location": "Phoenix",
      "Controller": "HEID_640",
      "Name": "HP-18",
      "IP": "192.168.203.215"
    },
    {
      "location": "Phoenix",
      "Controller": "HEID_640",
      "Name": "HP-19",
      "IP": "192.168.203.216"
    },
    {
      "location": "Phoenix",
      "Controller": "HEID_640",
      "Name": "HP-20",
      "IP": "192.168.203.217"
    },
    {
      "location": "Phoenix",
      "Controller": "HEID_640",
      "Name": "HP-21",
      "IP": "192.168.203.218"
    },
    {
      "location": "Phoenix",
      "Controller": "HEID_640",
      "Name": "HP-22",
      "IP": "192.168.203.219"
    },
    {
      "location": "Phoenix",
      "Controller": "HEID_640",
      "Name": "HP-23",
      "IP": "192.168.203.220"
    },
    {
      "location": "Phoenix",
      "Controller": "HEID_640",
      "Name": "HP-24",
      "IP": "192.168.203.221"
    },
    {
      "location": "Phoenix",
      "Controller": "HEID_640",
      "Name": "HP-25",
      "IP": "192.168.203.222"
    },
    {
      "location": "Phoenix",
      "Controller": "HEID_640",
      "Name": "HP-26",
      "IP": "192.168.71.92"
    }]

for machine in machines:
    name = machine["Name"]
    ip = machine["IP"]

    with open(f".\\Data\\tnccmd\\{name}.tnccmd", "w") as f:
        f.write(f":{name}\n")
        f.write(f"ping {ip}\n")
        f.write("on ERROR E20001406 GOTO HP-03\n")
        f.write(f"connect I {ip} -F\n")
        f.write(":FILE\n")
        f.write(f"get TNC:\\Tool.t C:\\Users\\adam.riggs\\Documents\\EssaiToolBox\\Data\\tooldott\\{name}\\tool.t\n")
        f.write("sleep 10\n")
        f.write("on always goto FILE\n")