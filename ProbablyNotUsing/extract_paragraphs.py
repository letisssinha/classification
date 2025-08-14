import fitz  # PyMuPDF
import os
import re

indicator_patterns = [
    r"\bperformance indicators?\b",
    r"\bperformance measures?\b",
    r"\bmeasure[s]? of performance\b",
    r"\bperformance metrics?\b",
    r"\bmetrics? of performance\b",
    r"\bKPIs?\b",
    r"\bkey performance indicators?\b",
    r"\bindicators? of performance\b"
]

pattern_regex = re.compile("|".join(indicator_patterns), re.IGNORECASE)

def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        print(f"Erro ao ler {pdf_path}: {e}")
        return ""

def extract_paragraphs_with_indicators(text):
    paragraphs = text.split("\n\n")
    filtered_paragraphs = [p.strip() for p in paragraphs if pattern_regex.search(p)]
    return filtered_paragraphs

def process_pdfs_in_alphabet_folders(root_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Percorre as pastas com letras (A, B, C, ...)
    for letter_folder in os.listdir(root_folder):
        letter_path = os.path.join(root_folder, letter_folder)
        if os.path.isdir(letter_path):
            print(f"Processando pasta: {letter_folder}")

            # Para cada PDF dentro dessa pasta de letra
            for file_name in os.listdir(letter_path):
                if file_name.lower().endswith(".pdf"):
                    pdf_path = os.path.join(letter_path, file_name)
                    print(f"Lendo {pdf_path} ...")
                    text = extract_text_from_pdf(pdf_path)
                    paragraphs = extract_paragraphs_with_indicators(text)

                    if paragraphs:
                        # Cria nome de arquivo para salvar baseado no arquivo pdf (sem extensão)
                        base_name = os.path.splitext(file_name)[0]
                        output_path = os.path.join(output_folder, f"{letter_folder}_{base_name}_indicator_paragraphs.txt")
                        with open(output_path, "w", encoding="utf-8") as f_out:
                            for para in paragraphs:
                                f_out.write(para + "\n\n")
                        print(f"{len(paragraphs)} parágrafos extraídos para {output_path}")
                    else:
                        print(f"Nenhum parágrafo com indicadores encontrado em {file_name}")

if __name__ == "__main__":
    pasta_raiz = "/Users/i553815/lerning/bibliographic_analysis/newProject/Articles/All Papers"
    pasta_saida = "/Users/i553815/lerning/bibliographic_analysis/newProject/classification/output"
    process_pdfs_in_alphabet_folders(pasta_raiz, pasta_saida)
