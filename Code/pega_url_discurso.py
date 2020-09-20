from requests import get
from bs4 import BeautifulSoup 
from pattern.web import plaintext


def pega_lista_url_discursos():
    url_base = 'http://www.itamaraty.gov.br'
    url_compl = '/pt-BR/discursos-artigos-e-entrevistas-categoria/presidente-da-republica-federativa-do-brasil-discursos?start='
    mod = 15 # Quantos aparecem por pagina
    max_paginas = 26 # Quantas paginas existem
    url_list = list()
    for num_pagina in range(0, max_paginas):
        print("Pagina " + str(num_pagina))
        
        start_num = str(num_pagina * mod)
        complete_url = url_base + url_compl + start_num
        htmlString = get(complete_url).text
        soup = BeautifulSoup(htmlString,'lxml')

        tiles = soup.find_all('div', {'class':'tileItem'})

        for tile in tiles:
            link = tile.find_all('a')
            if link is not None:
                url = link[0]['href']
                url_list.append(url_base + url)
    return url_list
                
url_list = pega_lista_url_discursos()
f = open("discursos_urls.csv", "w")
for link in url_list:
    f.write(str(link) + "\n")
f.close()



