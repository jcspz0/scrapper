import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import load_url

## CREATED:Rudy villagomez 
## MAIL	  :villagomezzr@gmail.com

##METODO INICIADOR DEL SCRAPING
def start():
	load_url.begin_loadUrl()

start()	
