import sqlite3
import datetime
import json
import pandas as pd
import logging
import os

# Get today's date
today = datetime.date.today()

# Define file paths
db_path = os.path.abspath("A:\Data\orders.db")
json_path = os.path.abspath('A:\EssaiControlPanel\excel\ToolDbEditorlog_ToolItems.json')
log_path = os.path.abspath('A:\Data\inventory_reporting_log.log')
excel_path = os.path.abspath('A:\Data\inventory_reporting.xlsx')

# Configure logging
logging.basicConfig(filename=log_path, level=logging.ERROR,
                    format='%(asctime)s %(levelname)s: %(message)s')

# Load tool data from JSON file
try:
    with open(json_path) as f:
        tool_data = json.load(f)['ToolItems']
except FileNotFoundError:
    logging.error(f"File not found: {json_path}")
    raise
except json.JSONDecodeError:
    logging.error(f"Invalid JSON file: {json_path}")
    raise

try:
    # Connect to database and retrieve order details
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute("SELECT DISTINCT date(time) FROM orders")
        dates = c.fetchall()
        grouped_data = []
        for date in dates:
            # Skip over None values
            if date[0] is None:
                continue
            date_obj = datetime.datetime.strptime(date[0], '%Y-%m-%d').date() # Convert string to date object
            c.execute("SELECT rowid FROM orders WHERE date(time)=? AND complete=?", (date[0],1))
            rows = c.fetchall()
            for row in rows:
                order_id = row[0]
                c.execute("SELECT * FROM order_detail WHERE order_id=?", (order_id,))
                order_details = c.fetchall()
                for detail in order_details:
                    tool_name = detail[1] # Assuming the tool name is in the second column
                    # Look up Essai part number for tool name
                    if tool_item := next(
                        (
                            item
                            for item in tool_data
                            if item['sToolName'] == tool_name
                        ),
                        None,
                    ):
                        essai_part_num = tool_item['sEssaiPartNum']
                        # Add order detail to list
                        grouped_data.append((date_obj, tool_name, essai_part_num, detail[2]))
                    else:
                        # Log warning if tool name not found in JSON file
                        logging.warning(f"No matching tool item found for tool name: {tool_name}")
        # Create DataFrame from order details and group by date
        df = pd.DataFrame(grouped_data, columns=['Date', 'Tool Name', 'Essai Part Number', 'Quantity'])
        grouped = df.groupby('Date')
        # Export order details to Excel file
        with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
            for name, group in grouped:
                sheet_name = name.strftime('%Y-%m-%d')
                group.to_excel(writer, sheet_name=sheet_name, index=False)
except FileNotFoundError:
    # Log error if database file not found
    logging.error(f"File not found: {db_path}")
    raise
except Exception as e:
    # Log error if exception occurs
    logging.error(f"An error occurred while fetching order details: {e}")
    raise
else:
    # Log success message if order details exported to Excel file
    logging.info(f"Order details exported to file: {excel_path}")
