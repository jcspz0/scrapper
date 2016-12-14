import requests
from bs4 import BeautifulSoup
import os.path, sys
import scrapers.hard_code_util
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import dao.segmentoDAO
import dao.leyDAO
import logger
import params
import scraper

## CREATED:Rudy villagomez 
## MAIL	  :villagomezzr@gmail.com
#***************************************************************************************************


def get_url_table(url_legis):	
	print 'url legis',url_legis
	misHeaders = {'user-agent': 'Mozilla/5.0 '}	
	response = requests.get(url_legis , headers = misHeaders)
	plain_text = response.text
	soup = BeautifulSoup(plain_text,'html.parser')		
	#caso para cuando son las exception hay que codificar
	div=soup.find('div',{'class':'plain'})
	print 'div',str(div)
	id_legis_verifi=scrapers.hard_code_util.get_idLegislacion_url(url_legis)
	#caso para medidas probistas 
	if id_legis_verifi == scrapers.hard_code_util.MEDIDA_PROVISTA:
		tables=div.find_all('table')
		print 'table len ',len(tables)
		arIdTable=[]
		if len(tables) == 2:
			arr_a_tb1=tables[0].find_all('a')
			arr_a_tb2=tables[1].find_all('a')

			arIdTable.append(scrapers.hard_code_util.MEDIDA_PROVISTA)
			arIdTable.append(['MPV',arr_a_tb1])
			arIdTable.append(['MP',arr_a_tb2])
			return arIdTable
	#caso para decreto-ley	
	elif id_legis_verifi == scrapers.hard_code_util.DECRETO_LEY :
		table=div.find_all('table')
		td=table[0].find_all('td')
		arrIdLeg=[]
		if len(td)==2:
			a1=td[0].find_all('a')
			a2=td[1].find_all('a')	
			arrIdLeg.append(scrapers.hard_code_util.DECRETO_LEY)
			arrIdLeg.append(['DEL',a1])
			arrIdLeg.append(['DL',a2])
			return arrIdLeg
	elif id_legis_verifi == scrapers.hard_code_util.LEY_ORDINARIA :	
		all_a=div.find_all('a')
		return all_a
	#caso para las emendas 	
	elif id_legis_verifi == scrapers.hard_code_util.EMENDAS:		
		table_em=soup.find_all('table')[1] #devuelve la tabla de emendas 
		tr=table_em.find_all('tr')		
		url_em='http://www.planalto.gov.br/ccivil_03/Constituicao/Emendas/Emc/'
		arr_a=[]
		for item_tr in tr:
			tds=item_tr.find_all('td')
			if tds[0].a is not None:
				if tds[0].a.get('href') != '':
					url_rela=tds[0].a.get('href')
					url_absolute=url_em+url_rela					
					b=BeautifulSoup()
					newtag=b.new_tag("a",href=url_absolute)					
					arr_a.append(newtag)
		return arr_a			


			
				
	elif id_legis_verifi != scrapers.hard_code_util.URL_ID_LEGIS_VACIA:		
		if div is not None:
			if len(div.find_all('table'))== 1:
				tabla=div.find('table')
				a=tabla.find_all('a')## a es un areglo de enlaces 
				return a
	return None		

def procesarTabla_de_nivel_1(a):	
	ultil_print_url_table(a)
	for href in a:		
		url_ley=href['href']
		if scrapers.hard_code_util.filterURL(url_ley):			
			print '<<< # URL A PROCESARCE .... #>>>',url_ley
			params.url=url_ley		
			scraper.iniciarScraping(url_ley)
	return len(a)# retornamos cantidad de leyes procesadas

def ultil_print_url_table(a):
	if a is not None:
		print '################ urls Table a procesar ######################'
		for ele in a:		
			print '----------------------------------------------------------------------------------------------------------------'
			print str(ele)
			print '----------------------------------------------------------------------------------------------------------------'
		



def get_url_table_lv1_col1(url_legis):
	print '<<< # OBTENIENDO URLS DE LEGISLACION # >>>',url_legis
	misHeaders = {'user-agent': 'Mozilla/5.0 '}	
	response = requests.get(url_legis , headers = misHeaders)
	plain_text = response.text
	soup = BeautifulSoup(plain_text,'html.parser')	
	div=soup.find('div',{'class':'plain'})
	if div is not None:
		if len(div.find_all('table'))== 1:
			table=div.find('table')
			tr=table.find_all('tr')
			arrUrls=[]
			for elem_td in tr:
				td=elem_td.find_all('td')
				if len(td) > 0:				
					elem_td1=td[0] #columna uno aca esta la url
					arrUrls.append(elem_td1.a) 
			return arrUrls
	else:
		div=soup
        if len(div.find_all('table'))== 2:
            table=div.find_all('table')[1]
            tr=table.find_all('tr')
            arrUrls=[]
            for elem_td in tr:
                td=elem_td.find_all('td')
                if len(td) > 0:
                    elem_td1=td[0]
                    # elem_a=elem_td1.find('a')#caso en el que el link se encuentra de primer lugar en la columna 1
                    # if elem_a is not None:
                    # 	if elem_a.get('href') is not None:
                    # 		arrUrls.append(elem_td1.a)
                    # 	else:
                    # 		elem_a2=elem_a.find_next_sibling('a')#caso en el que link se encuentra de segundo y de primero no existe un href
                    # 		if elem_a2 is not None:
                    # 			if elem_a2.get('href') is not None:
                    # 				arrUrls.append(elem_a2)                  			
                    #probando con font
                    elem_font=elem_td1.find('font')
                    elem_a=elem_font.find('a')#caso en el que el link se encuentra de primer lugar en la columna 1
                    if elem_a is not None:
                    	if elem_a.get('href') is not None:
                    		arrUrls.append(elem_font.a)
                    	else:
                    		elem_a2=elem_a.find_next_sibling('a')#caso en el que link se encuentra de segundo y de primero no existe un href
                    		if elem_a2 is not None:
                    			if elem_a2.get('href') is not None:
                    				arrUrls.append(elem_a2)
            return arrUrls  
	return None		


def procesarTabla_de_nivel_2(a):
	print '################  TABLE DE NIVEL 2 ######################',a	
	ultil_print_url_table(a)
	identLegis=a[0]
	print 'ID LEGISLACION CASO ESPE',identLegis
	if identLegis == scrapers.hard_code_util.MEDIDA_PROVISTA or identLegis == scrapers.hard_code_util.DECRETO_LEY:
		arrIdTab=a[1:len(a)]#este es el array de tabla con identificador [['MPV',[a,a]],['MV',[a,a]]]		
		print '################  TABLE DE NIVEL 1 ######################'
		ultil_print_url_table(a)
		resulAnt=[0,0]
		for elmTb in arrIdTab:
			print 'ITEM TABLE',elmTb			
			resul=begin_procesar_table(elmTb[1],elmTb[0])
			resulAnt[0]=resulAnt[0]+resul[0]
			resulAnt[1]=resulAnt[1]+resul[1]
		return resulAnt	
	elif identLegis != scrapers.hard_code_util.URL_ID_LEGIS_VACIA:
		return begin_procesar_table(a)	

def begin_procesar_table(a,id_tbl_legi=''):
	countLv1=0
	for href in a:		
		url_ley=href.get('href')
		if url_ley is not None:			
			print '## URL DE NIVEL2 A PROCESAR....',url_ley
			if scrapers.hard_code_util.filterURL(url_ley):
				if scrapers.hard_code_util.isURL_relative(url_ley):
					url_ley=scrapers.hard_code_util.build_url_absolute(params.url_leg,url_ley,id_tbl_legi)
				
				arrUrlNivel1=get_url_table_lv1_col1(url_ley)#leer table de primer nivel primera columna 
			else:
				arrUrlNivel1=None #url mala 
						
			if arrUrlNivel1 is not None:
				countLv1 += len(arrUrlNivel1)
				for urlNiv1 in arrUrlNivel1:
					try:
						if urlNiv1.get('href') is not None:																	
							titulo_ley=urlNiv1.text
							url_nv1=urlNiv1['href']
							if scrapers.hard_code_util.filterURL(url_nv1) and scrapers.hard_code_util.is_url_valid(url_nv1):								
								params.url=url_nv1
								scraper.iniciarScraping(url_nv1,id_tbl_legi)
							elif scrapers.hard_code_util.filterURL(url_nv1) and scrapers.hard_code_util.isURL_relative(url_nv1):
								#caso de medidas provisorias que no llegaba a agarrar las cosas
								url_base=href.get('href')
								url_nv1=scrapers.hard_code_util.build_url_absolute_MVP(url_base,url_nv1)
								params.url=url_nv1
								scraper.iniciarScraping(url_nv1,id_tbl_legi)

					except Exception ,e:
						print 'Valor por el que da excepcion',urlNiv1
						logger.info('URL EXCEPCION :'+ str(urlNiv1))
            #aqui ponr algo en el caso de que los links no se encuentren dentro de class:plain															
	return [len(a),countLv1] # retornamos el conteo de URL de nivel2 y nivel1 				




def util_print_tab_legis(arrLegis):
	if arrLegis is not None:
		print '################ Table Legislacion ######################'
		for elem in arrLegis:
			print '----------------------------------------------------------------------------------------'
			print str(elem)
			print '----------------------------------------------------------------------------------------'
		print 'carga completa'	

def begin_loadUrl():	
	arrLegis=dao.leyDAO.get_legislaciones()
	print arrLegis	
	#verificamos que el arry tenga len()>0 para comenzar scraping
	if len(arrLegis)>0:
		#obtenemos legislacion
		util_print_tab_legis(arrLegis)
		for legis in arrLegis:
			tipoScraper=legis[4]#obtenemos el tipo para saver si scraper sobre tabla o unica ley
			#seteamos el id de la legislacion a la que pertenece esta ley
			print 'TIPO SCRAPER',tipoScraper
			scrapers.hard_code_util.ID_LEGISLACION=legis[0]
			#obtenemos cant_url_lv
			cantUrl=legis[2:4] #// para obtener cant_url_lv1 y cant_url_lv2
			if tipoScraper == 'TB':	
				#parametro que nos ayuda para complementar las url relativas 
				params.url_leg=legis[1]
				urlsTabla=get_url_table(legis[1])#obtenemos las url de la tabla pasamos la url parametro				
				#verificamos si NO TIENE nivel 2
				if cantUrl[1]== -1:
					#verificamos si cant_url_lv1 >0 				
					if cantUrl[0] > 0: 
						#obtenemos camtidad de url de la tabla y verificamos si es mayor a cant_url_lv2					
						cantUrlTb=len(urlsTabla)
						if cantUrlTb > cantUrl[0]:						
							procesarTabla_de_nivel_1(urlsTabla)
							dao.leyDAO.set_nroUrl_level_1(legis[0],cantUrlTb)
						else:
							if not params.first_scraping:
								procesarTabla_de_nivel_1(urlsTabla) #verificamos si el peso de la ley cambio para scraping  

					else:
						
						countURL=procesarTabla_de_nivel_1(urlsTabla)
						dao.leyDAO.set_nroUrl_level_1(legis[0],countURL)	
				else:						
						#verificamos si cant_url_lv2 >0						
						if cantUrl[1] > 0:  
							#obtenemos camtidad de url del la tabla de nivel2  y verificamos si es mayor a cant_url_lv2
							if urlsTabla[0] == scrapers.hard_code_util.MEDIDA_PROVISTA or urlsTabla[0] == scrapers.hard_code_util.DECRETO_LEY:
								cantUrlTb=len(urlsTabla)-1
							else:
								cantUrlTb=len(urlsTabla)	
							
							if cantUrlTb > cantUrl[1]:								
								countURL=procesarTabla_de_nivel_2(urlsTabla)
								dao.leyDAO.set_nroUrl_level_2(legis[0],countURL[0])	
								dao.leyDAO.set_nroUrl_level_1(legis[0],countURL[1])
							else:
								if not params.first_scraping:
									countURL=procesarTabla_de_nivel_2(urlsTabla)								
									dao.leyDAO.set_nroUrl_level_1(legis[0],countURL[1])

							
						else: 							
							countURL=procesarTabla_de_nivel_2(urlsTabla)
							dao.leyDAO.set_nroUrl_level_2(legis[0],countURL[0])	
							dao.leyDAO.set_nroUrl_level_1(legis[0],countURL[1])
			
			elif tipoScraper == 'UN': #es de tipo unica ley				
				if cantUrl[0] == 0:
					params.url=legis[1]
					params.prefix=legis[5]
					scraper.iniciarScraping(params.url,params.prefix)
					dao.leyDAO.set_nroUrl_level_1(legis[0],1)				
	else: #si no tiene len()>0 mensaje cargue legislaciones
		print 'INSERTE LEGISLACIONES'




