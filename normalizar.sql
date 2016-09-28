
UPDATE segmento SET identificador = REPLACE(identificador, '-1', '') WHERE tipo = 'ARTICULO' AND identificador LIKE '%-1';

SELECT identificador FROM segmento WHERE tipo = 'ARTICULO' AND identificador LIKE '%-1';

