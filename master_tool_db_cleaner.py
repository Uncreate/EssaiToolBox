import json
import sys
import tkinter as tk
from tkinter import filedialog


def select_file():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(
        filetypes=[("JSON files", "*.json"), ("Text", "*.txt")]
    )

def check_tools(file_path, output_file_path):
    with open(file_path, "r") as file:
        data = json.load(file)

    with open(output_file_path, "w") as output_file:
        count = 0
        for tool in data["tools"]:
            if tool["sc_tool_type"] == "milling":
                if tool["drilling_tool"]["Tool"] != 0.0:
                    output_file.write(tool["tool_name"] + " Mill Tool\n")
                    count += 1
            elif tool["milling_tool"]["Tool"] != 0.0:
                output_file.write(tool["tool_name"] + " Drill Tool\n")
                count += 1
        print(f"{count} tools were added to the output file.")

    # Ask user if they want to continue
    while True:
        answer = input("Do you want to continue? (Y/N) ").lower()
        if answer in ["y", "n"]:
            break
        else:
            print("Invalid input. Please enter Y or N.")
    if answer == "n":
        sys.exit()


def update_tools(file_path, output_file_path):
    with open(file_path, "r") as file:
        data = json.load(file)

    for tool in data["tools"]:
        if tool["sc_tool_type"] == "milling":
            if tool["drilling_tool"]["Tool"] != 0.0:
                tool["drilling_tool"] = {
                "Tool": 0.0,
                "TurretNum": 0.0,
                "Position": 0.0,
                "SubPosition": 0.0,
                "Permanent": 0.0,
                "IdNumber": "",
                "ToolType": "",
                "ToolUserType": "",
                "UnitsDiameter": "",
                "Diameter": 0.0,
                "Angle": 0.0,
                "Radius": 0.0,
                "NumTeeth": 0.0,
                "Description": "",
                "TaperAngle": 0.0,
                "ShankDiameter": 0.0,
                "UnitsLength": "",
                "Length": 0.0,
                "TotalLength": 0.0,
                "ShoulderLength": 0.0,
                "Startshoulderlength": 0.0,
                "TipLength": 0.0,
                "CuttingLength": 0.0,
                "HLengthManual": 0.0,
                "HLength": 0.0,
                "UnitsFeedSpin": "",
                "Ftype": "",
                "FeedXY": 0.0,
                "FeedZ": 0.0,
                "FeedFinishManual": 0.0,
                "FeedFinish": 0.0,
                "FeedLeadIn": 0.0,
                "FeedLeadOut": 0.0,
                "FeedLink": 0.0,
                "Stype": "",
                "Spin": 0.0,
                "SpinFinishManual": 0.0,
                "SpinFinish": 0.0,
                "FeedZPenetration": 0.0,
                "ToolName": "",
                "ToolGroupName": "",
                "HolderName": "",
                "GroupHolderName": "",
                "ChamferLength": 0.0,
                "TipDiameter": 0.0,
                "Message1": "",
                "Message2": "",
                "Message3": "",
                "Message4": "",
                "Message5": "",
                "FloodCoolant": 0.0,
                "AirBlastCoolant": 0.0,
                "Rough": 0.0,
                "SpinDirection": "",
                "Pitch": 0.0,
                "PitchUnit": ""
            }
        elif tool["milling_tool"]["Tool"] != 0.0:
                tool["milling_tool"] = {
                "Tool": 0.0,
                "TurretNum": 0.0,
                "Position": 0.0,
                "SubPosition": 0.0,
                "Permanent": 0.0,
                "IdNumber": "",
                "ToolType": "",
                "ToolUserType": "",
                "UnitsDiameter": "",
                "Diameter": 0.0,
                "Angle": 0.0,
                "Radius": 0.0,
                "ProfileRadius": 0.0,
                "NumTeeth": 0.0,
                "ShoulderDiameter": 0.0,
                "ShoulderAngle": 0.0,
                "Description": "",
                "TaperAngle": 0.0,
                "ShankDiameter": 0.0,
                "UnitsLength": "",
                "Length": 0.0,
                "TotalLength": 0.0,
                "ShoulderLength": 0.0,
                "Startshoulderlength": 0.0,
                "TipLength": 0.0,
                "CuttingLength": 0.0,
                "HLengthManual": 0.0,
                "HLength": 0.0,
                "imHelicalAngle": 0.0,
                "UnitsFeedSpin": "",
                "Ftype": "",
                "FeedXY": 0.0,
                "FeedZ": 0.0,
                "FeedFinishManual": 0.0,
                "FeedFinish": 0.0,
                "FeedLeadIn": 0.0,
                "FeedLeadOut": 0.0,
                "FeedLink": 0.0,
                "Stype": "",
                "Spin": 0.0,
                "SpinFinishManual": 0.0,
                "SpinFinish": 0.0,
                "FeedZPenetration": 0.0,
                "ToolName": "",
                "ToolGroupName": "",
                "HolderName": "",
                "GroupHolderName": "",
                "ChamferLength": 0.0,
                "TipDiameter": 0.0,
                "Message1": "",
                "Message2": "",
                "Message3": "",
                "Message4": "",
                "Message5": "",
                "FloodCoolant": 0.0,
                "AirBlastCoolant": 0.0,
                "Rough": 0.0,
                "SpinDirection": "",
                "ThreadingStandard": "",
                "NumThreads": 0.0,
                "ThreadStandardByUser": 0.0,
                "Pitch": 0.0
            }

    with open(output_file_path, "w") as output_file:
        json.dump(data, output_file, indent=4)

def check_tools_again(file_path, output_file_path):
    with open(file_path, "r") as file:
        data = json.load(file)

    with open(output_file_path, "w") as output_file:
        for tool in data["tools"]:
            if tool["sc_tool_type"] == "milling":
                if tool["drilling_tool"]["Tool"] != 0.0:
                    output_file.write(tool["tool_name"] + " Mill Tool\n")
            elif tool["milling_tool"]["Tool"] != 0.0:
                output_file.write(tool["tool_name"] + " Drill Tool\n")

if __name__ == "__main__":
    # Prompt the user to select the first JSON file
    file_path_1 = select_file()
    # Check the tools in the first file and write the results to a file
    output_file_path_1 = "output.txt"
    check_tools(file_path_1, output_file_path_1)

    # Prompt the user to select the second JSON file
    file_path_2 = file_path_1
    # Update the tools in the second file and save the updated data to a new file
    output_file_path_2 = "MasterToolDatabase_Clean.json"
    update_tools(file_path_2, output_file_path_2)

    # Prompt the user to select the third JSON file
    file_path_3 = output_file_path_2
    # Check the tools in the third file and write the results to a file
    output_file_path_3 = "corrected.txt"
    check_tools_again(file_path_3, output_file_path_3)
