import pandas as pd

# Read the CSV files
df_assessors = pd.read_csv('TSM_Assessor_List_New.csv')
df_verifiers = pd.read_csv('TSM_Verifier_List_CSV.csv')

# Extract the 'Full Name' column from each file and remove any missing values
assessors_names = set(df_assessors['Full Name'].dropna().unique())
verifiers_names = set(df_verifiers['Full Name'].dropna().unique())

# Compute the three groups:
# 1. Names present in both files.
contacts_to_merge = sorted(list(assessors_names & verifiers_names))

# 2. Names in CM_TSM_Assessors_clean.csv but not in TSM_Verifier_List_CSV.csv.
not_fully_approved = sorted(list(assessors_names - verifiers_names))

# 3. Names in TSM_Verifier_List_CSV.csv but not in CM_TSM_Assessors_clean.csv.
to_chase_up = sorted(list(verifiers_names - assessors_names))

# Determine the maximum length among the lists so we can create a uniform DataFrame
max_length = max(len(contacts_to_merge), len(not_fully_approved), len(to_chase_up))

# Define a helper function to pad lists with empty strings to match the maximum length
def pad_list(name_list, length):
    return name_list + [''] * (length - len(name_list))

# Pad each list to the maximum length
contacts_to_merge = pad_list(contacts_to_merge, max_length)
not_fully_approved = pad_list(not_fully_approved, max_length)
to_chase_up = pad_list(to_chase_up, max_length)

# Create a DataFrame with the flagged columns
output_df = pd.DataFrame({
    'Contacts to merge': contacts_to_merge,
    'Not fully approved': not_fully_approved,
    'To chase up': to_chase_up
})

# Write the DataFrame to a CSV file
output_df.to_csv('Flagged Names_Mar25.csv', index=False)

print("Output written to 'Flagged Names_Mar25.csv'")
