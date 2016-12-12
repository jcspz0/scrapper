import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import load_url
import dao.normalizar

## CREATED:Rudy villagomez 
## MAIL	  :villagomezzr@gmail.com

def normalizar():
	dao.normalizar.normalizacion()


##METODO INICIADOR DEL SCRAPING
def start():
	load_url.begin_loadUrl()
	normalizar()
start()	
