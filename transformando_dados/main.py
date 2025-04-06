import pdfplumber
import os
import pandas as pd

pdf_path = os.path.join('web_scraping/pdfs', 'Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf')

csv_path = "tabelas_extraidas.csv"

abreviacoes= {
    'OD': 'Seg. Odontológica',
    'AMB': 'Seg. Ambulatorial',
    'HCO': 'Seg. Hospitalar Com Obstetrícia',
    'HSO': 'Seg. Hospitalar Sem Obstetrícia',
    'REF': 'Plano Referência'
}

def substituir_abreviacoes(celula):
    if isinstance(celula, str):  # Verifica se a célula é uma string
        for abreviacao, completo in abreviacoes.items():
            celula = celula.replace(abreviacao, completo)
    return celula

with pdfplumber.open(pdf_path) as pdf:
    all_tables = []  # Lista para armazenar todas as tabelas extraídas

    # Iterar por todas as páginas do PDF
    for page_num, page in enumerate(pdf.pages):
        print(f"Extraindo tabelas da página {page_num + 1}...")
        
        # Extrair todas as tabelas da página
        tabelas = page.extract_tables()

        # Adicionar as tabelas extraídas à lista
        all_tables.extend(tabelas)

    # Converter a lista de tabelas para DataFrame e salvar como CSV
    for i, tabela in enumerate(all_tables):
        df = pd.DataFrame(tabela[1:], columns=tabela[0])  # Usando a primeira linha como cabeçalho
        
        # Substituir as abreviações em todas as células do DataFrame
        df = df.applymap(substituir_abreviacoes)

        # Salvar o DataFrame como CSV
        df.to_csv(f"{csv_path}_tabela_{i + 1}.csv", index=False)
        print(f"Tabela {i + 1} salva em {csv_path}_tabela_{i + 1}.csv")