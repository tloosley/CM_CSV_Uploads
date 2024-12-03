import pandas as pd
import csv
from datetime import datetime
import os
import chardet

def read_csv(file_path):
    try:
        with open(file_path, 'rb') as file:
            raw_data = file.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']

        df = pd.read_csv(file_path, encoding=encoding)
        print(f"Successfully read the file with {encoding} encoding")
        return df
    except Exception as e:
        print(f"Error reading CSV file: {str(e)}")
        return None

def is_valid_date(date_string):
    if pd.isna(date_string):
        return False
    try:
        datetime.strptime(str(date_string), '%Y-%m-%d')
        return True
    except ValueError:
        return False

def parse_date(date_string):
    if pd.isna(date_string):
        return ''
    try:
        for fmt in ('%d-%b-%Y', '%d-%b-%y', '%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y'):
            try:
                return datetime.strptime(date_string, fmt).strftime('%Y-%m-%d')
            except ValueError:
                continue
        return ''  # Return empty string if date parsing fails
    except:
        return ''  # Return empty string for any other errors

def extract_project_data(df, project_id):
    projects = df[df["Unique Copper Mark number"] == project_id]
    if projects.empty:
        print(f"No project found with ID {project_id}")
        return []
    
    results = []
    for _, project in projects.iterrows():
        data = {}
        for col in df.columns:
            value = project[col]
            if pd.notna(value):
                parsed_date = parse_date(value)
                if parsed_date:
                    data[col] = parsed_date
                else:
                    data[col] = str(value)
            else:
                data[col] = ''
        
        site_name = project.get("Site Name", "Unknown Site")
        parent_company = project.get("Parent Company (if Applicable)", "Unknown Parent")
        results.append((data, site_name, parent_company))
    
    return results

def determine_date_category(task_name):
    received_tasks = [
        'DD Checklist Reviewed',
        'Completed Self-Assessment Received',
        'Assessment plan received',
        'Assessment start date',
        'Assessment end date',
        'Assessment report received',
        'Improvement Plan received',
        'Follow up assessment date',
        'Follow up assessment report received'
    ]
    
    if task_name in received_tasks:
        return 'Date received'
    
    due_keywords = ['due', 'assessment', 'plan', 'declaration']
    received_keywords = ['received', 'completed', 'issued', 'approved', 'start', 'end', 'date']
    
    task_lower = task_name.lower()
    if any(keyword in task_lower for keyword in due_keywords):
        return 'Due date'
    elif any(keyword in task_lower for keyword in received_keywords):
        return 'Date received'
    else:
        return 'Due date'  # Default to 'Due date' if unsure

def get_additional_tasks():
    return [
        ("Stage 1 - Commitment", "Fully Aligned Due", "Application Received", "Notes", "X"),
        ("Stage 2 - Self-assessment", "Completed Self-Assessment Received", "Self Assessment Notes", "Notes", "AA"),
        ("Stage 2 - Self-assessment", "Self Assessment Notes", "Selection of Assessor", "Assessment Firm (if applicable)", "AC"),
        ("Stage 3 - Site Assessment", "Assessment end date", "Number of Days On-Site", "Number of Days On-Site", "AK"),
        ("Stage 3 - Site Assessment", "Determination Issued", "Determination Issued & Final Decision", "Determination", "AQ"),
        ("Stage 3 - Site Assessment", "Determination", "Final Summary Report Received", "Notes", "AS"),
        ("Stage 4 - Improvement Plan", "Improvement Plan received", "1. Site Feedback", "Feedback 1", "AW"),
        ("Stage 4 - Improvement Plan", "1. Site Feedback", "2. Site Feedback", "Feedback 2", "AY"),
        ("Stage 4 - Improvement Plan", "2. Site Feedback", "3. Site Feedback", "Feedback 3", "BA"),
        ("Stage 4 - Improvement Plan", "3. Site Feedback", "4. Site Feedback", "Feedback 4", "BC"),
        ("Stage 4 - Improvement Plan", "Notification of Assessment Report received", "Determination Issued and Decision", "Determination", "BJ"),
        ("Stage 4 - Improvement Plan", "Determination Issued and Decision", "Improvement Plan", "Notes", "BK"),
        ("Stage 5 - Re-assessment", "Annual Declaration 1", "Annual Declaration 2", "Notes", "BP"),
        ("Stage 5 - Re-assessment", "Annual Declaration 2", "Re-assessment to be initiated", "Re-assessment triggered", "BQ"),
        ("Stage 5 - Re-assessment", "Expiry Date", "Re-Assessment Due", "Notes", "BV"),
    ]

def save_to_csv(data, output_file):
    try:
        with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["Name", "Due date", "Date received & completed", "Notes", "Parent task"])
            
            stages = {
                "Stage 1 - Commitment": ["Application Received", "Completed Letter of Commitment", "DD Checklist Reviewed", "DD Checklist Approved", "Assessment Due", "Fully Aligned Due"],
                "Stage 2 - Self-assessment": ["Self-Assessment Due Date", "Completed Self-Assessment Received"],
                "Stage 3 - Site Assessment": ["Assessment plan received", "Scoping Call date", "Assessment due date", "Assessment start date", "Assessment end date", "Assessment report received", "request for clarification sent to Assessor", "Notification of final report received", "Determination due", "Determination issued"],
                "Stage 4 - Improvement Plan": ["Improvement Plan due", "Improvement Plan received", "Check in 1 date", "Check in 2 date", "Check in 3 date", "Check in 4 date", "Follow up Assessment Due", "Follow up assessment date", "Follow up assessment report received", "Notification of assessment report received"],
                "Stage 5 - Re-assessment": ["Next Assessment due", "Annual Declaration 1", "Annual Declaration 2", "Award Date", "Expiry Date"]
            }
            
            additional_tasks = get_additional_tasks()
            
            for stage, columns in stages.items():
                writer.writerow([stage, "", "", "", ""])
                stage_notes = []

                for col in columns:
                    if col in data:
                        category = determine_date_category(col)
                        date_value = data[col]
                        note = data.get(f"{col} Notes", "").strip()
                        
                        if is_valid_date(date_value):
                            if category == 'Due date':
                                writer.writerow([col, date_value, "", note, stage])
                            else:
                                writer.writerow([col, "", date_value, note, stage])
                        else:
                            # If the date is invalid, move it to notes
                            combined_note = f"{date_value} {note}".strip()
                            writer.writerow([col, "", "", combined_note, stage])
                        
                        # Collect additional notes for this task
                        if note:
                            stage_notes.append((col, note))
                
                # Add additional tasks and notes
                for task in additional_tasks:
                    if task[0] == stage:
                        if task[2] == "Number of Days On-Site":
                            writer.writerow([task[2], "", "", data.get(task[3], ""), stage])
                        else:
                            notes = data.get(task[3], '').strip()
                            if notes:
                                stage_notes.append((task[2], notes))
                
                # Write collected notes
                for task, note in stage_notes:
                    writer.writerow([f"{task} Notes", "", "", note, stage])
                
                # Add a general notes line for the stage if there are any notes not associated with specific tasks
                general_notes = data.get(f"{stage} Notes", "").strip()
                if general_notes:
                    writer.writerow([f"{stage} Notes", "", "", general_notes, stage])
        
        print(f"Data saved to {output_file}")
        
        # Verify the encoding and presence of the "Date received & completed" column
        with open(output_file, 'rb') as file:
            raw_data = file.read()
            result = chardet.detect(raw_data)
            detected_encoding = result['encoding']
        
        df = pd.read_csv(output_file, encoding=detected_encoding)
        if "Date received & completed" not in df.columns:
            print(f"Warning: 'Date received & completed' column is missing in {output_file}")
        
        print(f"File saved with detected encoding: {detected_encoding}")
        
    except Exception as e:
        print(f"Error saving CSV file {output_file}: {str(e)}")

def create_filename(project_id, site_name, parent_company, duplicate_count):
    site_name = site_name if pd.notna(site_name) else 'None'
    parent_company = parent_company if pd.notna(parent_company) else 'None'
    
    filename = f"{project_id}_{site_name}_{parent_company}"
    if duplicate_count > 0:
        filename += f"_({duplicate_count + 1})"
    filename = "".join(c if c.isalnum() or c in (' ', '_', '-') else '_' for c in filename).rstrip()
    filename = filename.replace(' ', '_')
    return f"{filename}.csv"

def process_batch(df, start_id, end_id, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for i in range(start_id, end_id + 1):
        project_id = f"P{i:04d}"
        results = extract_project_data(df, project_id)
        if results:
            for idx, (project_data, site_name, parent_company) in enumerate(results):
                output_file = os.path.join(output_dir, create_filename(project_id, site_name, parent_company, idx))
                save_to_csv(project_data, output_file)
                print(f"Data for project {project_id}{' (reassessment)' if idx > 0 else ''} extracted and saved to {output_file}")
        else:
            print(f"No data extracted for project {project_id}")

def main():
    file_path = r"C:\Users\tomlo\OneDrive\Documents\Personal\Work\The Copper Mark\Participants CSV- APM.csv"
    output_dir = r"C:\Users\tomlo\OneDrive\Documents\Personal\Work\The Copper Mark\Extracted_1007"
    
    start_id = 1
    end_id = 117
    
    df = read_csv(file_path)
    if df is not None:
        process_batch(df, start_id, end_id, output_dir)
        print(f"Batch processing completed for projects P{start_id:04d} to P{end_id:04d}")
    else:
        print("Failed to read the CSV file. Please check the file path and try again.")

if __name__ == "__main__":
    main()