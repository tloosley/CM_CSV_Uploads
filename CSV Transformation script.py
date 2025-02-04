import pandas as pd

# Read the CSV file
df = pd.read_csv('Assessor list 2025 - partially approved.csv')

# Define the expertise columns that contain 'X'
expertise_columns = [
    'Environmental management systems',
    'Occupational health and safety management systems',
    'Labor, industrial relations, and human resources management systems',
    'Social impact assessments and human rights due diligence',
    'Community relations and stakeholder engagement;',
    'Compliance and ethics',
    'Mineral supply chain due diligence',
    'Sustainability reporting',
    'Experience with local communities'
]

# Function to extract expertises for a row
def extract_expertises(row):
    # Find columns with 'X' (case-insensitive)
    expertises = [col for col in expertise_columns if str(row[col]).strip().lower() == 'x']
    return '; '.join(expertises) if expertises else ''

# 1) Create a new column "Expertise" with extracted expertise from the X columns
df['Expertise'] = df.apply(extract_expertises, axis=1)

# 2) Drop the original expertise columns
df_cleaned = df.drop(columns=expertise_columns)

# 3) Rename the "Name" column to "Full name" (only if "Name" exists in your CSV)
df_cleaned.rename(columns={'Name': 'Full name'}, inplace=True)

# 4) Create a column "Stakeholder Type" set to "Assessor" for all rows
df_cleaned['Stakeholder Type'] = 'Assessor'

# 5) Create another column "Country of Residence"
#    You can leave it blank or populate it with existing data if available
df_cleaned['Country of Residence'] = ''

# 6) Save to a new CSV
df_cleaned.to_csv('assessor_details_v2.csv', index=False)

print("Process complete. Output saved to 'assessor_details.csv'")
