import pandas as pd

# Define the mapping from initial categories to Salesflare categories
mapping = {
    "Tailings Management": ["Tailings"],
    "Tailings management": ["Tailings"],
    "Indigenous and community relationships": [
        "Community relations and stakeholder engagement",
        "Experience with local communities"
    ],
    "Safe, healthy, and respectful workplaces": [
        "Occupational health and safety management systems"
    ],
    "Equitable, diverse, and inclusive workplaces": [
        "Labor, industrial relations and human resources management systems"
    ],
    "Prevention of child and forced labour": [
        "Social impact assessments and human rights due diligence"
    ],
    "Crisis management and communications planning": [
        "Community relations and stakeholder engagement"
    ],
    "Biodiversity conservation management": ["Environmental management systems"],
    "Water stewardship": ["Environmental management systems"],
    "Climate change": ["Environmental management systems", "Sustainability reporting"]
}

def map_expertise(expertise_str):
    """Map expertise categories to Salesflare categories, handling semicolon separation."""
    # Handle empty or NaN inputs
    if pd.isna(expertise_str) or not expertise_str.strip():
        return ""
    # Split by semicolon and strip whitespace, filtering out empty strings
    categories = [cat.strip() for cat in expertise_str.split(";") if cat.strip()]
    mapped_categories = []
    # Map each category to Salesflare categories
    for cat in categories:
        if cat in mapping:
            mapped_categories.extend(mapping[cat])
        else:
            print(f"Warning: Unknown category '{cat}' not mapped.")
    # Remove duplicates while preserving order
    seen = set()
    unique_mapped = [x for x in mapped_categories if not (x in seen or seen.add(x))]
    return "; ".join(unique_mapped)

# Read the CSV file
df = pd.read_csv("TSM_Assessor_Details.csv")

# Create the new Expertise_mapped column
df["Expertise_mapped"] = df["Expertise"].apply(map_expertise)

# Write the updated DataFrame back to the CSV file
df.to_csv("TSM_Assessor_Details.csv", index=False)

print("CSV file has been updated with the 'Expertise_mapped' column.")