import pandas as pd
import json

# Read the Excel file
excel_file = pd.ExcelFile(
    "C:\\Users\\adam.riggs\\Downloads\\R14-999-TOOLS.XLS")

# Load the "Milling" and "Drilling" sheets into dataframes
milling_df = pd.read_excel(excel_file, sheet_name='Milling', na_filter=False)
drilling_df = pd.read_excel(excel_file, sheet_name='Drilling', na_filter=False)

# Load the JSON file
with open("C:\\Users\\adam.riggs\\OneDrive - Advantest\\EssaiControlPanel\\MasterToolDatabase.txt") as f:
    data = json.load(f)

# Find matching tools in the milling sheet
matching_milling_tools = []
for index, row in milling_df.iterrows():
    tool = row['Tool']
    message2 = row['Message2']
    if message2 != '':
        matching_milling_tools.extend(
            (tool, message2, tool_data['tool_name'],tool_data['milling_tool']['HolderName'])
            for tool_data in data['tools']
            if tool_data['milling_tool']['Message2'] == message2
        )
        if not matching_milling_tools:
            matching_milling_tools.append((tool, message2, 'No match'))
    else:
        matching_milling_tools.append((tool, message2, 'No match'))

# Find matching tools in the drilling sheet
matching_drilling_tools = []
for index, row in drilling_df.iterrows():
    tool = row['Tool']
    message2 = row['Message2']
    if message2 != '':
        matching_drilling_tools.extend(
            (tool, message2, tool_data['tool_name'],tool_data['drilling_tool']['HolderName'])
            for tool_data in data['tools']
            if tool_data['drilling_tool']['Message2'] == message2
        )
        if not matching_drilling_tools:
            matching_drilling_tools.append((tool, message2, 'No match'))
    else:
        matching_drilling_tools.append((tool, message2, 'No match'))

# Combine the matching milling and drilling tools into a single dataframe
df = pd.DataFrame(matching_milling_tools + matching_drilling_tools, columns=[
                  'Legacy Tool', 'Essai Part Number', 'New Tool Name', 'Holder'])

# Write the dataframe to a CSV file
df.to_csv('matching_tools.csv', index=False)

# Print a message indicating success
print('Matching tools written to matching_tools.csv')
