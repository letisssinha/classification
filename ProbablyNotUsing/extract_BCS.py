import os
import re
import pandas as pd
import PyPDF2
import nltk
from nltk.tokenize import sent_tokenize
from thefuzz import process

nltk.download('punkt')

# === CONFIGURATION ===
pdf_folder = '/Users/i553815/lerning/articles'
excel_path = '/Users/i553815/lerning/classification/citation_data/data_bcs_empty.xlsx'
output_excel = 'output_with_bcs_mentions.xlsx'

title_column = 'Title'           # Column with article titles
mention_column = 'mention BCS'   # Column to be marked with 'X'
mention_text_column = 'BCS mention'  # Column for matched sentences

# === REGEX PATTERN ===
pattern = re.compile(r'\b(?:balanced[-\s]?score\s?cards?|BSC|BCS)\b', re.IGNORECASE)

# === TEXT EXTRACTION FUNCTION ===
def extract_text_from_pdf(pdf_path):
    text = ''
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
    return text

def clean_excel_text(text):
    if not isinstance(text, str):
        return text
    # Removes non-printable ASCII characters: \x00 - \x1F and \x7F
    return re.sub(r'[\x00-\x1F\x7F]', ' ', text).strip()

# === PREPARE ===
pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]
df = pd.read_excel(excel_path)

# === MAIN LOOP ===
for index, row in df.iterrows():
    article_title = row[title_column]

    # Find the best PDF filename match using fuzzy matching
    best_match, score = process.extractOne(article_title, pdf_files)
    
    if score >= 80:  # confidence threshold (adjust if needed)
        pdf_path = os.path.join(pdf_folder, best_match)
        print(f"\n🔍 Matching: '{article_title}' → '{best_match}' (score: {score})")

        text = extract_text_from_pdf(pdf_path)
        sentences = sent_tokenize(text)
        matches = [s.strip() for s in sentences if pattern.search(s)]

        if matches:
            joined = ' | '.join(matches)
            cleaned = clean_excel_text(joined)
            df.at[index, mention_column] = 'X'
            df.at[index, mention_text_column] = cleaned
        else:
            df.at[index, mention_column] = ''
            df.at[index, mention_text_column] = ''

    else:
        print(f"❌ No good match for: {article_title} (best score: {score})")
        df.at[index, mention_column] = 'NO MATCH'
        df.at[index, mention_text_column] = ''

# === SAVE ===
df.to_excel(output_excel, index=False)
print(f"\n✅ Done! Results saved to: {output_excel}")