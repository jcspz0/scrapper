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
last_titulo_id = 0
last_capitulo_id = 0
last_seccion_id = 0
last_subseccion_id = 0
last_segmento_id = 0
last_articulo_id = 0
start_articles = False
end_of_code = ''

last_titulo = ''
last_capitulo = ''
last_seccion = ''
last_subseccion = ''
last_articulo = ''

idnetificador_articulo = ''
articulo_completo = ''
id_parent_articulo = 0

def __separarTituloCompuesto(soup):
	tags_a = soup.find_all(['a'])
	tags_name = []
	for item in tags_a:
		if item is not None and 'name' in item.attrs:
			print item.attrs, '\n'
			tags_name.append(item.attrs['name'])
		else:
			print 'ERROR, el tag no tiene un atributo nombre'
			return []
	if (len(tags_name) > 1):
		if tags_name[0] == 'tituloii' and tags_name[1] == 'tituloiicapituloi':
			# logger.info('Excepcion procesada : tituloii - tituloiicapituoi')
			tag1 = '<p align=\'center\'><font face=\'Arial\' size=\'2\'><a name=\'tituloii\'></a><span style=\'text-transform: uppercase\'><b>TÍTULO II<br>Dos Direitos e Garantias Fundamentais</b></span></font></p>'
			tag2 = '<p align=\'center\'><font face=\'Arial\' size=\'2\'><br><a name=\'tituloiicapituloi\'></a>CAPÍTULO I<br>DOS DIREITOS E DEVERES INDIVIDUAIS E COLETIVOS</font></p>'
			return [(BeautifulSoup(tag1.decode('utf-8'))).p, (BeautifulSoup(tag2.decode("utf-8"))).p]
		elif tags_name[0] == 'tituloiii' and tags_name[1] == 'tituloiiicapituloi':
			# logger.info('Excepcion procesada : tituloiii - tituloiiicapituloi')
			tag1 = '<p align="center"><font face="Arial" color="#000000" size="3"><a name="tituloiii"></a></font><font face="Arial" color="#000000" size="2"><span style="text-transform: uppercase"><b>TÍTULO III<br>Da Organização do Estado</b></span></font></p>'
			tag2 = '<p align="center"><font face="Arial" color="#000000" size="3"><br></font><font face="Arial" size="2"><a name="tituloiiicapituloi"></a>CAPÍTULO I<br>DA ORGANIZAÇÃO POLÍTICO-ADMINISTRATIVA</font></p>'
			return [(BeautifulSoup(tag1.decode('utf-8'))).p, (BeautifulSoup(tag2.decode("utf-8"))).p]
		elif tags_name[0] == 'tituloiiicapitulov' and tags_name[1] == 'tituloiiicapitulovsecaoi':
			# logger.info('Excepcion procesada : tituloiiicapitulov - tituloiiicapitulovsecaoi')
			tag1 = '<p align="CENTER"><font face="Arial" size="2"><a name="tituloiiicapitulov"></a>CAPÍTULO V<br>DO DISTRITO FEDERAL E DOS TERRITÓRIOS</font></p>'
			tag2 = '<p align="CENTER"><font face="Arial" size="2"><a name="tituloiiicapitulovsecaoi"></a><span style="text-transform: uppercase"><b>Seção I<br>DO DISTRITO FEDERAL</b></span></font></p>'
			return [(BeautifulSoup(tag1.decode('utf-8'))).p, (BeautifulSoup(tag2.decode("utf-8"))).p]
		elif tags_name[0] == 'tituloiiicapitulovii' and tags_name[1] == 'tituloiiicapituloviisecaoi':
			# logger.info('Excepcion procesada : tituloiiicapitulovii - tituloiiicapituloviisecaoi')
			tag1 = '<p align="CENTER"><font face="Arial" size="2"><a name="tituloiiicapitulovii"></a>CAPÍTULO VII<br>DA ADMINISTRAÇÃO PÚBLICA</font></p>'
			tag2 = '<p align="CENTER"><font face="Arial" size="2"><a name="tituloiiicapituloviisecaoi"></a><b><span style="text-transform: uppercase">Seção I<br>DISPOSIÇÕES GERAIS</span></b></font></p>'
			return [(BeautifulSoup(tag1.decode('utf-8'))).p, (BeautifulSoup(tag2.decode("utf-8"))).p]
		elif tags_name[0] == 'tituloiv' and tags_name[1] == 'tituloivcapituloi' and len(tags_name) == 3 and tags_name[2] == 'tituloivcapituloisecaoi':
			# logger.info('Excepcion procesada : tituloiv - tituloivcapituloi - tituloivcapituloisecaoi')
			tag1 = '<p align="center"><font size="2"><a name="tituloiv."></a><font face="Arial"><b><span style="text-transform: uppercase">TÍTULO IV<br>DA ORGANIZAÇÃO DOS PODERES</span></b></font><br><a href="http://www.planalto.gov.br/ccivil_03/Constituicao/Emendas/Emc/emc80.htm#art1">(Redação dada pela Emenda Constitucional nº 80, de 2014)</a></font></p>'
			tag2 = '<p align="center"><font face="Arial" size="2"><a name="tituloivcapituloi"></a>CAPÍTULO I<br>DO PODER LEGISLATIVO<br></font></p>'
			tag3 = '<p align="center"><font face="Arial" size="2"><a name="tituloivcapituloisecaoi"></a><b><span style="text-transform: uppercase">Seção I<br>DO CONGRESSO NACIONAL</span></b></font></p>'
			return [(BeautifulSoup(tag1.decode('utf-8'))).p, (BeautifulSoup(tag2.decode("utf-8"))).p, (BeautifulSoup(tag3.decode("utf-8"))).p]
		elif tags_name[0] == 'tituloivcapituloisecaoviii' and tags_name[1] == 'tituloivcapituloisecaoviiisubsecaoi':
			# logger.info('Excepcion procesada : tituloivcapituloisecaoviii - tituloivcapituloisecaoviiisubsecaoi')
			tag1 = '<p align="CENTER"><a name="tituloivcapituloisecaoviii"></a>&nbsp;<a name="sviii"></a><font face="Arial" size="2"><b><span style="text-transform: uppercase">Seção VIII<br>DO PROCESSO LEGISLATIVO</span></b></font></p>'
			tag2 = '<p align="CENTER"><a name="tituloivcapituloisecaoviiisubsecaoi"></a><b><span style="text-transform: uppercase">Subseção I<br>Disposição Geral</span></b></font></p>'
			return [(BeautifulSoup(tag1.decode('utf-8'))).p, (BeautifulSoup(tag2.decode("utf-8"))).p]
		elif tags_name[0] == 'tituloivcapituloii' and tags_name[1] == 'tituloivcapituloiisecaoi':
			# logger.info('Excepcion procesada : tituloivcapituloii - tituloivcapituloiisecaoi')
			tag1 = '<p align="CENTER"><font face="Arial" size="2"><a name="tituloivcapituloii"></a>CAPÍTULO II<br>DO PODER EXECUTIVO</font></p>'
			tag2 = '<p align="CENTER"><font face="Arial" size="2"><a name="tituloivcapituloiisecaoi"></a><b><span style="text-transform: uppercase">Seção I<br>DO PRESIDENTE E DO VICE-PRESIDENTE DA REPÚBLICA</span></b></font></p>'
			return [(BeautifulSoup(tag1.decode('utf-8'))).p, (BeautifulSoup(tag2.decode("utf-8"))).p]
		elif tags_name[0] == 'tituloivcapituloiisecaov' and tags_name[1] == 'tituloivcapituloiisecaovsubsecaoi':
			# logger.info('Excepcion procesada : tituloivcapituloiisecaov - tituloivcapituloiisecaovsubsecaoi')
			tag1 = '<p align="CENTER"><font face="Arial" size="2"><a name="tituloivcapituloiisecaov"></a><b><span style="text-transform: uppercase">Seção V<br>DO CONSELHO DA REPÚBLICA E DO CONSELHO DE DEFESA NACIONAL</span></b></font></p>'
			tag2 = '<p align="CENTER"><font face="Arial" size="2"><a name="tituloivcapituloiisecaovsubsecaoi"></a><b><span style="text-transform: uppercase">Subseção I<br>Do Conselho da República</span></b></font></p>'
			return [(BeautifulSoup(tag1.decode('utf-8'))).p, (BeautifulSoup(tag2.decode("utf-8"))).p]
		elif tags_name[0] == 'tituloivcapituloiii' and tags_name[1] == 'tituloivcapituloiiisecaoi':
			# logger.info('Excepcion procesada : tituloivcapituloiii - tituloivcapituloiiisecaoi')
			tag1 = '<p align="CENTER"><font face="Arial" size="2"><a name="tituloivcapituloiii"></a>CAPÍTULO III<br>DO PODER JUDICIÁRIO<br></font></p>'
			tag2 = '<p align="CENTER"><font face="Arial" size="2"><a name="tituloivcapituloiiisecaoi"></a><b><span style="text-transform: uppercase">Seção I<br>DISPOSIÇÕES GERAIS</span></b></font></p>'
			return [(BeautifulSoup(tag1.decode('utf-8'))).p, (BeautifulSoup(tag2.decode("utf-8"))).p]
		elif tags_name[0] == 'tituloivcapituloiv.' and tags_name[1] == 'tituloivcapituloivsecaoi':
			# logger.info('Excepcion procesada : tituloivcapituloiv. - tituloivcapituloivsecaoi')
			tag1 = '<p align="CENTER"><font size="2"><a name="tituloivcapituloiv."></a>CAPÍTULO IV<br>DAS FUNÇÕES ESSENCIAIS À JUSTIÇA<br><a href="http://www.planalto.gov.br/ccivil_03/Constituicao/Emendas/Emc/emc80.htm#art1">(Redação dada pela Emenda Constitucional nº 80, de 2014)</a></font></p>'
			tag2 = '<p align="CENTER"><font face="Arial" size="2"><br><a name="tituloivcapituloivsecaoi"></a><b><span style="text-transform: uppercase">Seção I<br>DO MINISTÉRIO PÚBLICO</span></b></font></p>'
			return [(BeautifulSoup(tag1.decode('utf-8'))).p, (BeautifulSoup(tag2.decode("utf-8"))).p]
		elif tags_name[0] == 'titulov' and tags_name[1] == 'titulovcapituloi' and len(tags_name) == 3 and tags_name[2] == 'titulovcapituloisecaoi':
			# logger.info('Excepcion procesada : titulov - titulovcapituloi - titulovcapituloisecaoi')
			tag1 = '<p align="center"><font face="Arial" size="2"><a name="titulov"></a><b><span style="text-transform: uppercase">TÍTULO V<br>Da Defesa do Estado e Das Instituições Democráticas </span></b></font></p>'
			tag2 = '<p align="center"><font face="Arial" size="2"><a name="titulovcapituloi"></a>CAPÍTULO I<br>DO ESTADO DE DEFESA E DO ESTADO DE SÍTIO<br></font></p>'
			tag3 = '<p align="center"><font face="Arial" size="2"><a name="titulovcapituloisecaoi"></a><b><span style="text-transform: uppercase">Seção I<br>DO ESTADO DE DEFESA</span></b></font></p>'
			return [(BeautifulSoup(tag1.decode('utf-8'))).p, (BeautifulSoup(tag2.decode("utf-8"))).p, (BeautifulSoup(tag3.decode("utf-8"))).p]
		elif tags_name[0] == 'titulovi' and tags_name[1] == 'titulovicapituloi' and len(tags_name) == 3 and tags_name[2] == 'titulovicapituloisecaoi':
			# logger.info('Excepcion procesada : titulovi - titulovicapituloi - titulovicapituloisecaoi')
			tag1 = '<p align="center"><font face="Arial" color="#000000" size="3"><a name="titulovi"></a></font><font face="Arial" size="2"><b><span style="text-transform: uppercase">TÍTULO VI<br>Da Tributação e do Orçamento</span></b></font></p>'
			tag2 = '<p align="center"><font face="Arial" color="#000000" size="3"><br></font><font face="Arial" size="2"><a name="titulovicapituloi"></a>CAPÍTULO I<br>DO SISTEMA TRIBUTÁRIO NACIONAL<br></font></p>'
			tag3 = '<p align="center"><font face="Arial" color="#000000" size="3"><br></font><font face="Arial" size="2"><a name="titulovicapituloisecaoi"></a><b><span style="text-transform: uppercase">Seção I<br>DOS PRINCÍPIOS GERAIS</span></b></font></p>'
			return [(BeautifulSoup(tag1.decode('utf-8'))).p, (BeautifulSoup(tag2.decode("utf-8"))).p, (BeautifulSoup(tag3.decode("utf-8"))).p]
		elif tags_name[0] == 'titulovicapituloii' and tags_name[1] == 'titulovicapituloiisecaoi':
			# logger.info('Excepcion procesada : titulovicapituloii. - titulovicapituloiisecaoi')
			tag1 = '<p align="CENTER"><font face="Arial" size="2"><a name="titulovicapituloii"></a>CAPÍTULO II<br>DAS FINANÇAS PÚBLICAS<br></font></p>'
			tag2 = '<p align="CENTER"><font face="Arial" size="2"><a name="titulovicapituloiisecaoi"></a><b><span style="text-transform: uppercase">Seção I<br>NORMAS GERAIS</span></b></font></p>'
			return [(BeautifulSoup(tag1.decode('utf-8'))).p, (BeautifulSoup(tag2.decode("utf-8"))).p]
		elif tags_name[0] == 'titulovii' and tags_name[1] == 'tituloviicapituloi':
			# logger.info('Excepcion procesada : titulovii. - tituloviicapituloi')
			tag1 = '<p align="center"><font face="Arial" size="2"><a name="titulovii"></a><b><span style="text-transform: uppercase">TÍTULO VII<br>Da Ordem Econômica e Financeira </span></b> <br></font></p>'
			tag2 = '<p align="center"><font face="Arial" size="2"><a name="tituloviicapituloi"></a>CAPÍTULO I<br>DOS PRINCÍPIOS GERAIS DA ATIVIDADE ECONÔMICA</font></p>'
			return [(BeautifulSoup(tag1.decode('utf-8'))).p, (BeautifulSoup(tag2.decode("utf-8"))).p]
		elif tags_name[0] == 'tituloviii' and tags_name[1] == 'tituloviiicapituloi':
			# logger.info('Excepcion procesada : titulovii. - tituloviiicapituloi')
			tag1 = '<p align="center"><font face="Arial" color="#000000" size="3"><a name="tituloviii"></a></font><font face="Arial" size="2"><b><span style="text-transform: uppercase">TÍTULO VIII<br>Da Ordem Social</span></b></font></p>'
			tag2 = '<p align="center"><font face="Arial" color="#000000" size="3"><br></font><font face="Arial" size="2"><a name="tituloviiicapituloi"></a>CAPÍTULO I<br>DISPOSIÇÃO GERAL</font></p>'
			return [(BeautifulSoup(tag1.decode('utf-8'))).p, (BeautifulSoup(tag2.decode("utf-8"))).p]
		elif tags_name[0] == 'tituloviiicapituloii' and tags_name[1] == 'tituloviiiCapii':
			# logger.info('Excepcion procesada : tituloviiicapituloii - tituloviiiCapii')
			tag1 = '<p align="CENTER"><a name="tituloviiicapituloii"></a>&nbsp;</a><font face="Arial" size="2">CAPÍTULO II<br>DA SEGURIDADE SOCIAL<br></p>'
			tag2 = '<p align="CENTER"><a name="tituloviiicapituloiisecaoi"></a><b><span style="text-transform: uppercase">Seção I<br>DISPOSIÇÕES GERAIS</span></b></p>'
			return [(BeautifulSoup(tag1.decode('utf-8'))).p, (BeautifulSoup(tag2.decode("utf-8"))).p]
		elif tags_name[0] == 'tituloviiicapituloiii' and tags_name[1] == 'tituloviiicapituloiiisecaoi':
			# logger.info('Excepcion procesada : tituloviiicapituloiii - tituloviiicapituloiiisecaoi')
			tag1 = '<p align="CENTER"><font face="Arial" size="2"><a name="tituloviiicapituloiii"></a>CAPÍTULO III<br>DA EDUCAÇÃO, DA CULTURA E DO DESPORTO<br></font></p>'
			tag2 = '<p align="CENTER"><font face="Arial" size="2"><a name="tituloviiicapituloiiisecaoi"></a><b><span style="text-transform: uppercase">Seção I<br>DA EDUCAÇÃO</span></b></font></p>'
			return [(BeautifulSoup(tag1.decode('utf-8'))).p, (BeautifulSoup(tag2.decode("utf-8"))).p]
		elif tags_name[0] == 'tituloivcapituloisecaoviii' and tags_name[1] == 'sviii':
			# logger.info('Excepcion procesada : tituloivcapituloisecaoviii - sviii')
			tag1 = '<p align="CENTER"><a name="tituloivcapituloisecaoviii"></a>&nbsp;<font face="Arial" size="2"><b><span style="text-transform: uppercase">Seção VIII<br>DO PROCESSO LEGISLATIVO</span></b><br></font></p>'
			tag2 = '<p align="CENTER"><a name="tituloivcapituloisecaoviiisubsecaoi"></a><b><span style="text-transform: uppercase">Subseção I<br>Disposição Geral</span></b></font></p>'
			return [(BeautifulSoup(tag1.decode('utf-8'))).p, (BeautifulSoup(tag2.decode("utf-8"))).p]
		elif tags_name[0] == 'tituloivcapituloiv' and tags_name[1] == 'tit.ivcap.iv':
			# logger.info('Excepcion procesada : tituloivcapituloiv - tit.ivcap.iv')
			tag1 = '<p align="CENTER"><strike><font face="Arial" size="2"><a name="tituloivcapituloiv"></a>&nbsp;</a>CAPÍTULO IV<br>DAS FUNÇÕES ESSENCIAIS À JUSTIÇA</font></strike></p>'
			return [(BeautifulSoup(tag1.decode('utf-8'))).p]
		elif tags_name[0] == 'titulox' and tags_name[1] == 'adct':
			# logger.info('Excepcion procesada : titulox - adct')
			tag1 = '<p align="center"><font face="Arial" size="2"><b><span style="text-transform: uppercase"><a name="titulox"></a>TÍTULO X<br></a>ATO DAS DISPOSIÇÕES CONSTITUCIONAIS TRANSITÓRIAS</span></b></font></p>'
			return [(BeautifulSoup(tag1.decode('utf-8'))).p]
		else:
			print soup, '\n\n'
			return [soup]


def __isTitulo(soup):
	attrs = soup.attrs
	if soup.p is not None:
		attrs = soup.p.attrs
	if 'align' in attrs:
		return attrs['align'].lower() == 'center'
	return False

def __isTituloCompuesto(soup):
	tags_a = soup.find_all(['a'])
	total = 0
	for item in tags_a:
		if 'name' in item.attrs:
			total += 1
	return total > 1

''' Metodo principal para cada parrafo (p) a procesar '''
def __procesarParrafo(soup):
	global ley_id, last_titulo_id, last_capitulo_id, last_seccion_id, last_subseccion_id, last_segmento_id, last_articulo_id, start_articles, end_of_code, last_titulo, last_capitulo, last_seccion, last_subseccion, last_articulo, articulo_completo, idnetificador_articulo, id_parent_articulo
	if (__isTitulo(soup)):
		if (__isTituloCompuesto(soup)):
			resp = __separarTituloCompuesto(soup) # resp es una lista de partes, cada parte es un tag
			print '**********esta es la respuesta luego de procesar**************'# quitar esto luego
			print resp, '\n'
			for p in resp:
				__procesarParrafo(p)
		else :
			if articulo_completo != '':
				dao.segmentoDAO.insert(articulo_completo, dao.segmentoDAO.TIPO_ARTICULO, ley_id, id_parent_articulo, idnetificador_articulo)
				idnetificador_articulo = ''
				articulo_completo = ''
			numeracion = hard_code_util.getNumeroTitular1(soup.text)
			if hard_code_util.isTitulo(soup.text):
				last_titulo = last_capitulo = last_seccion = last_subseccion = ''
				last_titulo = numeracion
				last_segmento_id = last_titulo_id = dao.segmentoDAO.insert(str(soup), dao.segmentoDAO.TIPO_TITULO, ley_id, ley_id, 'titulo' + last_titulo)
			elif hard_code_util.isCapitulo(soup.text):
				last_seccion = last_subseccion = ''
				last_capitulo = numeracion
				last_segmento_id = last_capitulo_id = dao.segmentoDAO.insert(str(soup), dao.segmentoDAO.TIPO_CAPITULO, ley_id, last_titulo_id, 'titulo' + last_titulo + "_capitulo" + last_capitulo)
			elif hard_code_util.isSeccion(soup.text):
				last_subseccion = ''
				last_seccion = numeracion
				cad = 'titulo' + last_titulo
				id_parent = last_titulo_id
				if last_capitulo != '':
					cad += "_capitulo" + last_capitulo
					id_parent = last_capitulo_id
				cad += '_seccion' + last_seccion
				last_segmento_id = last_seccion_id = dao.segmentoDAO.insert(str(soup), dao.segmentoDAO.TIPO_SECCION, ley_id, id_parent, cad)
			elif hard_code_util.isSubSeccion(soup.text):
				last_subseccion = numeracion
				cad = 'titulo' + last_titulo
				id_parent = last_titulo_id
				if last_capitulo != '':
					cad += "_capitulo" + last_capitulo
					id_parent = last_capitulo_id
				if last_seccion != '':
					cad += '_seccion' + last_seccion
					id_parent = last_seccion_id
				cad += '_subseccion' + last_subseccion
				last_subseccion_id = dao.segmentoDAO.insert(str(soup), dao.segmentoDAO.TIPO_SUBSECCION, ley_id, id_parent, cad)
				last_segmento_id = last_subseccion_id
	else:
		if hard_code_util.isArticulo(soup.text):
			cad = 'titulo' + last_titulo
			id_parent = last_titulo_id
			if last_capitulo != '':
				cad += "_capitulo" + last_capitulo
				id_parent = last_capitulo_id
			if last_seccion != '':
				cad += '_seccion' + last_seccion
				id_parent = last_seccion_id
			if last_subseccion != '':
				cad += '_subseccion' + last_subseccion
				id_parent = last_subseccion_id
			cad += '_articulo' + hard_code_util.getNumeroArticulo(soup.text)
			if soup.find('strike') is not None:
				 cad += '-'
			if articulo_completo != '':
				dao.segmentoDAO.insert(articulo_completo, dao.segmentoDAO.TIPO_ARTICULO, ley_id, id_parent, idnetificador_articulo)
				id_parent_articulo = id_parent
			idnetificador_articulo = cad
			articulo_completo = str(soup)
			start_articles = True
		elif start_articles:
			if 1>2:#hard_code_util.startEndConstitucion(soup.text) or len(end_of_code) > 0
				end_of_code += str(soup)
			else:
				if not __isTitulo(soup):
					articulo_completo += str(soup)

def readPreambulo(soup):
	global ley_id	
	preambulo_head = soup.find('font', {'color': '#800000'})
	preambulo_body = preambulo_head.find_next().find('font', {'size':'2'})
	preambulo ='</br><p align="CENTER"><strong>'+str(preambulo_head)+'</strong></p></br>'+ str(preambulo_body)
	id_header = dao.segmentoDAO.insert(preambulo, dao.segmentoDAO.TIPO_HEADER, ley_id, ley_id)	
	# logger.info('Preambulo registrado correctamente, ID = ' + str(id_header))
	return preambulo_body.find_next('p')
def readPreanbulo_ley_consoli(soup):
	global ley_id	
	preambulo_head = soup.find('font', {'color': '#800000'})
	preambulo_body = soup.find('font', {'color':'#000000'})
	preambulo ='</br><p align="CENTER"><strong>'+str(preambulo_head)+'</strong></p></br>'+ str(preambulo_body)
	id_header = dao.segmentoDAO.insert(preambulo, dao.segmentoDAO.TIPO_HEADER, ley_id, ley_id)	
	# logger.info('Preambulo registrado correctamente, ID = ' + str(id_header))
	return preambulo_body.find_next('p')	

def procesarLegislacion(soup,url_ley,codigo_ley,size_page,alias):
	try:
		global ley_id, end_of_code
	
		ley_id = dao.segmentoDAO.insert('CONSTITUIÇÃO DA REPÚBLICA FEDERATIVA DO BRASIL DE 1988', dao.segmentoDAO.TIPO_TITULO_LEY, None, None, '')
		# logger.info('Segmento - Ley registrada correctamente, ID = ' + str(ley_id))
		dao.leyDAO.insert_con_codLey('CONSTITUIÇÃO DA REPÚBLICA FEDERATIVA DO BRASIL DE 1988', url_ley, ley_id, datetime.now(), hard_code_util.ID_LEGISLACION,codigo_ley,size_page,alias)
		# logger.info('Ley registrada correctamente')
		soup_inicial = None

		if codigo_ley == 'ConstituicaoCompilado':
			soup_inicial=readPreanbulo_ley_consoli(soup)
		else:
			soup_inicial=readPreambulo(soup)	
		#titulo = soup.find('p', {'align': 'center'})
		next = soup_inicial
		while next is not None:
			__procesarParrafo(next)
			next = next.find_next('p')
		if len(end_of_code)>0:
			id_footer = dao.segmentoDAO.insert(end_of_code, dao.segmentoDAO.TIPO_FOOTER, ley_id, ley_id)
			# logger.info('Se registro el footer, ID = ' + str(id_footer))		
	
	except Exception, e:
		# logger.error('Error general : ' + str(e))
		raise