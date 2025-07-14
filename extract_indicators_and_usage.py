import os
import re
import csv

# Pasta com os arquivos de parágrafos (um .txt por artigo)
INPUT_FOLDER = "output_paragraphs"
OUTPUT_CSV = "resultado_indicadores.csv"

# Padrões combinados (nomes, listas, fórmulas, etc.)
indicator_patterns = [

    # Expressões conhecidas
    r"\bperformance indicators?\b",
    r"\bperformance measures?\b",
    r"\bmeasure[s]? of performance\b",
    r"\bperformance metrics?\b",
    r"\bmetrics? of performance\b",
    r"\bKPIs?\b",
    r"\bkey performance indicators?\b",
    r"\bindicators? of performance\b",

    # Exemplos após "such as", "including", etc.
    r"(?:such as|including|like)\s+([a-zA-Z0-9 ,\-\/]+)",

    # Expressões completas seguidas de lista de indicadores
    r"\b(?:performance indicators?|performance measures?|measures? of performance|performance metrics?|metrics? of performance|KPIs?|key performance indicators?|indicators? of performance)\s*[:\-]?\s*([a-zA-Z0-9 ,\-\/]+)",

    # Nome antes de "indicator"
    r"\b([a-zA-Z0-9 ]+ indicator[s]?)\b",

    # Fórmulas do tipo "KPI = fórmula"
    r"\b([A-Za-z0-9_ ]{2,30})\s*=\s*[^=\n]+"
]

# Padrões para uso do indicador
usage_patterns = [
    r"(used to|used for|helps to|helps in|serves to|aims to|allow[s]? to|enables)\s+([a-zA-Z0-9 ,\-]+)",
    r"(in order to|to)\s+([a-zA-Z0-9 ,\-]+)"
]

def extract_indicators(paragraph):
    indicators = []
    for pattern in indicator_patterns:
        matches = re.findall(pattern, paragraph, flags=re.IGNORECASE)
        for m in matches:
            # Se for tupla (grupo), pega o que for texto
            text = m[1] if isinstance(m, tuple) else m
            # Divide se for lista de indicadores
            parts = re.split(r",| and ", text)
            for p in parts:
                clean = p.strip().lower()
                if clean and clean not in indicators:
                    indicators.append(clean)
    return indicators

def extract_usage(paragraph):
    for pattern in usage_patterns:
        match = re.search(pattern, paragraph, flags=re.IGNORECASE)
        if match:
            return match.group(2).strip()
    return ""

def process_all_txts(input_folder, output_csv):
    results = []

    for file_name in os.listdir(input_folder):
        if file_name.endswith(".txt"):
            file_path = os.path.join(input_folder, file_name)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                paragraphs = content.split("\n\n")
                for paragraph in paragraphs:
                    paragraph = paragraph.strip()
                    if paragraph:
                        indicators = extract_indicators(paragraph)
                        usage = extract_usage(paragraph)
                        results.append({
                            "arquivo": file_name,
                            "paragrafo": paragraph,
                            "indicadores": ", ".join(indicators),
                            "uso": usage
                        })

    # Salva CSV
    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["arquivo", "paragrafo", "indicadores", "uso"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)

    print(f"✅ CSV salvo em {output_csv} com {len(results)} parágrafos processados.")

# Executa o script
if __name__ == "__main__":
    process_all_txts(INPUT_FOLDER, OUTPUT_CSV)


# Caminho onde estão os arquivos .txt com parágrafos
INPUT_FOLDER = "/Users/i553815/lerning/bibliographic_analysis/newProject/classification/output_paragraphs"
OUTPUT_CSV = "/Users/i553815/lerning/bibliographic_analysis/newProject/classification/output_indicators"

# Rodar o script
if __name__ == "__main__":
    process_txt_files(INPUT_FOLDER, OUTPUT_CSV)
