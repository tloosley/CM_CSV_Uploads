import re
import csv
import unicodedata
import pandas as pd

def clean_language_name(lang):
    """Clean and standardize language names"""
    # Mapping of truncated/misspelled languages to correct names
    language_corrections = {
        'englis': 'English',
        'spanis': 'Spanish',
        'portugues': 'Portuguese',
        'japanes': 'Japanese',
        'frenc': 'French',
        'german': 'German',
        'italian': 'Italian',
        'romanain': 'Romanian',
    }
    
    # Normalize unicode characters
    lang = unicodedata.normalize('NFKD', lang).encode('ASCII', 'ignore').decode('ASCII')
    
    # Check for truncated language names first
    lang_lower = lang.lower().strip()
    for trunc, full in language_corrections.items():
        if trunc in lang_lower:
            return full
    
    # Standard language map
    language_map = {
        'english': 'English', 'spanish': 'Spanish', 'french': 'French', 
        'german': 'German', 'portuguese': 'Portuguese', 'italian': 'Italian', 
        'russian': 'Russian', 'chinese': 'Chinese', 'japanese': 'Japanese', 
        'turkish': 'Turkish', 'urdu': 'Urdu', 'serbian': 'Serbian',
        'bosnian': 'Bosnian', 'croatian': 'Croatian', 'farsi': 'Farsi', 
        'arabic': 'Arabic', 'romanian': 'Romanian', 'mongolian': 'Mongolian', 
        'indonesian': 'Indonesian', 'afrikaans': 'Afrikaans', 'hebrew': 'Hebrew', 
        'shona': 'Shona', 'thai': 'Thai', 'polish': 'Polish', 
        'swedish': 'Swedish', 'bahasa indonesia': 'Indonesian'
    }
    
    # Apply standard cleaning
    for key, value in language_map.items():
        if key in lang_lower:
            return value
    
    return lang.strip().capitalize()

def standardize_proficiency(prof):
    """Standardize proficiency levels"""
    prof = str(prof).lower().strip()
    
    if 'mother' in prof or 'native' in prof or 'mother tongue' in prof:
        return 'Mother Tongue'
    elif 'professional' in prof or 'fluent' in prof or 'c2' in prof or 'business' in prof:
        return 'Professional'
    elif 'intermediate' in prof or 'middle' in prof:
        return 'Intermediate'
    elif 'elementary' in prof or 'basic' in prof or 'average' in prof:
        return 'Elementary'
    return None

def parse_language_entry(entry):
    """Parse a single language entry"""
    entry = str(entry).strip('"').strip()
    
    parts = re.split(r',|-', entry)
    
    mother_tongue = None
    other_languages = []
    
    for part in parts:
        part = part.strip()
        
        if not mother_tongue:
            for indicator in ['mother tongue', 'native', 'mother language']:
                if indicator in part.lower():
                    lang = re.sub(r'\(.*?\)', '', part, flags=re.IGNORECASE).strip()
                    mother_tongue = clean_language_name(lang.replace(indicator, '').strip())
                    break
        
        match = re.match(r'(\w+)\s*(?:\(.*?\))?\s*-?\s*([a-zA-Z\s]+)?', part, re.IGNORECASE)
        if match:
            lang = clean_language_name(match.group(1))
            prof = standardize_proficiency(match.group(2) or '')
            
            if lang:
                if not mother_tongue:
                    mother_tongue = lang
                
                if prof:
                    other_languages.append(f"{lang} - {prof}")
                elif lang != mother_tongue:
                    other_languages.append(lang)
    
    return mother_tongue, ', '.join(other_languages) if other_languages else None

def process_language_data(input_file):
    """Process language data from CSV"""
    df = pd.read_csv(input_file)
    
    results = []
    for column in df.columns:
        for entry in df[column].dropna():
            mother_tongue, other_languages = parse_language_entry(entry)
            if mother_tongue:
                results.append({
                    'Language Mother Tongue': mother_tongue,
                    'Other Languages': other_languages or ''
                })
    
    return results

def save_to_csv(data, filename='cleaned_language_data_claude.csv'):
    """Save processed data to CSV"""
    if not data:
        print("No data to save.")
        return
    
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
    
    print(f"Data saved to {filename}")

# Process the data
processed_data = process_language_data('assessor_languages.csv')

# Save to CSV
save_to_csv(processed_data)