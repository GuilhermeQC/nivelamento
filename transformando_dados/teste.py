import pdfplumber
import pandas as pd
import zipfile
import os

# Dicionário de abreviações para substituição
abreviacoes = {
    'OD': 'Seg. Odontológica',
    'AMB': 'Seg. Ambulatorial',
    'HCO': 'Seg. Hospitalar Com Obstetrícia',
    'HSO': 'Seg. Hospitalar Sem Obstetrícia',
    'REF': 'Plano Referência'
}

# Função para substituir abreviações
def substituir_abreviacoes(celula):
    if isinstance(celula, str):  # Verifica se a célula é uma string
        for abreviacao, completo in abreviacoes.items():
            celula = celula.replace(abreviacao, completo)
    return celula

# Caminho do arquivo PDF
pdf_path = os.path.join('web_scraping/pdfs', 'Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf')  # Substitua com o caminho do seu PDF

# Caminho para salvar o arquivo CSV
csv_path = os.path.join('transformando_dados', 'tabelas_extraidas.csv')  

# Abrir o PDF usando pdfplumber
with pdfplumber.open(pdf_path) as pdf:
    all_tables = []  # Lista para armazenar todas as tabelas extraídas

    # Iterar por todas as páginas do PDF
    for page_num, page in enumerate(pdf.pages):
        print(f"Extraindo tabelas da página {page_num + 1}...")
        
        # Extrair todas as tabelas da página
        tabelas = page.extract_tables()

        # Adicionar as tabelas extraídas à lista
        all_tables.extend(tabelas)

    # Converter a lista de tabelas para DataFrame
    # Assumindo que todas as tabelas extraídas possuem a mesma estrutura
    df = pd.DataFrame(all_tables[0][1:], columns=all_tables[0][0])  # Usando a primeira linha como cabeçalho
    
    # Substituir as abreviações nas colunas
    df = df.applymap(substituir_abreviacoes)

    # Salvar os dados no CSV
    df.to_csv(csv_path, index=False)
    print(f"Arquivo CSV salvo como {csv_path}")

# Compactar o CSV em um arquivo ZIP
zip_filename = f"Teste_{'Gui'}.zip"  # Substitua 'SeuNome' pelo seu nome

with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(csv_path, os.path.basename(csv_path))  # Adiciona o CSV ao ZIP
    print(f"Arquivo CSV compactado em {zip_filename}")
