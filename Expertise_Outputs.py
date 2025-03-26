# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 12:14:41 2025

@author: tomlo
"""

import pandas as pd

# Read the CSV files
try:
    tsm_assessors = pd.read_csv('TSM_Assessor_Details.csv')
    all_assessors = pd.read_csv('All_Assessors_JF.csv')
except FileNotFoundError as e:
    print(f"Error: Could not find one of the input files - {e}")
    exit()

# Define the expertise columns we're interested in
expertise_cols = {
    '1. Environmental': '1. Environmental',
    '2. Social': '2. Social',
    '4. Supply Chain Due Diligence': '4. Supply Chain Due Diligence'
}

# Initialize counters
stats = {
    '1. Environmental': {'YES': 0, 'NO': 0},
    '2. Social': {'YES': 0, 'NO': 0},
    '4. Supply Chain Due Diligence': {'YES': 0, 'NO': 0}
}
not_yes_assessors = set()

# Create results list
results = []

# Process each assessor in original order
for index, row in tsm_assessors.iterrows():
    name = row['Full Name']
    matching_row = all_assessors[all_assessors['Full Name'] == name]
    
    if matching_row.empty:
        print(f"Assessor not found in All_Assessors_JF.csv: {name}")
        results.append({'Full Name': name, 'Expertise': 'Not Found'})
        continue
    
    # Get expertise for this assessor
    assessor_expertise = []
    assessor_row = matching_row.iloc[0]
    has_no_expertise = True
    
    for col in expertise_cols:
        value = str(assessor_row[col]).strip().upper() if not pd.isna(assessor_row[col]) else 'NO'
        
        if value in ['YES', 'SI']:
            assessor_expertise.append(col)
            stats[col]['YES'] += 1
            has_no_expertise = False
        else:
            stats[col]['NO'] += 1
            if value not in ['NO', '']:
                print(f"Non-standard value '{value}' found for {name} in {col}")
        
        if has_no_expertise:
            not_yes_assessors.add(name)
    
    # Format expertise output
    expertise_output = '\n'.join(assessor_expertise) if assessor_expertise else 'None'
    results.append({'Full Name': name, 'Expertise': expertise_output})

# Create DataFrame and save to CSV
output_df = pd.DataFrame(results)
output_df.to_csv('All_Assessors_Expertise.csv', index=False)

# Print detailed summary
print("\nProcessing complete:")
print(f"Total assessors processed: {len(tsm_assessors)}")
print(f"Assessors not found: {sum(1 for r in results if r['Expertise'] == 'Not Found')}")
print("\nExpertise Statistics:")
for col in expertise_cols:
    print(f"{col}:")
    print(f"  YES: {stats[col]['YES']}")
    print(f"  NO/Blank/Other: {stats[col]['NO']}")
print(f"\nAssessors with no expertise (all NO/blank): {len(not_yes_assessors)}")
if not_yes_assessors:
    print("Assessors with no expertise:")
    for name in sorted(not_yes_assessors):
        print(f"  {name}")
print("\nOutput saved to All_Assessors_Expertise.csv")