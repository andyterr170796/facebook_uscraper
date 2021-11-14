from sys import exit
import pandas as pd
import re
import calendar
import time
import os
import platform
import sys
import time
from urllib.request import urlretrieve #pip install resumable-urlretrieve
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
# NOTE: if you are using using Google Colab or other virtual environment that use webdriver.Chrome, ignore driver_path

class FB_scraper:
    
    def __init__(self,correo,contra,direct,driver_path='',chromedriver=''):
        # Iniciando Chromedriver
        self.correo = correo
        self.contra = contra
        self.direct = direct
        if driver_path!='':
            self.driver_path = driver_path
            options = webdriver.ChromeOptions()
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-infobars")
            options.add_argument("--mute-audio")
            options.add_argument("--start-maximized")
            self.driver = webdriver.Chrome(self.driver_path, chrome_options=options)
            self.chromedriver = chromedriver
        else:
            self.driver_path = driver_path
            self.driver = chromedriver

        print('Entrando a la cuenta de',self.correo)
        self.driver.get("https://web.facebook.com/")
        time.sleep(5)
        self.driver.find_element(By.XPATH,"//input[contains(@id,'email')]").send_keys(self.correo)
        self.driver.find_element(By.XPATH,"//input[contains(@id,'pass')]").send_keys(self.contra)
        self.driver.find_element(By.XPATH,"//button[contains(@name,'login')]").click()
        time.sleep(10)
        print('Listo')
        print('Recuerda!!! Configuración debe estar en Español, no Español (España)')
        
        # Entrando a directorio con imágenes
        os.chdir(self.direct)

    def log_friend(self,url):    
        self.driver.get(url)
        time.sleep(7)
        name = self.driver.find_element(By.XPATH,'//h1')
        name = name.text
        return name
        
    def scrape(self,num_de_pub,url):
        # Cargamos un diccionario de imágenes de reacciones para su reconocimiento
        like = Image.open('0.png')
        love = Image.open('1.png')
        haha = Image.open('2.png')
        wow = Image.open('3.png')
        sad = Image.open('4.png')
        hate = Image.open('5.png')
        care = Image.open('6.png')
        
        # Listas para guardar resultados
        nombres = []
        textos = []
        urls = []
        likes = []
        loves = []
        hahas = []
        wows = []
        sads = []
        hates = []
        cares = []
        
        name = self.log_friend(url)
        
        # Bucle para diferentes publicaciones
        lll=1500
        sgh = 1
        
        for publ in range(sgh,sgh+num_de_pub):
            # Bajamos un poco la página
            nombres.append(name)
            time.sleep(3)
            bajar = 'window.scrollTo(0,' + str(lll) + ')' # para que cargue un poco la página
            self.driver.execute_script(bajar)
            lll2 = lll
            publ2=publ
            while publ2-sgh>0:
                lll2=lll2+800        
                bajar = 'window.scrollTo(0,' + str(lll2) + ')'
                self.driver.execute_script(bajar)
                time.sleep(2)
                publ2=publ2-1
                
            time.sleep(10)
        
            # Nos movemos a la publicación que deseamos scrapear
            pub_numero=publ
            
            try:
                element=self.driver.find_element(By.XPATH,"//div[contains(@data-pagelet,'ProfileTimeline')]/div["+str(pub_numero)+"]//span[contains(@dir,'auto')]/span") # ubicamos el driver en la fecha (puesto que ahí está el id del post, para analizar más fácil)
                self.driver.execute_script("arguments[0].scrollIntoView();", element)
                self.driver.execute_script("scrollBy(0,-200);") # subimos un poco la página puesto que está la ventana flotante de botones
                element.click()
                time.sleep(5)
                
                # Volvemos arriba para no malversar el scraping
                self.driver.execute_script("scroll(0, 0);")
                time.sleep(5)
                urls.append(self.driver.current_url)
            
            except:
                lll2=lll2-800        
                bajar = 'window.scrollTo(0,' + str(lll2) + ')'
                self.driver.execute_script("scrollBy(0,-500);")
                time.sleep(5)

                element=self.driver.find_element(By.XPATH,"//div[contains(@data-pagelet,'ProfileTimeline')]/div["+str(pub_numero)+"]//span[contains(@dir,'auto')]/span") # ubicamos el driver en la fecha (puesto que ahí está el id del post, para analizar más fácil)
                self.driver.execute_script("arguments[0].scrollIntoView();", element)
                self.driver.execute_script("scrollBy(0,-200);") # subimos un poco la página puesto que está la ventana flotante de botones
                element.click()
                time.sleep(5)
                
                # Volvemos arriba para no malversar el scraping
                self.driver.execute_script("scroll(0, 0);")
                time.sleep(5)
                urls.append(self.driver.current_url)
                
            try:
                # Obtenemos el texto de la publicación                
                texto=self.driver.find_element(By.XPATH,"//div[contains(@data-ad-preview,'message')]")
                texto=texto.text
                print(texto)
                textos.append(texto)
                                
            except:
                textos.append("")
            
            try:           
                # Damos click a las reacciones para ver reacción por reacción
                self.driver.find_element(By.XPATH,"//span[contains(@aria-label,'Consulta quién reaccionó a esto')]").click()
                time.sleep(5)
                
                # Encontramos el número de reacciones distintas
                reac_num=self.driver.find_elements(By.XPATH,"//div[contains(@aria-label,'Reacciones')]//div[contains(@role,'tab')]/div/div/img[contains(@src,'http')]")
                
                # Ahora sí, damos click reacción por reacción, vemos que imagen es y la comparamos con el diccionario, retorna que tipo de reacción es, y el scraping su cantidad
                for z in range(0,len(reac_num)):
                    if len(reac_num)==1:
                        reac=reac_num[z].get_attribute("src")
                        reac_cant=self.driver.find_elements(By.XPATH,"//div[contains(@aria-label,'Reacciones')]//div[contains(@role,'tab')]/div/span/span")
                        r=reac_cant[0].text
                        urlretrieve(reac, 'comparar.png')
                        reaccion = Image.open('comparar.png')
                        if list(like.getdata()) == list(reaccion.getdata()):
                            print(r,"likes")
                            likes.append(r)
                        if list(love.getdata()) == list(reaccion.getdata()):
                            print(r,"loves")
                            loves.append(r)
                        if list(haha.getdata()) == list(reaccion.getdata()):
                            print(r,"hahas")
                            hahas.append(r)
                        if list(wow.getdata()) == list(reaccion.getdata()):
                            print(r,"wows")
                            wows.append(r)
                        if list(sad.getdata()) == list(reaccion.getdata()):
                            print(r,"sads")
                            sads.append(r)
                        if list(hate.getdata()) == list(reaccion.getdata()):
                            print(r,"hates")
                            hates.append(r)
                        if list(care.getdata()) == list(reaccion.getdata()):
                            print(r,"cares")
                            cares.append(r)
                            
                    else:
                        self.driver.find_element(By.XPATH,"//div[contains(@aria-label,'Reacciones')]//div[contains(@role,'tab')]["+str(z+2)+"]").click()
                        reac=reac_num[z].get_attribute("src")
                        reac_cant=self.driver.find_elements(By.XPATH,"//div[contains(@aria-label,'Reacciones')]//div[contains(@role,'tab')]/div/span/span")
                        r=reac_cant[0].text
                        urlretrieve(reac, 'comparar.png')
                        reaccion = Image.open('comparar.png')
                        if list(like.getdata()) == list(reaccion.getdata()):
                            print(r,"likes")
                            likes.append(r)
                        if list(love.getdata()) == list(reaccion.getdata()):
                            print(r,"loves")
                            loves.append(r)
                        if list(haha.getdata()) == list(reaccion.getdata()):
                            print(r,"hahas")
                            hahas.append(r)
                        if list(wow.getdata()) == list(reaccion.getdata()):
                            print(r,"wows")
                            wows.append(r)
                        if list(sad.getdata()) == list(reaccion.getdata()):
                            print(r,"sads")
                            sads.append(r)
                        if list(hate.getdata()) == list(reaccion.getdata()):
                            print(r,"hates")
                            hates.append(r)
                        if list(care.getdata()) == list(reaccion.getdata()):
                            print(r,"cares")
                            cares.append(r)
                
                if len(likes)!=publ:
                    likes.append("0")
                if len(loves)!=publ:
                    loves.append("0")
                if len(hahas)!=publ:
                    hahas.append("0")
                if len(wows)!=publ:
                    wows.append("0")
                if len(sads)!=publ:
                    sads.append("0")
                if len(hates)!=publ:
                    hates.append("0")
                if len(cares)!=publ:
                    cares.append("0")
                    
                self.driver.back()
                time.sleep(3)
                
            except:
                likes.append("0")
                loves.append("0")
                hahas.append("0")
                wows.append("0")
                sads.append("0")
                hates.append("0")
                cares.append("0")
                self.driver.back()
                time.sleep(3)
                
        fb = pd.DataFrame(data=[nombres,textos,urls,likes,loves,hahas,wows,sads,hates,cares]).transpose()
        fb.columns = ["Nombre en Facebook","Contenido","URL Post","Likes","Loves","HAHAs","WOWs","Sads","Hates","Cares"]
        fb.to_excel("aqui.xlsx",index=False)
