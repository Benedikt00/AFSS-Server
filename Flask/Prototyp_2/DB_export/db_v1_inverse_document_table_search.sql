-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: db_v1
-- ------------------------------------------------------
-- Server version	8.3.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `inverse_document_table_search`
--

DROP TABLE IF EXISTS `inverse_document_table_search`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inverse_document_table_search` (
  `term` varchar(255) NOT NULL,
  `value` float DEFAULT NULL,
  PRIMARY KEY (`term`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inverse_document_table_search`
--

LOCK TABLES `inverse_document_table_search` WRITE;
/*!40000 ALTER TABLE `inverse_document_table_search` DISABLE KEYS */;
INSERT INTO `inverse_document_table_search` VALUES ('10',4.04452),('4k20',4.04452),('a',1.55962),('active',4.04452),('adjust',4.04452),('adoptiert',4.04452),('alligatoah',4.04452),('allows',4.04452),('amplification',4.04452),('an',3.35138),('and',1.64663),('applications',3.35138),('ascheregen',4.04452),('assembly',4.04452),('automation',4.04452),('b1',4.04452),('battery',4.04452),('begraben',4.04452),('between',4.04452),('break',4.04452),('by',4.04452),('c1',4.04452),('capacitor',4.04452),('casper',4.04452),('chip',4.04452),('circuit',3.35138),('circuits',1.8473),('cn1',4.04452),('coil',4.04452),('commonly',2.94591),('complex',4.04452),('component',3.35138),('components',1.33647),('connection',4.04452),('connector',4.04452),('containing',4.04452),('control',3.35138),('controlling',4.04452),('current',2.65823),('d1',4.04452),('d2',4.04452),('damage',4.04452),('designed',4.04452),('device',2.09861),('devices',2.94591),('diode',3.35138),('direction',4.04452),('disassembly',4.04452),('displays',4.04452),('easy',4.04452),('ein',4.04452),('electrical',1.33647),('electromagnetic',4.04452),('electromechanical',3.35138),('electronic',2.43508),('elektronik',3.35138),('emits',4.04452),('emitting',4.04452),('employed',4.04452),('enabling',3.35138),('energy',2.65823),('ensuring',4.04452),('exceeds',4.04452),('f1',4.04452),('fh1',4.04452),('field',4.04452),('filtering',4.04452),('filters',4.04452),('flow',3.35138),('flows',4.04452),('for',2.43508),('fundamental',4.04452),('fuse',3.35138),('fuses',4.04452),('herz',4.04452),('highpower',4.04452),('holder',4.04452),('ic',4.04452),('ic1',4.04452),('in',1.8473),('indicators',4.04452),('induction',4.04452),('inductor',4.04452),('integrated',4.04452),('interconnects',4.04452),('interrupt',4.04452),('is',1.47957),('it',4.04452),('item',3.35138),('join',4.04452),('julia',4.04452),('kann',4.04452),('key',4.04452),('l1',4.04452),('led',4.04452),('leicht',4.04452),('levels',4.04452),('light',4.04452),('lighting',4.04452),('limit',4.04452),('lowpower',4.04452),('magnetic',4.04452),('maintenance',4.04452),('make',4.04452),('man',4.04452),('manual',4.04452),('maschinenbau',3.35138),('mechanical',3.35138),('meladin',4.04452),('meladine',4.04452),('more',4.04452),('mount',4.04452),('nicht',3.35138),('numerous',4.04452),('of',2.94591),('often',4.04452),('on',4.04452),('one',4.04452),('operation',4.04452),('or',2.94591),('p1',4.04452),('passive',2.09861),('portable',4.04452),('potentiometer',4.04452),('power',4.04452),('preventing',4.04452),('processing',3.35138),('protect',4.04452),('protection',4.04452),('protective',4.04452),('q1',4.04452),('r1',4.04452),('rectification',4.04452),('relay',4.04452),('releases',4.04452),('reliable',4.04452),('resistance',4.04452),('resistor',3.35138),('rly1',4.04452),('safe',4.04452),('schrauben',3.35138),('scope',4.04452),('semiconductor',3.35138),('semiconductors',2.65823),('signal',2.94591),('signals',4.04452),('small',4.04452),('so',4.04452),('source',4.04452),('sources',4.04452),('specified',4.04452),('spule',4.04452),('storage',4.04452),('stores',3.35138),('supplying',4.04452),('sw1',4.04452),('switch',3.35138),('switching',3.35138),('systems',2.65823),('t1',4.04452),('that',2.94591),('the',1.47957),('this',3.35138),('through',3.35138),('to',1.96508),('together',4.04452),('totes',4.04452),('transfers',4.04452),('transformer',4.04452),('transformers',4.04452),('transistor',4.04452),('tuning',4.04452),('two',4.04452),('used',1.55962),('value',4.04452),('variable',4.04452),('various',4.04452),('verbindungssatz',3.35138),('voltage',4.04452),('volume',4.04452),('von',4.04452),('wegrwg',4.04452),('weil',4.04452),('when',3.35138),('widely',4.04452),('widerrstand',4.04452),('widerstand',4.04452),('with',4.04452);
/*!40000 ALTER TABLE `inverse_document_table_search` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-28 20:18:27
