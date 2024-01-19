import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

start_url = "https://www.congreso.gob.pe/integrantescomisionespermanentes"
url_list = "https://www.congreso.gob.pe/integrantescomisionespermanentes?=undefined&m21_idP="

congresistas={
  'Nombres del Congresista':[],
  'Votacion Obtenida':[],
  'Año Legislativo':[],
  'Inicio de Funciones':[],
  'Termino de Funciones':[],
  'Partido Politico':[],
  'Bancada que pertence':[],
  'Representa a':[],
  'Url de Proyectos':[],
  'Condicion':[]
}


def getYears(url):
  try:
    years = []
    html_doc = requests.get(url).content
    soup = BeautifulSoup(html_doc, 'html.parser')
    select = soup.select('select[name="idRegistroPadre"]')[0]
    for op in select:
      years.append( {"value":op.get("value"), "year":op.get_text()})
  except Exception as e:
    print(e)
  finally:
    return years



def getCongresistaData(url, year):
  try:
    html_doc = requests.get(url).content
    soup = BeautifulSoup(html_doc, 'html.parser')
    nombre = soup.select('.dpersonales .value')[0].get_text()
    votacion = soup.select('.dgenerales .votacion .value')[0].get_text()
    votacion = votacion.replace('"', '')
    votacion = votacion.replace(',', '')

    inicioFunciones = soup.select('.dgenerales .periodo .periododatos')[0].select_one('.value').get_text()
    terminoFunciones = soup.select('.dgenerales .periodo .periododatos')[1].select_one('.value').get_text()
    partidoPolitico = soup.select('.dgenerales .grupo .value')[0].get_text()
    bancada = soup.select('.dgenerales .bancada .value')[0].get_text()
    representa = soup.select('.dgenerales .representa .value')[0].get_text()
    urlProyecto = soup.select('.dpersonales .web .value a')[0].get('href')
    condicion = soup.select('.dgenerales .condicion .value')[0].get_text()
    congresistas["Url de Proyectos"].append(urlProyecto)
    congresistas["Año Legislativo"].append(year)
    congresistas["Nombres del Congresista"].append(nombre)
    congresistas["Votacion Obtenida"].append(votacion)
    congresistas["Inicio de Funciones"].append(inicioFunciones)
    congresistas["Termino de Funciones"].append(terminoFunciones)
    congresistas["Partido Politico"].append(partidoPolitico)
    congresistas["Bancada que pertence"].append(bancada)
    congresistas["Representa a"].append(representa)
    congresistas["Condicion"].append(condicion)
  except Exception as e:
    print(e)

def scrapCongresistas(url, year):
  try:
    html_doc = requests.get(url).content
    soup = BeautifulSoup(html_doc, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')
    rows.pop(0)
    print(f'{len(rows)} Congresistas en total')
    for row in rows:
      url_congresista = start_url + row.select('td:nth-child(2) .conginfo')[0].get("href")
      getCongresistaData(url_congresista, year)
  except Exception as e:
    print(e)


years = getYears(start_url)
for kv in years:
  if(len(kv["year"])>0 and int(kv["year"]) > 2021 ): ##1994
    url = url_list+kv["value"]
    print(url)
    scrapCongresistas(url, kv["year"])
    
df = pd.DataFrame(congresistas)
df.to_csv('./data/congresista.csv', index=False)
