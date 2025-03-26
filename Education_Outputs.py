import pandas as pd

# Read the CSV files
try:
    tsm_assessors = pd.read_csv('TSM_Assessor_Details.csv')
    all_assessors = pd.read_csv('All_Assessors_JF.csv')
except FileNotFoundError as e:
    print(f"Error: Could not find one of the input files - {e}")
    exit()

# Create a list to store results while maintaining original order
results = []

# Counter for statistics
missing_count = 0
no_education_count = 0

# Process each assessor in original order
for index, row in tsm_assessors.iterrows():
    name = row['Full Name']
    
    # Find matching row in All_Assessors_JF.csv
    matching_row = all_assessors[all_assessors['Full Name'] == name]
    
    if matching_row.empty:
        print(f"Assessor not found in All_Assessors_JF.csv: {name}")
        results.append({'Full Name': name, 'Education': 'Not Found'})
        missing_count += 1
    else:
        education = matching_row['Education'].iloc[0]
        if pd.isna(education) or str(education).strip() == "":
            print(f"No education information found for assessor: {name}")
            results.append({'Full Name': name, 'Education': 'Not Available'})
            no_education_count += 1
        else:
            results.append({'Full Name': name, 'Education': education})

# Create DataFrame from results and save to CSV
output_df = pd.DataFrame(results)
output_df.to_csv('All_Assessors_Education.csv', index=False)

# Print summary
total_assessors = len(tsm_assessors)
print(f"\nProcessing complete:")
print(f"Total assessors processed: {total_assessors}")
print(f"Assessors with education info: {total_assessors - missing_count - no_education_count}")
print(f"Assessors not found: {missing_count}")
print(f"Assessors with no education info: {no_education_count}")
print("Output saved to All_Assessors_Education.csv")