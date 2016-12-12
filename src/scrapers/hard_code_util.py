# -*- encoding: utf-8 -*-
import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from bs4 import BeautifulSoup
import re
import params

## CREATED:Rudy villagomez 
## MAIL	  :villagomezzr@gmail.com



ID_LEGISLACION=0
#cosntantes para la codificacion de las exceptions
MEDIDA_PROVISTA='medidas-provisorias'
DECRETO_LEY='decretos-leis'
URL_ID_LEGIS_VACIA='url_id_legislacion_vacia'
LEY_ORDINARIA='leis-ordinarias'
EMENDAS='quadro_emc.htm'


# constantes posicion en el arbol 
POS_TITULO_LEY=8
POS_HEADER    =7

POS_PARTE     =6 
POS_LIBRO     =5 
POS_TITULO    =4 
POS_SUBTITULO =3 
POS_CAPITULO  =2
POS_SECCION   =1 
POS_SUBSECCION=0 
# posiciones e peciales pertenecen al arbol pero no lo representamos en el arbolAr ray
POS_FOOTER    =-2 
POS_ARTICULO  =- 1  


arbolArray=[None,None,None,None,None,None,None,None,None]


def clear_camino_identifi(posFinal):
	i=0
	while i<posFinal:
		arbolArray[i]=None
		i=i+1




def addTree(id,idenTifi,posArbol):
	if posArbol == POS_TITULO_LEY:
	    item=[id,idenTifi]
	    arbolArray[posArbol]=item
	    return item
	elif posArbol == POS_ARTICULO:
		 #aca vamos a recorrer el camino y obtener id padre
		 id_padre=buscarIdPadre(arbolArray) #tenemos que buscar en todo el arbol
		 caminoIdentifi=armarCaminoIdenArticulo(arbolArray,idenTifi)
		 resul=[id_padre,caminoIdentifi]
		 return resul

	elif posArbol == POS_HEADER:
	     item=[id,idenTifi]
	     arbolArray[posArbol]=item
	     return item		

	elif posArbol == POS_FOOTER:
		# SOLO SACAMOS EL PADRE DEL FOOTER
	    return arbolArray[POS_TITULO_LEY]

	## SI NO ENTRA A NINGUN CASO ES EL CASO GENERAL 
	arbolArray[posArbol]=[id,idenTifi]
	caminoIdParent=arbolArray[posArbol + 1:POS_TITULO_LEY + 1] #sumamos 1 a posArbol para no tomar encuenta nuestra posicion 
												               # y sumamos 1 a POST_TITULO_LEY para recorrer todo el arbol	
	#buscamos id padre 
	id_padre=buscarIdPadre(caminoIdParent)
	#armamos el camino conocido como identificador
	caminoIdentifi=arbolArray[posArbol:POS_TITULO_LEY + 1]
	cad_camino=armarCaminoIdentificador(caminoIdentifi)
	resul=[id_padre,cad_camino]
	return resul

def actualizarIdNodo(id,posicion):
	nodo=arbolArray[posicion]
	nodo[0]=id
	arbolArray[posicion]=nodo


def buscarIdPadre(caminoIdParent):
 	 	id_padre=0
 	 	for nodo in caminoIdParent:								   				
			if nodo is not None:
				id_padre=nodo[0]
				return id_padre


def armarCaminoIdentificador(caminoIdentifi):
	
	i=(len(caminoIdentifi)-1)##para enpezar en posTitulo_ley
	cad_camino=''
	while i > 0:		
		if caminoIdentifi[i] is not None:
			nodo=caminoIdentifi[i]
			cad_camino+=nodo[1] + '_'
		i=i-1
	nodUlt=caminoIdentifi[0]
	if nodUlt is not None:
		cad_camino += nodUlt[1]
	return cad_camino


def armarCaminoIdenArticulo(caminoIdentifi,identifi):	
	i=(len(caminoIdentifi)-1)##para enpezar en posTitulo_ley
	cad_camino=''
	while i > 0:		
		if caminoIdentifi[i] is not None:
			nodo=caminoIdentifi[i]
			cad_camino+=nodo[1] + '_'
		i=i-1
	nodUlt=caminoIdentifi[0]
	if nodUlt is not None:
		cad_camino += nodUlt[1]
	cad_camino +=identifi		
	return cad_camino




def isParte(text):
	if text is not None:		
		if ('P A R T E' in text or ('PARTE' in text and 'PARTES' not in text)):
			return True
		if 'Parte Geral' in text and  'PARTES' not in text:
			return True
		if 'PARTE GERAL' in text and  'PARTES' not in text:
			return True

	return False

def isLibro(text):	
	return text is not None and 'LIVRO' in text

def isSubTitulo(text):
	return text is not None and 'SUBTÍTULO' in text

def isTitulo(text):	
	if text is not None:
		if 'TÍTULO' in text:
			return True
		if 'TTULO' in str(text): 
			return True
		if 'Título' in text:
			return True	
	return False

def isCapitulo(text):
	if text is not None:
		if 'CAPÍTULO' in text:			
			return True
		if 'Capítulo' in text:
			return True
		if '"CAPÍTULO' in text:
			return True			
	return False

def isSeccion(text):		
	if text is not None:
		if 'Seção' in text:
			return True
		if 'SEÇÃO' in text:
			return True
		if 'SECÇÃO' in text:
			return True	
		if '"Seção' in text:
			return True				
	return False

def isSubSeccion(text):
	if text is not None:
		if 'subseção' in text:
			return True
		if 'SUBSEÇÃO' in text:
			return True
	return False		

def isArticulo(text):	
	if text is not None:
		if text.strip().startswith('Art.'):
			return True
		if text.strip().startswith('Art'):
			return True	

	return  False

def getNumeroTitular1(text):	
	if text is None:
		return '0'
	if isParte(text):
		cad = text.replace(' ', '')		
		if len(cad.split())> 1:
			return cad.split()[1]
		else:
			return cad.split()[0]	
		
	if len(text.split()) > 1:
		return text.split()[1]
	return None

def getNumeroTitular2(text):	
	if text is None:
		return '0'
	if len(text.split()) > 1:
		return text.split()[1]
	return None

#codigo para obtener datos del articulo con regex. grupo  0=todo el articulo, 2=numero del articulo,
# 3=si existe algun guion o el º , 4=la letra del articulo, 5= si termina en punto o coma el articulo
def contenido_articulo(texto,grupo):
	match=re.search(r'(A|a)rt\.(\n|\s|\t|&nbsp;)*(\d+)( |\º|-)*([a-zA-Z]{1})*(\.|\,)*', texto)
	if match:
		return match.group(grupo)
	else:
		return None		

def getNumeroArticulo(text):	
	if text is None :
		return '0'	
	# if len(text.split()) > 1:		 
	# 	 return text.split()[1] 	 	
	# if len(text.split()) == 1:
	# 	return '0'
	cont = contenido_articulo(text,3)#mod
	if cont is not None and cont != '':#mod
		return cont#mod
	else:#mod
		return '0'	#mod

def startEndConstitucion(text):	
	if text is not None :
		if  text == 'ANEXO':
			return True		
		if '5 de outubro de 1988.' in text:
			return True
		if 'Este texto não substitui' in text:
			return True
		if 'Este texto não' in text:
			return True			
		if 'FERNANDO	HENRIQUE CARDOSO' in text:
			return True			
	return False
def isAnexo(text):
		if text != '':
			return text == 'ANEXO'



def obtenerTituloLey(soup):
	n=soup.find('font', {'color': '#000080'})
	if n is not None:
		return n.text
	else:
		return None	
def util_get_codigo(part_titu):
	i=len(part_titu)-1
	while i >= 0:
		if part_titu[i] == '.':
			return part_titu[0:i]
		i=i-1			
def get_codigoLey_url(url_ley,id_tabl_legis):
	if url_ley != '':		
		url_titu=url_ley
		part_titu=url_titu.split('/')[-1]
		#ley_titu=part_titu.split('.')[0]
		ley_titu=util_get_codigo(part_titu)
		ley_titu=remove_point(ley_titu) #quita los puntos de medio
		if id_tabl_legis == 'MPV':
			return 'MPV'+encode_cod_ley_excep(ley_titu)
		elif id_tabl_legis == 'MP':	
			return 'MP'+encode_cod_ley_excep(ley_titu)
		elif id_tabl_legis == 'DEL':
			return 'DEL'+encode_cod_ley_excep(ley_titu)
		elif id_tabl_legis == 'DL':	
			return 'DL'+encode_cod_ley_excep(ley_titu)
		return ley_titu
	return 'url vacia'	

def remove_point(ley_titu):
	return ley_titu.replace('.','')


def encode_cod_ley_excep(codLey):
	arrCod=re.split('[a-zA-Z]',codLey)  
	i=(len(arrCod)-1)					
	while(i>=0):
		if arrCod[i] != '':
			return  arrCod[i].strip()
		i=i-1	

	

def obtenerCodigoLey(soup):
	t=soup.title.string
	titulo=str(t.encode('utf-8'))
	return titulo.replace(' ','')

def obtenerHeader(soup):
	tablas=soup.find_all('table',limit=2)
	table2=None	
	if tablas is not None and len(tablas) == 2:
		tabla2=tablas[1]		
		if tabla2 is not None:
			arr_td=tabla2.find_all('td')			
			if arr_td is not None and len(arr_td)>0:
				ultTd=arr_td[-1]				
				allTagUltd=ultTd.find_all()				
				if allTagUltd is not None and len(allTagUltd)>0:
					ultElemTabl=allTagUltd[-1]					
					p_precident_repub=ultElemTabl.find_next('p')					
					if p_precident_repub is not None:
						contHtml=''						
						if not isItemTree(p_precident_repub.getText()) and not isArticulo(p_precident_repub.getText()):							
							contHtml=str(tabla2)+str(p_precident_repub)							
						p_decreta=get_next_ele_decreta(p_precident_repub)
						print str(p_decreta)						
						if p_decreta is not None:
							if not isItemTree(p_decreta.getText()) and not isArticulo(p_decreta.getText()):
								contHtml +=str(p_decreta)	
					 	newHead=BeautifulSoup(contHtml,'html.parser')
						return newHead
	return None						

def get_next_ele_decreta(p_president):	
	p_decreta=p_president.find_next('h1')
	print('este es h1',p_decreta)
	if p_decreta is not None:
		h1=p_decreta.getText().replace('\n','').replace(' ','')
		print ('luego de quitar ',h1)
		if 'DECRETA:'in h1 :
			return p_decreta
	return p_president.find_next('p')

def isParent_table_tr_td(soup):
	if (soup.find_parent()).name == 'td':
		return True
	if (soup.find_parent()).name == 'tr':
		return True	
	if (soup.find_parent()).name == 'table':
		return True
	# caso para cunato <p> su padre es <font> y su padre es <td>	
	font=soup.find_parent()
	if font is not None and font.name == 'font':
		par_font=font.find_parent()
		if par_font is not None and par_font.name == 'td':
			return True	
	return False	

def isParent_table(soup):
	if soup is not None:
		parents=soup.parents
		for pr in parents:
			if pr.name == 'table' or 'td' or 'tr':
				return True
	return False				

def isParent_center_body(font):
	if font is not None:
		padreCenter=font.find_parent()		
		if padreCenter is not None and padreCenter.name == 'center':
			padreBody=padreCenter.find_parent()
			if padreBody is not None and padreBody.name == '[document]':  #es como body
				return True
	return False 


#funcion para controlar que se repitan las tablas en el caso de no cumplir la condicion de que una tabla
#su padre es un div pero se en cuentra en una estructura asi tabla-->center--->div (apliar esta funcion en la parte 
	#que controlamos el footer en el if que verifica tabla con padre div aumentar como un or )
def isParent_center_div(soup):
	if soup is not None:
		padreCenter=soup.find_parent()
		if padreCenter is not None :
			if padreCenter.name == 'center':
				padreDiv=padreCenter.find_parent()
				if padreDiv is not None :
					if padreDiv.name == 'div':
						return True	
	return False					

def isParent_p_center_body(font):
	if font is not None:
		padre_p=font.find_parent()
		if padre_p is not None and padre_p.name == 'p' and 	isParent_center_body(padre_p):
			return True
	False	

def isItemTree(text):
	return 	isParte(text) or isLibro(text) or  isTitulo(text) or isSubTitulo(text) or isCapitulo(text) or isSeccion(text) or isSubSeccion(text)				

def filterURL(url):
	if url is not None:
		urlSecion=url.split('.')						
		ulSec=urlSecion[-1] #obtenemos el ultimo elmento que viene a ser un html,doc,htm etc		
		if ulSec == 'doc' or ulSec == 'DOC' or ulSec ==  'docx':
			return False
		if ulSec == 'pdf' or ulSec == 'PDF':
			return False
		if ulSec == 'xlsx' or ulSec == 'xls' or ulSec == 'XLSX'  or ulSec == 'XLS' :
			return False
	else:
		return False															
	return True


def is_url_valid(url):
	if url.strip().startswith('http') or url.strip().startswith('www'):
		return True
	return False	

def isURL_relative(url):	
	if url.strip().startswith('http') or url.strip().startswith('www'):
			return False
	return True

def build_url_absolute(url_prin,url_se,id_table_legi=''):
	if id_table_legi=='MPV' or id_table_legi=='MP':
		arrUrlPart=url_prin.split('#')
		urlComple=arrUrlPart[0]+'/'+url_se
		return urlComple
	#caso general para algunas 	
	url_pric=url_prin
	url_sec=url_se
	surl_p=url_pric.split('/')
	surl_s=url_sec.split('/')

	i=(len(surl_p)-1)
	url_new=surl_p[0:(len(surl_p)-1)]
	while i >= 0:
		if surl_s[0]== surl_p[i]:
			url_new=surl_p[0:i]
		i=i-1
	print url_new
	s=''
	for item in url_new:	
		if item == '':
			s+='/'
		else:
			s+= item+'/' 
	print 'URL ABSOLUTA ', s + url_sec			
	return s + url_sec	


def clean_id_arti(nroArt):	
	if len(nroArt) > 1:
		nroArt=nroArt.strip()		
		i=len(nroArt)-1		
		while i >= 0:
			if re.match('[0-9]',nroArt[i]):				
				nroArt=nroArt[0:(i+1)]
				return nroArt
			i=i-1	
	
	return nroArt	

# def get_clean_article(arrayArt,pos):
# 	pos2=arrayArt[pos].split('-')
# 	# print pos2
# 	# print pos 
# 	# nroArt=pos2[0]
# 	if len(pos2) >= 3:
# 		# aca esta el nro del articulo a tratar 
# 		artToClear= pos2[0] +'-'+ pos2[1] 
# 		print artToClear
# 		return artToClear.strip()
# 	elif len(pos2) > 1:
# 		# aca esta el nro del articulo a tratar 
# 		artToClear= pos2[0]
# 		print artToClear
# 		return artToClear.strip()			
# 	elif pos2 is not None:
# 		# aca esta el nro del articulo a tratar 
# 		print pos2[0]
# 		if pos2[0] is None:
# 			pos2[0]=''
# 		mNroAct=re.findall(r'\d+', pos2[0])
# 		if len(mNroAct) > 0:
# 			return mNroAct[0]
# 		else:
# 			noPuntoArt=arrayArt[0]
# 			nArtCle=re.findall(r'\d+',noPuntoArt)
# 			if len(nArtCle) > 0:
# 				return nArtCle[0]
# 			else:
# 				return None	
def check_to_have_number(arry):
		if arry is not None and len(arry) > 0:
			for elemen in arry:
				conten = re.findall(r'\d+', elemen)
				if len(conten)> 0:
					return True
		else:
			return False
		return False	

def clean_nro_art(arry,pos):
	artClean = re.findall(r'\d+', arry[pos])
	if len(artClean) > 0:
		return artClean[0].strip()
	else:
		return None

def ckeck_is_artigo_unico_emc(textArt):
	arryArt = textArt.split('.')
	artigo = 'Artigoúnico'
	if len(arryArt) > 1:		
		if artigo in arryArt[0]:
			return artigo
		else:
			return None	
	else:
		return None		

def is_art_firs_position(textArt):
	arryArt = textArt.split('.')
	if len(arryArt) >= 2 and arryArt[0] is not None:		
		return clean_nro_art(arryArt,0)
	else:
		return None		

def none_nro_article(textArt):
	artClean = re.findall(r'\d+', textArt)
	if len(artClean) > 0:
		return False
	else:
		return True

				
def get_clean_article(textArt):
	if textArt is not None or textArt == '':
		
		noExistNroArt = none_nro_article(textArt)
		if noExistNroArt == True:
			return " "

		artFirsPosition = is_art_firs_position(textArt)
		if artFirsPosition is not None:
			return artFirsPosition

		artUnicoEmc = ckeck_is_artigo_unico_emc(textArt) 
		if artUnicoEmc is not None:
			return artUnicoEmc

		puntoSp=textArt.split('.')
		if len(puntoSp) >= 3:
			#para este caso Art93.HaveránoD.N.P.
			if check_to_have_number(puntoSp[1:len(puntoSp)]) == False :
				return clean_nro_art(puntoSp,0)

			if puntoSp[1] is None or puntoSp[1] == '': #es este caso > Art..195Acaracteri
				return clean_nro_art(puntoSp,2)

			else: #Art.235-G.Éjhuhhujiji
				if len(re.findall(r'\d+', puntoSp[1])) > 0 :
					sanetizar = "".join(re.split("[^a-zA-Z]*", puntoSp[1]))
					if sanetizar != '' and len(sanetizar) == 1 and 'A' <= sanetizar <= 'Z': # verificamos este caso Art.235-GÉjhuhhujiji.
						return puntoSp[1].strip().replace('-','')
					else:
						return clean_nro_art(puntoSp,1)							
				else:
					return None 	

		if len(puntoSp)	== 2: #Art554.Destitui  O tambien Art.1ºEstaConso
			if len(re.findall(r'\d+', puntoSp[1])) == 0 :# no hay numeros 
				return clean_nro_art(puntoSp,0)

			else: # si tine numero y puede tener guion 
				guionArt = puntoSp[1].split('-')
				if len(guionArt) == 1: #1ºEstaConso
					return clean_nro_art(guionArt,0)

				if 	len(guionArt) == 2: #1ºA-EstaCon O tambien 360 - Toda 
					if guionArt[0] is not None or guionArt[0] == '':
						sanetizar = "".join(re.split("[^a-zA-Z]*", guionArt[0]))
						if sanetizar != '' and len(sanetizar) == 1 and 'A' <= sanetizar <= 'Z' : # verificamos este caso Art.235GÉjhuhhujiji-jjj.
							return guionArt[0].strip().replace('-','')
						else:
							return clean_nro_art(guionArt,0)				
					else:
						return None	
						
				if 	len(guionArt) >= 3:	#877-A-Écomp
					nro= clean_nro_art(guionArt,0)
					if nro is None:
						return None
					letra= guionArt[1]
					if nro is not None and nro !='' and letra is not None and letra !='' : 
						letra = letra.strip()
						sanetizar = "".join(re.split("[^a-zA-Z]*", letra))
						if sanetizar != '' and len(sanetizar) == 1 and 'A' <= sanetizar <= 'Z':
							return nro + letra
						else:
							return nro.strip()	 
					else:
						return None 

		if len(puntoSp)	== 1: #	Art554Destitui	 o tambien art 
			return clean_nro_art(puntoSp,0)
	else:
		return None			

			
def stringNotNoneOrEmpty(cadena):
	if cadena is not None and cadena != '':
		return True
	return False
		
def getArticuleUnderscoreGroup(actual_articule,last_articule,number_article):
	if not stringNotNoneOrEmpty(actual_articule):
		return [None,last_articule,number_article]# no recibio bien el articulo actual
	if last_articule == '' or actual_articule != last_articule:
		return [actual_articule,actual_articule,1]# retorna el mismo articulo porque aun no ha encontrado otro articulo o es un nuevo articulo
	if actual_articule == last_articule:
		number_article = number_article + 1
		new_articule = actual_articule+'-'+str(number_article)
		last_articule = actual_articule
		return [new_articule,last_articule,number_article]


def number_repeated(art_act,art_ant,padre_art_ant,indice_art):
	if art_act == art_ant:
	   if art_ant != padre_art_ant:
	   		indice_art=0
	   padre_art_ant=art_ant
	   indice_art=indice_art+1
	   newidArt=art_ant+'-'+str(indice_art)
	   art_ant=art_act	
	   return[newidArt,art_ant,padre_art_ant,indice_art]			
	
	elif art_ant == padre_art_ant:
		 indice_art=indice_art+1
		 newidArt=art_ant+'-'+str(indice_art)
		 padre_art_ant=art_ant
		 art_ant=art_act
		 return[newidArt,art_ant,padre_art_ant,indice_art]
	else:
		padre_art_ant=art_ant
		art_ant=art_act
		indice_art=0
		return[None,art_ant,padre_art_ant,indice_art]

def new_id_articulo(newId,idreplace,identificador_art):
	if newId is not None:
		return identificador_art.replace(idreplace.encode('utf-8','ignore'),newId.encode('utf-8','ignore'))
	return identificador_art	
def get_size_page(request):
	header=request.headers
	size=header.get('Content-Length')
	if size is not None:
		return float(size)
	else:
		print 'Esta ley no tiene tamanio..'
		c=int(input('continuar'))	

def get_idLegislacion_url(url_ley):
	if url_ley != '':		
		url_titu=url_ley
		part_titu=url_titu.split('/')[-1]
		ley_titu=part_titu.split('#')[0]
		return ley_titu
	print 'url_id_legislacion vacia' 	
	return 'url_id_legislacion_vacia'	

def is_h_and_parent_body(soup):
	if soup is not None:		
		if soup.name == 'h1' and soup.find_parent().name == 'body':
			return True
		elif soup.name == 'h2' and soup.find_parent().name == 'body':
			return True
		elif soup.name == 'h3' and soup.find_parent().name == 'body' or soup.find_parent().name == 'texto':
			return True
	return False				

def is_h_123(soup):
	if soup is not None:
		if soup.name == 'h1':
			return True 
		if soup.name == 'h2':
			return True 
		if soup.name == 'h3':
			return True
	return False		 						

def set_href_a(soup_p):
	if soup_p is not None:
		size=len(soup_p.find_all('a'))
		if size > 0:
			i=0
			while i < size:
				try:
					if soup_p.findAll('a')[i].get('href') is not None:
						value_href=soup_p.findAll('a')[i]['href']
						soup_p.findAll('a')[i]['href']=get_new_value_href(value_href)#obtenemos y seteamos nuevo valor
					i=i+1	
				except Exception ,e:
					print 'metodo set_href_a ,no contiene href ',soup_p
	return soup_p			
						
def get_new_value_href(value_href):	
	url_split=value_href.split('/')
	ultimo_url=url_split[len(url_split)-1]#/L12462.htm#art9. 
	if isURL_relative(value_href):	
		return cod_uniq_or_ancla(ultimo_url,value_href)
	ley_ext=is_ley_externa(ultimo_url,value_href)
	if ley_ext	== None: #entonces es ley Externa
		return 'target:_blank'
	return ley_ext

def this_part_url_is_codigoLey(partUrl):
	arrUrl=partUrl.split('.')
	if len(arrUrl)>1:
		if 'htm' in arrUrl[1]:
			return True
	return False

def get_encoding_ley_exeption(partUrl,arrayParte,index):
	partUrl=partUrl.strip()	
	if partUrl == 'Mpv': #que pertenece a Tabla1 con codificacion MPV
		return 'MPV'
	if partUrl == 'mpv': # mpv que pertenece a Tabla1 ley antiguas con codificacion MPV
		return 'MPV'		
	elif partUrl == 'MPV':	#que pertenece a Tabla2 con codificacion MV
		return 'MV'
	elif partUrl == '1937-1946': #codificacion decreto-ley tabla1 (o fila1)
		return 'DEL'	
	elif partUrl == '1965-1988' or partUrl == 'Decreto-Lei':#codificacion decreto-ley tabla2(o fila2)
		if this_part_url_is_codigoLey(arrayParte[index+1]):
			return 'DL'	
	return None		


			 
def search_in_url_exception(arrPartUrl):
	if arrPartUrl is not None:		
		size_arr=len(arrPartUrl)
		i=0
		while i < size_arr:
			part=arrPartUrl[i]
			encoding_ley=get_encoding_ley_exeption(part,arrPartUrl,i)
			if encoding_ley is not None:
				return encoding_ley
			i=i+1					

	return None	
def build_code_excetion(cod_ley,encodingAct,encodingExcep):
	if encodingAct == '':
		return encodingExcep+cod_ley
	return cod_ley.replace(encodingAct,encodingExcep)

def is_cod_ley_exception(encoding):
	print 'Codigo',encoding	
	if encoding == '':
		return True
	elif encoding.strip() == 'mpv':
		return True
	elif encoding.strip() == 'Del':
		return True		

		
def encode_if_exception(cod_ley,value_href):	
	if cod_ley == 'Del5452compilado':
		return cod_ley #esta no se debe codificar 
	encoding=re.split('[0-9]',cod_ley)[0]	
	if is_cod_ley_exception(encoding):
		if len(value_href.split('/')) > 1:#entonces es codigo desde otra pagina
			cod_resul=search_in_url_exception(value_href.split('/'))
			if cod_resul is not None:
				#codificamos y armamos el codigo
				return build_code_excetion(cod_ley,encoding,cod_resul)
			else:
				return cod_ley #retornamos el mismo codigo por a hora 

		else:# el codigo es local tenemos que validar con la url de esta pagina que estamos mirando
			url_page_act=params.url
			arr_url=url_page_act.split('/')
			cod_resul=search_in_url_exception(arr_url)
			if cod_resul is not None:
				#codificamos y armamos el codigo
				return build_code_excetion(cod_ley,encoding,cod_resul)
			else:
				return cod_ley #retornamos el mismo codigo por a hora 
	return cod_ley
	

def cod_uniq_or_ancla(cod_ley,value_href):
	arrSpli=cod_ley.split('#') #[L12462.htm][art9.]
	if len(arrSpli) > 1:#entonces tiene ancla 
		splitLey=arrSpli[0] #[L12462.htm]
		codigoLey=splitLey.split('.')
		codigoLey=codigoLey[0].replace('.','')
		cod_new=encode_if_exception(codigoLey,value_href)# esta parte hacer para despues para la codificacion de las leyes exception
		return cod_new+'#'+arrSpli[1]
	elif len(arrSpli) == 1: #es ley unicac 'codley.htm'
		cod_ley=cod_ley.split('.')[0] #L5512.html-->L5512
		verify_cod=cod_ley.replace('.','')
		return encode_if_exception(verify_cod,value_href) # esto en el caso de que el codigo contenga punto al medio

#verificar si es una ley externa o es Ley decoreba 
def is_ley_externa(cod_ley,value_href):
	arrSpli=cod_ley.split('#') #[L12462.htm][art9.]
	if len(arrSpli) > 1:#entonces tiene ancla 
		splitLey=arrSpli[0] 
		codigoLey=splitLey.split('.') #[L12462.htm]
		if len(codigoLey)>1:
			if codigoLey[1] in "html":
				codigoLey=codigoLey[0].replace('.','')
				cod_new=encode_if_exception(codigoLey,value_href)
				return cod_new+'#'+arrSpli[1]
			return None	
		return None		
	elif len(arrSpli) == 1: #es ley unicac 'codley.htm'
		cod_ley=cod_ley.split('.') #[L5512][html]
		if len(cod_ley) > 1:
			if cod_ley[1] in 'html':
				cod_new=encode_if_exception(cod_ley[0].replace('.',''),value_href)
				return cod_new
		return None		
# se va a encargar de colocar los link como deven ser en decoreba 
def set_link_segmento(contenido):
	if contenido is not None:
		new_soup=BeautifulSoup(contenido,'html.parser')
		if len(new_soup.find_all('a')) > 0:#entonces tenemos enlaces
		 	i=0
		 	size_a=len(new_soup.find_all('a'))
		 	while i < size_a:
		 		content_href=new_soup.find_all('a')[i].get('href')
		 		if content_href is not None:
		 			newHref=get_new_value_href(content_href)
		 			if 'target:_blank' == newHref:
		 				atrib_valu=newHref.split(':')
		 				new_soup.find_all('a')[i][atrib_valu[0]]=atrib_valu[1]
		 			else:	
		 				new_soup.find_all('a')[i]['href']=newHref
		 		i=i+1
		 	return new_soup	
		return contenido 		
	else:
		return 'contenido Vacio verificar codfigo set_link_segmento (contenido)'	


def is_texto_compilado(tag):
	if tag is not None:
		if tag.getText()!= '':		
			textCons=tag.getText().replace('\n','').replace(' ','')			
			if tag.getText().strip() in 'Texto compilado':
				return True
			if textCons.strip() in "Textocompilado":	
				return True	
	return False			

#metodo para saber cuantos '..' tiene una cadena
def cant_retrocesos_directorio(url):
	i=0
	mini_url=url.split('/')
	for ele in mini_url:
		if ele == '..':
			i = i + 1
	return i

def url_retrocesos_directorio(url,i):
	i=i+1
	ultimo_directorio_saltado=url.split('/')[-i]
	return url.split('/'+ultimo_directorio_saltado)[0]

def url_relativa_sin_retroceso(url):
	return url.split('.')[-2]+'.htm'

def build_url_absolute_MVP(url_base,url_relativa):
	retrocesos=cant_retrocesos_directorio(url_relativa)
	url_new_base=url_retrocesos_directorio(url_base,retrocesos)
	url_new_relativa=url_relativa_sin_retroceso(url_relativa)
	return url_new_base+url_new_relativa

	