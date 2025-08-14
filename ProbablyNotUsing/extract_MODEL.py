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
excel_path = '/Users/i553815/lerning/classification/citation_data/output_with_bcs_mentions.xlsx'
output_excel = 'output_with_model_mentions.xlsx'

title_column = 'Title'                 # Column with article titles
model_column = 'model cited'          # Column to write model names
model_phrase_column = 'model citation'  # Column to write sentences

# === REGEX PATTERN FOR MODELS ===
MODEL_REGEX = re.compile(
    r"\b("
    r"self[- ]?assessment excellences?|"
    r"EFQMs?|"
    r"Cross and Lynch(?:es)?|"
    r"SMARTs?|"
    r"Performance Prisms?|"
    r"SCORs?|"
    r"Activity[- ]Based Costings?|"
    r"ABCs?|"
    r"Objectives? and Key Results?|"
    r"OKRs?|"
    r"360[- ]Degree Feedbacks?"
    r")\b",
    re.IGNORECASE
)

MODEL_NORMALIZATION = {
    "efqm": "EFQM",
    "self-assessment excellence": "Self-Assessment Excellence",
    "cross and lynch": "Cross and Lynch",
    "smart": "SMART",
    "performance prism": "Performance Prism",
    "scor": "SCOR",
    "activity-based costing": "Activity-Based Costing",
    "abc": "ABC",
    "objectives and key results": "OKR",
    "okr": "OKR",
    "360-degree feedback": "360-Degree Feedback"
}

def normalize_model(raw_match):
    raw = raw_match.lower().replace("–", "-").replace("—", "-")
    raw = re.sub(r'[-\s]+', ' ', raw).strip()
    for key, canonical in MODEL_NORMALIZATION.items():
        if key in raw:
            return canonical
    return raw_match

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
    return re.sub(r'[\x00-\x09\x0B-\x1F\x7F]', ' ', text).strip()

# === PREPARE ===
pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]
df = pd.read_excel(excel_path)

# === MAIN LOOP ===
for index, row in df.iterrows():
    article_title = row[title_column]
    best_match, score = process.extractOne(article_title, pdf_files)
    
    if score >= 80:
        pdf_path = os.path.join(pdf_folder, best_match)
        print(f"🔍 Matched: '{article_title}' → '{best_match}' (score: {score})")

        text = extract_text_from_pdf(pdf_path)
        sentences = sent_tokenize(text)

        model_matches = []
        model_sentences = []

        for sentence in sentences:
            matches = MODEL_REGEX.findall(sentence)
            if matches:
                model_sentences.append(sentence.strip())
                for m in matches:
                    norm = normalize_model(m)
                    model_matches.append(norm)

        unique_models = sorted(set(model_matches))

        if unique_models:
            df.at[index, model_column] = ', '.join(unique_models)
            df.at[index, model_phrase_column] = clean_excel_text('\n'.join(model_sentences))
        else:
            df.at[index, model_column] = ''
            df.at[index, model_phrase_column] = ''
    else:
        print(f"❌ No good match for: {article_title}")
        df.at[index, model_column] = 'NO MATCH'
        df.at[index, model_phrase_column] = ''

# === SAVE ===
df.to_excel(output_excel, index=False)
print(f"\n✅ Done! Results saved to: {output_excel}")
