import pdfplumber
import pandas as pd
import re


pdf_path = "student.pdf"
records = []

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        lines = page.extract_text().split('\n')
        i = 0
        while i < len(lines) - 1:
            line = lines[i].strip()

            match = re.match(r'^(F\d{3})\s+(.*)', line)
            if match:
                roll = match.group(1)
                name = match.group(2).strip()
                
                next_line = lines[i + 1].strip()
                marks = re.findall(r'\b(AB|\d{1,2})\b', next_line)

                if len(marks) == 5:
                    records.append([roll, name] + marks)
                    i += 1 
            i += 1

df = pd.DataFrame(records, columns=["Roll No", "Name", "EM-II", "PPS", "CHEM", "EG", "BXE"])

df.to_csv("students_exact.csv", index=False)
print("✅ CSV created: students_exact.csv with", len(df), "rows")
