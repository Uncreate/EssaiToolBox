import json

with open("C:\\EssaiControlPanel\\excel\\ToolDbEditorlog_ToolItems.json") as f:
    ToolItems = json.load(f)['ToolItems']

# Create a dictionary to store the result
result = {}

# Iterate through each item in the ToolItems list
for item in ToolItems:
    sEssaiPartNum = item['sEssaiPartNum']
    sToolName = item['sToolName']
    if sEssaiPartNum not in result:
        result[sEssaiPartNum] = {
            'sToolName': [sToolName],
            'min': 0,
            'max': 0,
            'qty_on_hand': 0,
            'crib_location': 0
        }
    else:
        result[sEssaiPartNum]['sToolName'].append(sToolName)
        result[sEssaiPartNum]['min'] = 0
        result[sEssaiPartNum]['max'] = 0
        result[sEssaiPartNum]['qty_on_hand'] = 0
        result[sEssaiPartNum]['crib_location'] = 0
# Write the result to a new JSON file
with open('C:\\Users\\adam.riggs\\Documents\\EssaiToolBox\\Data\\inventory.json', 'w') as f:
    json.dump(result, f)




import json

# Load the JSON file
with open('./Data/inventory.json', 'r') as f:
    inventory = json.load(f)

# Function to subtract 1 from qty_on_hand of a tool
def subtract_qty(tool_name):
    for item in inventory:
        if tool_name in inventory[item]['sToolName']:
            inventory[item]['qty_on_hand'] -= 1
            break

# Call the function when submit button is clicked
tool_name = # retrieve tool_name from UI input
subtract_qty(tool_name)

# Save the updated inventory
with open('./Data/inventory.json', 'w') as f:
    json.dump(inventory, f)
