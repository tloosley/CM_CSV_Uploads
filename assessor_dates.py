import pandas as pd
from datetime import datetime

# Read the CSV file (assumes the CSV has a header; if not, use header=None)
df = pd.read_csv('assessor_dates.csv')

# Get the name of the only column
date_column = df.columns[0]

def convert_date(date_str):
    """
    Convert a date from 'DD-MMM-YY' (e.g., '29-SEP-21') to 'YYYY-MM-DD'
    (e.g., '2021-09-29'). If the cell is blank, return an empty string.
    """
    # Check if the cell is blank or NaN.
    if pd.isna(date_str) or str(date_str).strip() == '':
        return ''  # Leave the cell blank.
    
    # Parse the original date string.
    date_obj = datetime.strptime(date_str, '%d-%b-%y')
    
    # Format the date to 'YYYY-MM-DD'
    return date_obj.strftime('%Y-%m-%d')

# Apply the conversion to the entire column.
df[date_column] = df[date_column].apply(convert_date)

# Write the updated DataFrame back to the same CSV file.
df.to_csv('assessor_dates.csv', index=False, na_rep='')
