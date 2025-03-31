from bs4 import BeautifulSoup
import requests, os, zipfile
from pathlib import Path

busca = "Anexo"

pagina = requests.get(
    "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
)
soup = BeautifulSoup(pagina.content, "html.parser")

try:
    os.makedirs("web_scraping\pdfs")
except FileExistsError:
    pass

for link in soup.find_all("a", href=True):
    file_url = link["href"]

    if file_url.endswith(".pdf"):

        file_name = file_url.split("/")[-1]

        if file_name.startswith(busca):
            print(file_name)
            file_response = requests.get(file_url)

            file_path = f"web_scraping\pdfs\{file_name}"

            with open(file_path, "wb") as f:
                f.write(file_response.content)

pasta = Path("web_scraping\pdfs")
arquivos = [arquivo for arquivo in pasta.iterdir() if arquivo.is_file()]

arquivozip = pasta/'dadosrecolhidos.zip'
with zipfile.ZipFile(arquivozip, 'w') as zipf:
    for arquivo in arquivos:
        zipf.write(arquivo, arquivo.name)