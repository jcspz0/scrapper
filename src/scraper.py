import requests
from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
import logger
import params
import scrapers.hard_code_util
import dao.segmentoDAO
import dao.leyDAO
import scrapers.constitucion
import scrapers.scraping_dynamic
from selenium import webdriver
import load_url
import sys
import os
import codecs

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

## CREATED:Rudy villagomez 
## MAIL	  :villagomezzr@gmail.com


BEGING_DRIVER_GOOGLE=False
DRIVER_NAV_GOOGLE=None
PATH_LEY_SCRAPING=params.path_ley_scraping
PATH_DRIVER=params.path_driver
ARR_LEY_ENCODING_EXCEP=['http://www.planalto.gov.br/ccivil_03/Constituicao/Emendas/Emc/emc39.htm']

#PARA CUANDO ESTE CORRIENDO ESTE ARCHIVO TENER EN CUENTA QUE TENEMOS QUE CREAR LOS DIRECTORIOS NECESARIOS Y DRIVER COLOCAR DONDE CORRESPONDA
def is_ley_encoding_exception():
	global ARR_LEY_ENCODING_EXCEP
	misHeaders = {'user-agent': 'Mozilla/5.0 '}
	for elem in ARR_LEY_ENCODING_EXCEP:
		if elem	== params.url:
			response = requests.get(params.url,headers = misHeaders,verify=False)
			plain_text = response.text				
			soup = BeautifulSoup(plain_text,'html5lib')
			return soup
	return None		
def getContenHtmlSoup():
	
	global BEGING_DRIVER_GOOGLE,DRIVER_NAV_GOOGLE,PATH_LEY_SCRAPING
	misHeaders = {'user-agent': 'Mozilla/5.0 '}
	try:
		#verificando la exception de codificacion
		soup=is_ley_encoding_exception()
		if soup is not None:
			return soup
		if params.tipo_scraping == 'DRIVER_GOOGLE':			
			if not BEGING_DRIVER_GOOGLE:
				BEGING_DRIVER_GOOGLE=True
				DRIVER_NAV_GOOGLE = webdriver.Chrome(PATH_DRIVER)
			if 	DRIVER_NAV_GOOGLE is not None :
				DRIVER_NAV_GOOGLE.get(params.url);
				html = (DRIVER_NAV_GOOGLE.page_source)
				newLey = open(PATH_LEY_SCRAPING, "wt")
				newLey.write(html)
				newLey.close()			
				soup=BeautifulSoup(open(PATH_LEY_SCRAPING),'html.parser')				
				return soup
		else:
			response = requests.get(params.url,headers = misHeaders,verify=False)
			plain_text = response.text	
			soup = BeautifulSoup(plain_text,'html.parser')					
			return soup
	except Exception,e:
		print '<<<< # Pudo haver fallado el driver de google si no lo tiene instalado #>>>>>',str(e)
		print '<<<< # intentando reiniciar el proceso .... #>>>>>'
		logger.warn('Exception Modulo Scraping:'+str(e))		
		BEGING_DRIVER_GOOGLE=False
		load_url.begin_loadUrl()	
			





def iniciarScraping(url_ley,id_table_legis=''):	
	# logger.info('Iniciando Scraping - planalto')	
	response=None
	misHeaders = {'user-agent': 'Mozilla/5.0 '}	
	response = requests.head(params.url,headers = misHeaders,verify=False)
	if response.status_code == 200:#  peticion correcta	
		codigo_ley=scrapers.hard_code_util.get_codigoLey_url(url_ley,id_table_legis)	
		existsLey=dao.leyDAO.exists_ley(codigo_ley)
		size_page=scrapers.hard_code_util.get_size_page(response)
		print 'SIZE PAGE',size_page
		print 'existe',existsLey
		if existsLey is None: # entonces no existe insertamos
			procesarLey(getContenHtmlSoup(),url_ley,codigo_ley,size_page)
		elif existsLey[2] != size_page: # entonces actualizamos la ley
				dao.segmentoDAO.deleteSegmentos(existsLey[1])#pasamos el id_ley de segmento
				dao.leyDAO.deleteLey_by_id(existsLey[0])
				#luego mandamos a procesar ley
				procesarLey(getContenHtmlSoup(),url_ley,codigo_ley,size_page,existsLey[3])#mas el alias
		# logger.info('Finalizado ')

	else:
		logger.info('URL MALA :'+url_ley)
			


def procesarLey(soup,url_ley,codigo_ley,size_page,alias=''):
	print 'URL A SCRAPERAR: ',url_ley
	print 'CODIGO LEY: ',codigo_ley	
	if 'Constituicao' == codigo_ley or 'ConstituicaoCompilado' == codigo_ley:		
		scrapers.constitucion.procesarLegislacion(soup,url_ley,codigo_ley,size_page,alias)
	else:
		scrapers.scraping_dynamic.procesarLegislacion(soup,url_ley,codigo_ley,size_page,alias) 





## NO SE ESTAN OCUPANDO ESTOS MEDOTOS 
def crearHtml():
	f=open('C:\\xampp\\htdocs\\scraperDebug\\Constituicao.html','w')
	f.close()	
	cargarHtml()

def cargarHtml():
	response = requests.get(params.url,verify=False)
	plain_text = response.text	
	f=open('C:\\xampp\\htdocs\\scraperDebug\\Constituicao.html','a')
	f.write(plain_text)
	f.close()


