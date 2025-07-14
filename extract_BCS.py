import os
import re
import PyPDF2
import nltk
from nltk.tokenize import sent_tokenize

nltk.download('punkt')  # Download tokenizer data

pattern = re.compile(r'\b(?:balanced[-\s]?score\s?cards?|BSC|BCS)\b', re.IGNORECASE)
folder_path = '/Users/i553815/lerning/articles'
output_file = '/output_BCS/balanced_scorecard_matches.txt'

# Helper: extract text from a PDF
def extract_text_from_pdf(pdf_path):
    text = ''
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ''
    return text

# Loop through PDF files
def proccess_results():
    results = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            print(f"Processing: {filename}")
            
            text = extract_text_from_pdf(pdf_path)
            sentences = sent_tokenize(text)
            
            matches = [sent.strip() for sent in sentences if pattern.search(sent)]
            
            if matches:
                results.append(f"\n=== {filename} ===\n" + '\n'.join(matches))

    # Write results to file
    with open(output_file, 'w', encoding='utf-8') as f:
        if results:
            f.write('\n\n'.join(results))
            print(f"\n✅ Matches written to {output_file}")
        else:
            f.write("No matches found.")
            print("\n❌ No matches found in any file.")

proccess_results()