import PyPDF2
import csv
import re

# Percorso del file PDF
pdf_path = r"C:\Users\JoaquimFrancalanci\Downloads\Linea_E014 sett-2024.pdf"
output_csv = 'orari_guardamiglio_codogno.csv'

# Funzione per estrarre testo dal PDF
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
        return text

# Funzione per trovare gli orari con la validità SC5 tra Guardamiglio e Codogno
def extract_guardamiglio_codogno_times(text):
    # Regex per trovare le righe con Guardamiglio e Codogno Ferrovia che includono la validità SC5
    pattern = r'(GUARDAMIGLIO-Via De Gasperi/fr Via Kennedy.*?SC5.*?\d{2}:\d{2})|(CODOGNO-Ferrovia.*?SC5.*?\d{2}:\d{2})'
    matches = re.findall(pattern, text)
    
    # Filtrare e riorganizzare i risultati
    results = []
    guardamiglio_times = []
    codogno_times = []
    
    for match in matches:
        # Filtra la tupla e prendi solo l'elemento non vuoto
        row = [m for m in match if m]
        if row:
            # Determina se è Guardamiglio o Codogno
            if "GUARDAMIGLIO" in row[0]:
                guardamiglio_times.append(row[0])
            elif "CODOGNO" in row[0]:
                codogno_times.append(row[0])
    
    # Abbina gli orari andata e ritorno
    for i in range(min(len(guardamiglio_times), len(codogno_times))):
        if i % 2 == 0:
            # Andata: Guardamiglio -> Codogno
            guardamiglio_time = re.search(r'\d{2}:\d{2}', guardamiglio_times[i]).group()
            codogno_time = re.search(r'\d{2}:\d{2}', codogno_times[i]).group()
            results.append(["Guardamiglio", guardamiglio_time, "Codogno", codogno_time])
        else:
            # Ritorno: Codogno -> Guardamiglio
            codogno_time = re.search(r'\d{2}:\d{2}', codogno_times[i]).group()
            guardamiglio_time = re.search(r'\d{2}:\d{2}', guardamiglio_times[i]).group()
            results.append(["Codogno", codogno_time, "Guardamiglio", guardamiglio_time])
    
    return results

# Funzione per scrivere gli orari in un CSV
def write_to_csv(data, output_file):
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Partenza', 'Orario', 'Arrivo', 'Orario'])  # Intestazione del CSV
        for row in data:
            writer.writerow(row)

# Estrarre testo dal PDF
pdf_text = extract_text_from_pdf(pdf_path)

# Estrarre gli orari tra Guardamiglio e Codogno Ferrovia solo per SC5
orari_guardamiglio_codogno = extract_guardamiglio_codogno_times(pdf_text)

# Scrivere il risultato nel file CSV
write_to_csv(orari_guardamiglio_codogno, output_csv)

print(f"I dati sono stati salvati in {output_csv}")
