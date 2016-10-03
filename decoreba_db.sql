/*
Navicat MySQL Data Transfer

Source Server         : scaper
Source Server Version : 50624
Source Host           : localhost:3306
Source Database       : decoreba2

Target Server Type    : MYSQL
Target Server Version : 50099
File Encoding         : 65001

Date: 2015-12-01 09:28:02
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for legislacion
-- ----------------------------
DROP TABLE IF EXISTS `legislacion`;
CREATE TABLE `legislacion` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`url`  varchar(900) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`tipo`  varchar(900) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`cant_url_lv1`  int(11) NOT NULL DEFAULT 0 ,
`cant_url_lv2`  int(11) NULL DEFAULT 0 ,
`tipo_scrap`  varchar(2) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
/*!50003 AUTO_INCREMENT=56 */

;

-- ----------------------------
-- Records of legislacion
-- ----------------------------
BEGIN;
INSERT INTO `legislacion` VALUES ('1', 'http://www4.planalto.gov.br/legislacao/legislacao-1/codigos-1#content', 'Códigos', '0', '-1', 'TB'), ('2', 'http://www4.planalto.gov.br/legislacao/legislacao-1/estatutos#content', 'Estatutos', '0', '-1', 'TB'), ('3', 'http://www4.planalto.gov.br/legislacao/legislacao-1/leis-delegadas-1#content', 'Leis Delegadas', '0', '-1', 'TB'), ('4', 'http://www.planalto.gov.br/ccivil_03/Constituicao/Emendas/Emc/quadro_emc.htm', 'Emendas Constitucionais', '0', '-1', 'TB'), ('5', 'http://www.planalto.gov.br/ccivil_03/Constituicao/Constituicao.htm', 'Constituicao', '0', '0', 'UN'), ('6', 'http://www.planalto.gov.br/ccivil_03/Constituicao/ConstituicaoCompilado.htm', 'ConstituicaoCompilado', '0', '0', 'UN'), ('7', 'http://www4.planalto.gov.br/legislacao/legislacao-1/leis-complementares-1#content', 'Leis Complementares', '0', '0', 'TB'), ('8', 'http://www4.planalto.gov.br/legislacao/legislacao-1/decretos-leis#content', 'Decretos-Leis', '0', '0', 'TB'), ('9', 'http://www4.planalto.gov.br/legislacao/legislacao-1/leis-ordinarias#content', 'Leis Ordinárias', '0', '0', 'TB'), ('10', 'http://www4.planalto.gov.br/legislacao/legislacao-1/medidas-provisorias#content', 'Medidas Provisórias', '0', '0', 'TB');
COMMIT;

-- ----------------------------
-- Table structure for ley
-- ----------------------------
DROP TABLE IF EXISTS `ley`;
CREATE TABLE `ley` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`titulo`  varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`url_ley`  varchar(900) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`id_segmento`  int(11) NULL DEFAULT NULL ,
`fecha`  datetime NOT NULL ,
`id_legislacion`  int(11) NOT NULL ,
`codigo_ley`  varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`size_ley`  double NULL DEFAULT NULL ,
`alias`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`),
FOREIGN KEY (`id_legislacion`) REFERENCES `legislacion` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
FOREIGN KEY (`id_segmento`) REFERENCES `segmento` (`id`) ON DELETE SET NULL ON UPDATE SET NULL,
INDEX `id_legislacion_fk` USING BTREE (`id_legislacion`),
INDEX `id_segmento_fk` USING BTREE (`id_segmento`),
INDEX `codigo_ley` USING BTREE (`codigo_ley`),
INDEX `alias` USING BTREE (`alias`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
COMMENT='InnoDB free: 260096 kB; (`id_legislacion`) REFER `decoreba2/legislacion`(`id`) O'
/*!50003 AUTO_INCREMENT=24216 */

;

-- ----------------------------
-- Records of ley
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for scraper_log
-- ----------------------------
DROP TABLE IF EXISTS `scraper_log`;
CREATE TABLE `scraper_log` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`fecha`  datetime NOT NULL ,
`tipo_log`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`detalle`  varchar(500) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
/*!50003 AUTO_INCREMENT=73132 */

;

-- ----------------------------
-- Records of scraper_log
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for segmento
-- ----------------------------
DROP TABLE IF EXISTS `segmento`;
CREATE TABLE `segmento` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`contenido`  longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL ,
`tipo`  varchar(15) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`id_parent`  int(11) NULL DEFAULT NULL ,
`identificador`  varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`id_ley`  int(11) NULL DEFAULT NULL ,
PRIMARY KEY (`id`),
FOREIGN KEY (`id_parent`) REFERENCES `segmento` (`id`) ON DELETE SET NULL ON UPDATE SET NULL,
INDEX `id_parent` USING BTREE (`id_parent`),
INDEX `id_ley` USING BTREE (`id_ley`),
INDEX `identificador` USING BTREE (`identificador`),
INDEX `contenido` USING BTREE (`contenido`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
COMMENT='InnoDB free: 260096 kB; (`id_parent`) REFER `decoreba2/segmento`(`id`) ON UPDATE'
/*!50003 AUTO_INCREMENT=340313 */

;

-- ----------------------------
-- Records of segmento
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Auto increment value for legislacion
-- ----------------------------
ALTER TABLE `legislacion` AUTO_INCREMENT=56;

-- ----------------------------
-- Auto increment value for ley
-- ----------------------------
ALTER TABLE `ley` AUTO_INCREMENT=24216;

-- ----------------------------
-- Auto increment value for scraper_log
-- ----------------------------
ALTER TABLE `scraper_log` AUTO_INCREMENT=73132;

-- ----------------------------
-- Auto increment value for segmento
-- ----------------------------
ALTER TABLE `segmento` AUTO_INCREMENT=340313;
