# -*- coding: latin-1 -*-

import os.path, sys
from bs4 import BeautifulSoup
import hard_code_util
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import dao.segmentoDAO
import dao.leyDAO
import logger
import params
import scraper

## CREATED:Rudy villagomez 
## MAIL	  :villagomezzr@gmail.com

ley_id = 0
last_parte_id = 0
last_libro_id = 0
last_titulo_id = 0
last_subtitulo_id = 0
last_capitulo_id = 0
last_seccion_id = 0
last_subseccion_id = 0
last_segmento_id = 0
start_articles = False
end_of_code = ''

last_parte = ''
last_libro = ''
last_titulo = ''
last_subtitulo = ''
last_capitulo = ''
last_seccion = ''
last_subseccion = ''

idnetificador_articulo = ''
articulo_completo = ''
id_parent_articulo = 0
titulo_de_ley=''
contFooter=0
fin_del_codigo=False

art_anterior='' #este sirve para verificar si estan repitiendo los articulos 
art_actual=''
indice_art=0
primr_coinciden=True
padre_art_ant=''

urlLeyTextoCompilado=''
cont194=0


def restartVar():
	global ley_id,titulo_de_ley,padre_art_ant,primr_coinciden,art_actual,indice_art,art_anterior,fin_del_codigo,contFooter, last_parte_id, last_libro_id, last_titulo_id, last_subtitulo_id, last_capitulo_id, last_seccion_id, last_subseccion_id, last_segmento_id, start_articles, end_of_code, last_parte, last_libro, last_titulo, last_subtitulo, last_capitulo, last_seccion, last_subseccion, articulo_completo, idnetificador_articulo, id_parent_articulo

	ley_id = 0
	last_parte_id = 0
	last_libro_id = 0
	last_titulo_id = 0
	last_subtitulo_id = 0
	last_capitulo_id = 0
	last_seccion_id = 0
	last_subseccion_id = 0
	last_segmento_id = 0
	start_articles = False
	end_of_code = ''

	last_parte = ''
	last_libro = ''
	last_titulo = ''
	last_subtitulo = ''
	last_capitulo = ''
	last_seccion = ''
	last_subseccion = ''

	idnetificador_articulo = ''
	articulo_completo = ''
	id_parent_articulo = 0
	titulo_de_ley=''
	contFooter=0
	fin_del_codigo=False
	hard_code_util.arbolArray=[None,None,None,None,None,None,None,None,None]
	art_anterior=''
	indice_art=0
	art_actual=''
	primr_coinciden=True
	padre_art_ant=''

def check_is_title(attrs,soup):
	if attrs is not None:
		if 'align' in attrs:
			return attrs['align'].lower() == 'center'
		#aumentando el caso en que tiene style='text-align:center'
		if 'style' in attrs:
		    style=attrs['style']
		    #print ('/////////array style //////////',style)
		    styValu=style.split(';')
		    if styValu is not None and len(styValu)>0:
		    	for itemSty in styValu:
		    		if 'text-align:center' == itemSty.strip().lower() or 'text-align: center' == itemSty.strip().lower():
		    			return True
		#caso para los Titulos Capitulos  tag h3
		if 'style' in attrs and soup.name=='h3':
		    style=attrs['style']
		    #print ('/////////array style //////////',style)
		    styValu=style.split(';')
		    if styValu is not None and len(styValu)>0:
		    	for itemSty in styValu:
		    		if 'text-indent:1cm' == itemSty.strip().lower() or 'text-indent: 1cm' == itemSty.strip().lower() or 'margin-bottom:0' == itemSty.strip().lower():
		    			return True	
	return False	    			

def __isTitulo(soup):
	if soup is not None:
		attrs = soup.attrs
		#print '<<<<<< # VERIFICANDO ES-SEGMENTO-TITULO # >>>>>>>>'
		#print ('/////////atributo//////////',attrs)
		if soup.p is not None:		
			attrs = soup.p.attrs
		#caso para no repetir titulos que estan dentro de una lista		
		if soup.name=='p' and  soup.findParent().name=='li': #caso en que p-->padre-->li
			return False	
		if soup.p is not None:	
			#print 'lista p',soup.p
			#print 'lista p--padre',soup.p.findParent().name
			#v=int(input('contii'))		
			#import pdb;pdb.set_trace()			
			if soup.name=='li':
				return check_is_title(soup.p.attrs,soup)				
		#aumentando caso pra los titulos con etiquetas center con contenido font
		if soup is not None and soup.name == 'font' and hard_code_util.isParent_center_body(soup):
			return True
		if	soup is not None and soup.name == 'font' and hard_code_util.isParent_p_center_body(soup):
			return True

		#print '<<<<este tiene que ser una p>>>',soup		
		#import pdb;pdb.set_trace()
		return check_is_title(attrs,soup)  #verificar si es titulo  		

	return False

def get_part_restante_titulo(soup_titulo):
	#return soup_titulo # quitar esto luego de hacer las prubas (para algunas ley este codigo afecta parece)
	if soup_titulo is not None:
		next_p=soup_titulo.find_next(str(soup_titulo.name))
		newTitulo=''
		if next_p is not None and __isTitulo(next_p) and not hard_code_util.isItemTree(next_p.text):
			newTitulo=str(soup_titulo)+str(next_p)
		next_p2=next_p.find_next(str(next_p.name))	
		if next_p2 is not None and __isTitulo(next_p2) and not hard_code_util.isItemTree(next_p2.text):
			newTitulo+=str(next_p2)	
		if newTitulo != '':
			return newTitulo
		else:
			return soup_titulo		

def get_url_texto_compilado(table_soup,url_ley):
	global urlLeyTextoCompilado
	#print 'table soup',str(table_soup)
	if table_soup is not None:
		arr_a_tab=table_soup.find_all('a')
		#print 'arreglo de tag a de la table',str(arr_a_tab)
		if len(arr_a_tab)>0:
			for tag_a in arr_a_tab:
				if hard_code_util.is_texto_compilado(tag_a):
					if tag_a.get('href') is not None:
						urlTexCompi=tag_a.get('href')
						#print 'url compilada',urlTexCompi
						urlLeyTextoCompilado=hard_code_util.build_url_absolute(url_ley,urlTexCompi)
						print 'url compilada completa',urlLeyTextoCompilado
						return urlLeyTextoCompilado	
	urlLeyTextoCompilado=''	

def exist_ley_TextCompilado():
	#import pdb;pdb.set_trace()
	global urlLeyTextoCompilado
	if urlLeyTextoCompilado != '':
		#print 'url compilada completa',urlLeyTextoCompilado
		params.url=urlLeyTextoCompilado
		#print 'url parametro',params.url
		scraper.iniciarScraping(urlLeyTextoCompilado)
		urlLeyTextoCompilado=''
					

''' Metodo principal para cada parrafo (p) a procesar '''
def __procesarParrafo(soup):
	global ley_id,cont194,titulo_de_ley,padre_art_ant,primr_coinciden,art_anterior,art_actual,indice_art,fin_del_codigo,contFooter, last_parte_id, last_libro_id, last_titulo_id, last_subtitulo_id, last_capitulo_id, last_seccion_id, last_subseccion_id, last_segmento_id, start_articles, end_of_code, last_parte, last_libro, last_titulo, last_subtitulo, last_capitulo, last_seccion, last_subseccion, articulo_completo, idnetificador_articulo, id_parent_articulo
	if (__isTitulo(soup)):
		
		#implementando la funcion es item del arbol para verificar si es titulo,capitu,parte,etc 
		if articulo_completo != '':
			if not  hard_code_util.isItemTree(soup.text):
				articulo_completo += str(soup)
			else:
				arr_repead=hard_code_util.number_repeated(art_actual,art_anterior,padre_art_ant,indice_art)								
				art_anterior=arr_repead[1]
				padre_art_ant=arr_repead[2]
				indice_art=arr_repead[3]
				idnetificador_articulo=hard_code_util.new_id_articulo(arr_repead[0],padre_art_ant,idnetificador_articulo)

				dao.segmentoDAO.insert(articulo_completo, dao.segmentoDAO.TIPO_ARTICULO, ley_id, id_parent_articulo, idnetificador_articulo)
				print '<<<<<< # ARTICULO INSERTADO  # >>>>>>>>'
				#print '****************insertando articulo ********************'
				#print articulo_completo					
				idnetificador_articulo = '' #luego quitar esto para guiarnos en los elementos que se insertan por separado como articulos
				articulo_completo = ''


		numeracion = hard_code_util.getNumeroTitular1(soup.text)
		if hard_code_util.isParte(soup.text):
			last_libro = last_titulo = last_subtitulo = last_capitulo = last_seccion = last_subseccion = ''
			last_parte = numeracion
			start_articles = False
			#añadir al arbolArray y obtener idPadre y caminoIdentificador
			pos=hard_code_util.POS_PARTE
			identifi='parteGeral'+str(last_parte)
			id=0
			nodo=hard_code_util.addTree(id,identifi,pos)
			id_padre=nodo[0]
			caminoIdentifi=nodo[1]
			soup=get_part_restante_titulo(soup) # para obtener la parte restante del titulo			
			last_segmento_id = last_parte_id = dao.segmentoDAO.insert(str(soup), dao.segmentoDAO.TIPO_PARTE, ley_id, id_padre, caminoIdentifi)
			print '<<<<<< # PARTE-GENERAL INSERTADA  # >>>>>>>>'
			#actualizar id del nodo insertado
			hard_code_util.actualizarIdNodo(last_parte_id,pos)
			

		elif hard_code_util.isLibro(soup.text):
			last_titulo = last_subtitulo = last_capitulo = last_seccion = last_subseccion = ''
			last_libro = numeracion
			start_articles = False

			#añadir al arbolArray y obtener idPadre y caminoIdentificador
			pos=hard_code_util.POS_LIBRO
			identifi='livro'+str(last_libro)
			id=0
			nodo=hard_code_util.addTree(id,identifi,pos)
			id_padre=nodo[0]
			caminoIdentifi=nodo[1]
			soup=get_part_restante_titulo(soup) # para obtener la parte restante del titulo
			last_segmento_id = last_libro_id = dao.segmentoDAO.insert(str(soup), dao.segmentoDAO.TIPO_LIBRO, ley_id, id_padre,caminoIdentifi)
			print '<<<<<< # LIBRO INSERTADO  # >>>>>>>>'
			#actualizar id del nodo insertado
			hard_code_util.actualizarIdNodo(last_libro_id,pos)

		elif hard_code_util.isSubTitulo(soup.text):
			last_capitulo = last_seccion = last_subseccion = ''
			last_subtitulo = numeracion
			start_articles = False
			
			#añadir al arbolArray y obtener idPadre y caminoIdentificador
			pos=hard_code_util.POS_SUBTITULO
			identifi='subTit'+str(last_subtitulo)
			id=0
			nodo=hard_code_util.addTree(id,identifi,pos)
			id_padre=nodo[0]
			caminoIdentifi=nodo[1]
			soup=get_part_restante_titulo(soup) # para obtener la parte restante del titulo
			last_segmento_id = last_subtitulo_id = dao.segmentoDAO.insert(str(soup), dao.segmentoDAO.TIPO_SUBTITULO, ley_id, id_padre,caminoIdentifi)
			print '<<<<<< # SUB-TITULO INSERTADO  # >>>>>>>>'
			#actualizar id del nodo insertado
			hard_code_util.actualizarIdNodo(last_subtitulo_id,pos)			

		elif hard_code_util.isTitulo(soup.text):
			last_subtitulo = last_capitulo = last_seccion = last_subseccion = ''
			last_titulo = numeracion
			start_articles = False

			#añadir al arbolArray y obtener idPadre y caminoIdentificador
			pos=hard_code_util.POS_TITULO
			identifi='tit'+str(last_titulo)
			id=0
			nodo=hard_code_util.addTree(id,identifi,pos)
			id_padre=nodo[0]
			caminoIdentifi=nodo[1]
			soup=get_part_restante_titulo(soup) # para obtener la parte restante del titulo
			last_segmento_id = last_titulo_id = dao.segmentoDAO.insert(str(soup), dao.segmentoDAO.TIPO_TITULO, ley_id, id_padre,caminoIdentifi)
			print '<<<<<< # TITULO INSERTADO  # >>>>>>>>'
			#actualizar id del nodo insertado
			hard_code_util.actualizarIdNodo(last_titulo_id,pos)
			hard_code_util.clear_camino_identifi(pos)	#limpiamos el camino identificador para que no haya inconsistencia		


		elif hard_code_util.isCapitulo(soup.text):
			last_seccion = last_subseccion = ''
			last_capitulo = numeracion
			start_articles = False
			
			#añadir al arbolArray y obtener idPadre y caminoIdentificador
			pos=hard_code_util.POS_CAPITULO
			identifi='cap'+str(last_capitulo)
			id=0
			nodo=hard_code_util.addTree(id,identifi,pos)
			id_padre=nodo[0]
			caminoIdentifi=nodo[1]	
			soup=get_part_restante_titulo(soup) # para obtener la parte restante del titulo
			last_segmento_id = last_capitulo_id = dao.segmentoDAO.insert(str(soup), dao.segmentoDAO.TIPO_CAPITULO, ley_id, id_padre, caminoIdentifi)
			print '<<<<<< # CAPITULO INSERTADO  # >>>>>>>>'
			#actualizar id del nodo insertado
			hard_code_util.actualizarIdNodo(last_capitulo_id,pos)
			hard_code_util.clear_camino_identifi(pos)	#limpiamos el camino identificador para que no haya inconsistencia	

		elif hard_code_util.isSeccion(soup.text):
			last_subseccion = ''
			last_seccion = numeracion
			start_articles = False
			
			#añadir al arbolArray y obtener idPadre y caminoIdentificador
			pos=hard_code_util.POS_SECCION
			identifi='secao'+str(last_seccion)
			id=0
			nodo=hard_code_util.addTree(id,identifi,pos)
			id_padre=nodo[0]
			caminoIdentifi=nodo[1]	
			soup=get_part_restante_titulo(soup) # para obtener la parte restante del titulo
			last_segmento_id = last_seccion_id = dao.segmentoDAO.insert(str(soup), dao.segmentoDAO.TIPO_SECCION, ley_id, id_padre, caminoIdentifi)
			print '<<<<<< # SECCION INSERTADA  # >>>>>>>>'
			#actualizar id del nodo insertado
			hard_code_util.actualizarIdNodo(last_seccion_id,pos)
			hard_code_util.clear_camino_identifi(pos)	#limpiamos el camino identificador para que no haya inconsistencia



		elif hard_code_util.isSubSeccion(soup.text):
			last_subseccion = numeracion
			start_articles = False

			#añadir al arbolArray y obtener idPadre y caminoIdentificador
			pos=hard_code_util.POS_SECCION
			identifi='subSecao'+str(last_seccion)
			id=0
			nodo=hard_code_util.addTree(id,identifi,pos)
			id_padre=nodo[0]
			caminoIdentifi=nodo[1]	
			soup=get_part_restante_titulo(soup) # para obtener la parte restante del titulo
			last_segmento_id = last_subseccion_id = dao.segmentoDAO.insert(str(soup), dao.segmentoDAO.TIPO_SUBSECCION, ley_id, id_padre, caminoIdentifi)
			print '<<<<<< # SUB-SECCION INSERTADA  # >>>>>>>>'
			#actualizar id del nodo insertado
			hard_code_util.actualizarIdNodo(last_subseccion_id,pos)
		#saque el caso de reconocer anexo probocava error	


	else:
		if hard_code_util.isArticulo(soup.text):

			nroArt=hard_code_util.getNumeroArticulo(soup.text)
			art_actual=nroArt
			# print '-----------------texto nro aticulo normal fuera if  -------------------------'
			# print(soup.text)
			# print '-----------------nro  if  -------------------------'
			# print(nroArt)
			# print '-----------------nro sanetizado  if  -------------------------'
			# nroArt=hard_code_util.clean_id_arti(nroArt)
			# print(nroArt)
			# print '-----------------string arry split   -------------------------'
			# print(soup.text.split())
			# print '========================delete all space   =============================='
			newArtc = ''.join(filter(None,soup.text.split(' ')))
			newArtc = newArtc.replace('\n','')

			newArtc = newArtc[0:20]#antes :50
			newArtc = ''.join(filter(None,newArtc.split(' ')))
			newArtc = newArtc.replace('\n','')
						
			# print(newArtc)

			# print '==========================ARTIULO NUEVO=============================================='

			# arryArt = newArtc.split('.')
			# if arryArt[1] is not None and arryArt[1] != '':
			# 	nroArt = hard_code_util.get_clean_article(arryArt,1)
			# else:
			# 	nroArt = hard_code_util.get_clean_article(arryArt,2)

			# print '*************** este es el numreo *********************'
			nroArt = hard_code_util.get_clean_article(newArtc)
			# print nroArt
			if nroArt == None :
				# import pdb; pdb.set_trace()
				# print newArtc
				nroArt = ''
				details = 'Exection Article :|'+ newArtc + ' | idLey : |' + str(ley_id)+ '| url: '+params.url
				logger.info(details)




			#print 'NUMERO DEL ARTICULO ',nroArt
			##PARA HACER DEBUG ESPECIAL
			#j=int(input('continuar numero articulo'))
			# if nroArt == '194':
			# if '194' in nroArt:
			# 	cont194 = cont194 + 1
			# 	import pdb; pdb.set_trace()
			# 	#print '-----------------texto nro aticulo normal -------------------------'
			# 	#print(soup.text)
			# 	#print '--------------luego de sanetizado ----------------------------'
			# 	#print(nroArt)
			# 	#print '------------------------------------------'
			# if cont194 >= 2 :
			# 	import pdb; pdb.set_trace()

			#añadir al arbolArray y obtener idPadre y caminoIdentificador
			pos=hard_code_util.POS_ARTICULO
			identifi='artigo'+nroArt
			id=0
			nodo=hard_code_util.addTree(id,identifi,pos)
			id_padre=nodo[0]
			caminoIdentifi=nodo[1]

			if articulo_completo != '':
				arr_repead=hard_code_util.number_repeated(art_actual,art_anterior,padre_art_ant,indice_art)								
				art_anterior=arr_repead[1]
				padre_art_ant=arr_repead[2]
				indice_art=arr_repead[3]
				idnetificador_articulo=hard_code_util.new_id_articulo(arr_repead[0],padre_art_ant,idnetificador_articulo)
				dao.segmentoDAO.insert(articulo_completo, dao.segmentoDAO.TIPO_ARTICULO, ley_id, id_parent_articulo, idnetificador_articulo)
				print '<<<<<< # ARTICULO INSERTADO  # >>>>>>>>'
				#id_parent_articulo = id_parent
			art_anterior=nroArt	
			id_parent_articulo = id_padre
			idnetificador_articulo = caminoIdentifi
			articulo_completo = str(soup)
			start_articles = True
		elif start_articles:
			if hard_code_util.startEndConstitucion(soup.text) or len(end_of_code) > 0:
				print 'TAMAÑO FOOTER ',len(end_of_code)
				print '<<<<<< # INICIANDO CAPTURA DEL FOOTER  # >>>>>>>>'
				#j=int(input('validando cantidad footer '))

				if titulo_de_ley != 'DEL5452' and titulo_de_ley != 'd3048compilado' and titulo_de_ley != 'Del5452compilado' and  titulo_de_ley != 'Del5452':	#esta es una solucion momentanea al problema de footer con esta ley aparece al comienzo el identificador				
					print 'TITULO_DE_LEY',titulo_de_ley
					#print '//***footer//***' ,str(soup)
					#j=int(input('dentro del footer original '))
					#import pdb;pdb.set_trace()
					fin_del_codigo=True
					#print 'CONTENIDO DEL FOOTER',soup					
					while soup is not None:	
						#print 'CONTENIDO DEL FOOTER',soup					
						if soup.name == 'div':
							end_of_code += str(soup)
						elif soup.name == 'table' and soup.find_parent().name != 'div':
							end_of_code += str(soup)	
						elif soup.name == 'p'  and not hard_code_util.isParent_table_tr_td(soup):
							end_of_code += str(soup)
						soup=soup.find_next()

				else:
					contFooter=contFooter+1
					print 'INCREMENTANDO EL CONTADOR',contFooter
					#j=int(input('FOOTER DOS  '))
					if contFooter > 1:
						#print'NOMOBRE PADRE TAG', (soup.find_parent()).name
						#j=int(input('FOOTER DOS DENTRO  '))
						fin_del_codigo=True
						while soup is not None:							
							if soup.name == 'div':
								end_of_code += str(soup)
							elif soup.name == 'table' and soup.find_parent().name != 'div':
								end_of_code += str(soup)									
							elif soup.name == 'p' and not hard_code_util.isParent_table_tr_td(soup):
								#print 'PADRE DE P',(soup.find_parent()).name
								#j=int(input('PADRE P  '))
								end_of_code += str(soup)
							soup=soup.find_next()	

																

			else:
				if not __isTitulo(soup):
					articulo_completo += str(soup)

def procesarLegislacion(soup,url_ley,codigo_ley,size_ley,alias):
	try:
		global ley_id, end_of_code,articulo_completo,titulo_de_ley,fin_del_codigo,art_anterior,art_actual,padre_art_ant,indice_art,idnetificador_articulo
		restartVar()
		print '<<<<<< # iniciando insertar titulo # >>>>>>>>'	
		tituloLey=hard_code_util.obtenerTituloLey(soup)			
		if tituloLey is not None: #verificamos si tiene titulo es por que existe ley  		

			titulo_de_ley=codigo_ley
			## insertando primer segmeto y la ley
			ley_id = dao.segmentoDAO.insert(tituloLey, dao.segmentoDAO.TIPO_TITULO_LEY, None, None, 'norma')
			## añadir nodo raiz al arbolArray
			posi=hard_code_util.POS_TITULO_LEY		
			hard_code_util.addTree(ley_id,'norma',posi)

			#logger.info('Segmento - Ley registrada correctamente, ID = ' + str(ley_id))
			dao.leyDAO.insert_con_codLey(tituloLey, url_ley, ley_id, datetime.now(), hard_code_util.ID_LEGISLACION,codigo_ley,size_ley,alias)
			print '<<<<<< # Ley registrada correctamente # >>>>>>>>'
			#logger.info('Ley registrada correctamente')

			##verificando e insertando header
			contHead=hard_code_util.obtenerHeader(soup) 
			if contHead  is not None:
				#print(str(contHead))
				id_header = dao.segmentoDAO.insert(str(contHead), dao.segmentoDAO.TIPO_HEADER, ley_id, ley_id, 'cabecalho')
				print '<<<<<< # HEADER registrado # >>>>>>>>'
				pos=hard_code_util.POS_HEADER
				hard_code_util.addTree(id_header,'cabecalho',pos)
				#import pdb;pdb.set_trace()
				get_url_texto_compilado(contHead,url_ley)

			#titulo = soup.find('p', {'style': 'text-indent: 30px'})
			next =soup.find('font', {'color': '#000080'})
			next =next.find_next('p')
			#next =next.find_next()
			
			#print (str(next))	
			print '<<<<# Bandera-Fin-codigo #>>>>',fin_del_codigo
			#import pdb;pdb.set_trace()
			print '=============================================================================================================================================================='	
			print '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< # INICIANDO A PROCESAR LEY .......... # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
			print '=============================================================================================================================================================='	
			while next is not None and not fin_del_codigo:
				#print '####Tag nombre#### ',next.name
				#print '******contenido****',next
				#if next.name == 'p' and  not hard_code_util.isParent_table(next):
				if next.name == 'p' and  not hard_code_util.isParent_table_tr_td(next):
					#padre=next.find_parent()
					#if padre.name != 'p':    #este caso se dio por que ocurre una inconsistencia dentro de una tabla y aparece la p como  si su padre 
					#	__procesarParrafo(next) # fuese otra p y esta esta dentro de la tabla 
					#else:
					#	print 'NO ENTRO NO ENTRO'	
					__procesarParrafo(next)	
					
				elif next.name == 'div' and 'align' in next.attrs and next.attrs['align'] == 'center'  and start_articles:
					#print '***div****',str(next)
					#print '****startArt*****',start_articles
					#print 'articuloCOmp',articulo_completo
					#import pdb;pdb.set_trace()
					#d=int(input('pres continu'))
					articulo_completo += str(next)
				elif next.name == 'center'and (next.find_parent()).name == '[document]' and len(next.find_all('table'))==0 : 
					padre=next.find_parent()
					#print 'Padre centere', str(padre.name)
					#c=int(input('este el center titulo'))
					arrFont=next.find_all('font')
					if len(arrFont) > 0:
						for eleFont in arrFont:
							__procesarParrafo(eleFont)
				elif next.name == 'center'and (next.find_parent()).name == '[document]' and len(next.find_all('table')) > 0 and start_articles :
					#print '***CENTER TABLA ****',str(next)
					#print '****startArt*****',start_articles
					#print 'articuloCOmp',articulo_completo
					#d=int(input('pres continu'))
					articulo_completo += str(next)

				#caso para controlar listas en div 
				elif next.name == 'li':
					#print '####Lista li ',next
					#i=int(input('verificando Lista conti..'))
					__procesarParrafo(next)
				#caso para controlar h1 h2 que son Titulos 	
				elif hard_code_util.is_h_and_parent_body(next):	
					#import pdb;pdb.set_trace()
					__procesarParrafo(next)						

				next=next.find_next()

			if articulo_completo != '' and start_articles:

				arr_repead=hard_code_util.number_repeated(art_actual,art_anterior,padre_art_ant,indice_art)								
				art_anterior=arr_repead[1]
				padre_art_ant=arr_repead[2]
				indice_art=arr_repead[3]
				idnetificador_articulo=hard_code_util.new_id_articulo(arr_repead[0],padre_art_ant,idnetificador_articulo)
				
				dao.segmentoDAO.insert(articulo_completo, dao.segmentoDAO.TIPO_ARTICULO, ley_id, id_parent_articulo, idnetificador_articulo)
			#verificamos si existe footer para insertarlo	
			if len(end_of_code) > 0: # si hay footer			
				id_footer = dao.segmentoDAO.insert(end_of_code, dao.segmentoDAO.TIPO_FOOTER, ley_id, ley_id,'rodape')
				print '<<<<<< # FOOTER REGISTRADO # >>>>>>>>'
				fin_del_codigo=False #reiniciamos la bandera
				end_of_code='' #este colar a vacio	
			#reseteamos todo al finalizar para enpezar todo limpio
			#restartVar()
			print '<<<<<< # VERIFICANDO EXISTE TEXTO-COMPILADO # >>>>>>>>'
			exist_ley_TextCompilado()	
			print '<<<<<< # LEY PROCESADA CON EXITO  # >>>>>>>>'
			print '===================================================================================================================================================================='	
			print '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< # FIN LEY -->(A LA ESPERA DE LEY).............. # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
			print '====================================================================================================================================================================='

	except Exception, e:
		#logger.error('Error general : ' + str(e))
		raise