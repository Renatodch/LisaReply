from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import pandas as pd

proyectos={
  'Nombres del Congresista':[],
  'Año Legislativo':[],
  'Periodo de Legislatura Ordinaria':[],
  'Fecha de Presentacion':[],
  'Estado':[],
  'Titulo':[],
  'Codigo':[],
}

#Aca usamos selenium
def getProyectoLeyDataIFrame(url,name, year):
  try:
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a")))
    data_elements = driver.find_elements(By.CSS_SELECTOR, ".mb-4.ng-star-inserted")
    for element in data_elements:
      period=element.text
      rows = element.find_elements(By.CSS_SELECTOR, ".p-datatable-tbody .ng-star-inserted")
      for row in rows:
        proyectos["Año Legislativo"].append(year)
        proyectos["Nombres del Congresista"].append(name)
        proyectos["Periodo de Legislatura Ordinaria"].append(period)
        col = row.find_element(By.CSS_SELECTOR, "td:nth-child(1)")
        proyectos["Codigo"].append(col.find_element(By.CSS_SELECTOR, "a").get_attribute('innerText'))
        col = row.find_element(By.CSS_SELECTOR, "td:nth-child(2)")
        proyectos["Fecha de Presentacion"].append(col.get_attribute('innerText'))
        col = row.find_element(By.CSS_SELECTOR, "td:nth-child(3)")
        proyectos["Estado"].append(col.get_attribute('innerText'))
        col = row.find_element(By.CSS_SELECTOR, "td:nth-child(4)")
        proyectos["Titulo"].append(col.get_attribute('innerText'))

  except Exception as e:
    print(e)

def getProyectoLeyData(url,name, year):
  try:
    html_doc = requests.get(url).content
    soup = BeautifulSoup(html_doc, 'html.parser')
    url_iframe=soup.select('iframe[name="ventana02"]')[0].get('src')
    if url_iframe != None:
      getProyectoLeyDataIFrame(url_iframe, name , year)

  except Exception as e:
    print(e)



df = pd.read_csv('./data/congresista.csv')
# Set up the Selenium webdriver (ensure you have the correct driver executable in your PATH)
driver = webdriver.Chrome()

for index, row in df.iterrows():
    name = row['Nombres del Congresista']
    year = row['Año Legislativo']
    url = row['Url de Proyectos']
    if(url != ""):
      url += "laborlegislativa/proyectos-ley/"
      print("Escrapeando proyectos desde: "+url)
      getProyectoLeyData(url, name, year)

df = pd.DataFrame(proyectos)
df.to_csv('./data/proyecto.csv', index=False)


driver.quit()
