from requests import get
from bs4 import BeautifulSoup 
from pattern.web import plaintext
from pandas import DataFrame
import re
import csv

presidentes_nomes = {
    'Bolsonaro':'Bolsonaro',
    'Luiz': 'Lula',
    'Lula': 'Lula',
    'Temer' : 'Temer',
    'Dilma' : 'Dilma',
    'Cardoso' : 'FHC',
    'Collor':'Collor'
}

def pega_discurso(pagina):
    text = pagina.find_all('div',{'itemprop':'articleBody'})[0].get_text()
    return text

def pega_data(pagina):
    text = pagina.find_all('time',{'itemprop':'dateCreated'})[0]['datetime']
    return text.split('T')[0]

def pega_presidente(pagina):
    titulo = pagina.find_all('h1',{'class':'documentFirstHeading'})[0].a.get_text()
    for nome in presidentes_nomes.keys():
        if nome in titulo:
            return presidentes_nomes[nome]
    return "Desconhecido"

def pega_todos_discursos():
    df = DataFrame()
    urls_csv = open('discursos_urls.csv','r')
    url_reader = csv.reader(urls_csv)
    i = 0
    for row in url_reader:
        print(i)
        i += 1
        htmlString = get(row[0]).text
        soup = BeautifulSoup(htmlString,'lxml')
        
        discurso = dict()
        discurso['presidente'] = pega_presidente(soup)
        discurso['data'] = pega_data(soup)
        discurso['discurso'] = pega_discurso(soup)
        
        df = df.append(discurso,ignore_index=True)
    return df

discursos = pega_todos_discursos()
f = open("discursos.csv","w")
f.write(discursos.to_csv())
f.close()
