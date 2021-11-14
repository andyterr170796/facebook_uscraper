#!git clone https://github.com/andyterr170796/facebook_uscraper
import os
correo="tu_correo"
contra="tu_contrasena"
direct=r"C:\Users\metro\Desktop\Test" # Tu directory path
os.chdir(direct)
driver_path=r"C:\Users\metro\AppData\Local\Programs\Python\Python38\Lib\site-packages\selenium\chromedriver.exe" # Tu chromedriver path

from facebook_uscraper import facebook_uscraper

s = FB_scraper(correo=correo, contra=contra,direct=direct,driver_path=driver_path)
x = 0

for scrapeados in ["url_fb_amigo1","url_fb_amigo2",
                   "url_fb_amigo3"]:
    s.scrape(url=scrapeados,num_de_pub=10)
    exec(f"bd_{x}=pd.read_excel('aqui.xlsx')")
    x = x + 1

pdList = []
pdList.extend(value for name, value in locals().items() if name.startswith('bd_'))
data = pd.concat(pdList)
