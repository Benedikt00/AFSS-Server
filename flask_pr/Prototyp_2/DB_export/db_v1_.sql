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
-- Table structure for table `Lookup_Table_Search`
--

DROP TABLE IF EXISTS `Lookup_Table_Search`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Lookup_Table_Search` (
  `term` varchar(255) NOT NULL,
  `location` json DEFAULT NULL,
  PRIMARY KEY (`term`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Lookup_Table_Search`
--

LOCK TABLES `Lookup_Table_Search` WRITE;
/*!40000 ALTER TABLE `Lookup_Table_Search` DISABLE KEYS */;
/*!40000 ALTER TABLE `Lookup_Table_Search` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `area`
--

DROP TABLE IF EXISTS `area`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `area` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(20) DEFAULT NULL,
  `max_cont` int DEFAULT NULL,
  `allocated_cont` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `area`
--

LOCK TABLES `area` WRITE;
/*!40000 ALTER TABLE `area` DISABLE KEYS */;
INSERT INTO `area` VALUES (0,'Commisioning Station',1,0),(1,'AFSS_1',24,0);
/*!40000 ALTER TABLE `area` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `article`
--

DROP TABLE IF EXISTS `article`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `article` (
  `id` int NOT NULL AUTO_INCREMENT,
  `article_name` varchar(50) DEFAULT NULL,
  `article_description` text,
  `category` json DEFAULT NULL,
  `groupes` json DEFAULT NULL,
  `weight` int DEFAULT NULL,
  `picture` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `article`
--

LOCK TABLES `article` WRITE;
/*!40000 ALTER TABLE `article` DISABLE KEYS */;
INSERT INTO `article` VALUES (4,'Ascheregen','by Casper','\"\\n[{\'cat\': \'Farbe\', \'value\': \'\', \'prefix\': \'Schwarz\', \'unit\': \' \'}]\\n\"','[\"Maschinenbau\", \"Schrauben\"]',999,'makeitmeme_OcYCK.jpeg'),(5,'Scope','wegrwg','\"\\n[{\'cat\': \'Farbe\', \'value\': \'\', \'prefix\': \'Schwarz\', \'unit\': \' \'}, {\'cat\': \'Höhe\', \'value\': \'10\', \'prefix\': \'m\', \'unit\': \'m\'}]\\n\"','[\"Elektronik\", \"Spule\"]',132,'LWL Dämpfungsmessung.jpg'),(6,'10 von 10','Julia Meladine','\"\\n[{\'cat\': \'Farbe\', \'value\': \'\', \'prefix\': \'Schwarz\', \'unit\': \' \'}, {\'cat\': \'Spannung\', \'value\': \'4\', \'prefix\': \'m\', \'unit\': \'V\'}]\\n\"','[\"Item\", \"Verbindungssatz\"]',8,'asd.jpeg'),(7,'Nicht adoptiert','Alligatoah','\"\\n[{\'cat\': \'Höhe\', \'value\': \'1\', \'prefix\': \'m\', \'unit\': \'m\'}]\\n\"','[\"Maschinenbau\", \"Schrauben\"]',66,'Whiteboard.png'),(8,'4k20','Widerstand 4K20','\"\\n[{\'cat\': \'Widerstand\', \'value\': \'4200\', \'prefix\': \' \', \'unit\': \'Ohm\'}]\\n\"','[\"Elektronik\", \"Widerrstand\"]',2,'p1.jpeg'),(9,'Totes Herz - Meladin','Dies und jenes','\"\\n[{\'cat\': \'Farbe\', \'value\': \'\', \'prefix\': \'Schwarz\', \'unit\': \' \'}]\\n\"','[\"Item\", \"Verbindungssatz\"]',8,'Figure_1.png'),(10,'Resistor R1','This resistor is a fundamental component in electrical circuits, used to limit current flow and adjust signal levels.','[\"Resistors\"]','[\"Electrical Components\", \"Passive Components\"]',10,'default.png'),(11,'Capacitor C1','This capacitor stores and releases electrical energy, commonly used for filtering, tuning, and energy storage in circuits.','[\"Capacitors\"]','[\"Electrical Components\", \"Passive Components\"]',15,'default.png'),(12,'Inductor L1','The inductor is a coil that stores energy in a magnetic field, often used in filters, transformers, and signal processing circuits.','[\"Inductors\"]','[\"Electrical Components\", \"Passive Components\"]',20,'default.png'),(13,'Diode D1','The diode is a semiconductor device that allows current to flow in one direction, commonly used for rectification, switching, and protection in circuits.','[\"Diodes\"]','[\"Electrical Components\", \"Semiconductors\"]',5,'default.png'),(14,'Transistor Q1','The transistor is a key active component used for amplification, switching, and signal processing in electronic circuits.','[\"Transistors\"]','[\"Electrical Components\", \"Semiconductors\"]',8,'default.png'),(15,'LED D2','The Light Emitting Diode (LED) emits light when current flows through it, widely used for indicators, displays, and lighting applications.','[\"LEDs\"]','[\"Electrical Components\", \"Semiconductors\"]',3,'default.png'),(16,'Potentiometer P1','The potentiometer is a variable resistor used for controlling electrical resistance, voltage, or volume in electronic circuits.','[\"Potentiometers\"]','[\"Electrical Components\", \"Passive Components\"]',12,'default.png'),(17,'Transformer T1','The transformer is a passive electrical device that transfers electrical energy between two or more circuits through electromagnetic induction.','[\"Transformers\"]','[\"Electrical Components\", \"Passive Components\"]',25,'default.png'),(18,'Fuse F1','The fuse is a protective device designed to interrupt the circuit when current exceeds a specified value, preventing damage to components.','[\"Fuses\"]','[\"Electrical Components\", \"Passive Components\"]',6,'default.png'),(19,'Relay RLY1','The relay is an electromechanical switch used to control high-power devices with low-power signals, commonly employed in automation and control systems.','[\"Relays\"]','[\"Electrical Components\", \"Electromechanical Components\"]',18,'default.png'),(20,'Connector CN1','The connector is a device used to join electrical circuits together, enabling easy assembly, disassembly, and maintenance of electronic systems.','[\"Connectors\"]','[\"Electrical Components\", \"Interconnects\"]',10,'default.png'),(21,'Fuse Holder FH1','The fuse holder is a mechanical device used to mount and protect fuses, ensuring safe and reliable operation in electrical systems.','[\"Fuse Holders\"]','[\"Electrical Components\", \"Passive Components\"]',4,'default.png'),(22,'IC (Integrated Circuit) IC1','The integrated circuit (IC) is a complex semiconductor device containing numerous electronic components on a small chip, used in various electronic applications.','[\"Integrated Circuits\"]','[\"Electrical Components\", \"Semiconductors\"]',15,'default.png'),(23,'Switch SW1','The switch is a mechanical device used to make or break an electrical connection, enabling manual control of circuits and devices.','[\"Switches\"]','[\"Electrical Components\", \"Electromechanical Components\"]',7,'default.png'),(24,'Battery B1','The battery is a portable source of electrical energy, supplying power to electronic devices and systems.','[\"Batteries\"]','[\"Electrical Components\", \"Power Sources\"]',30,'default.png');
/*!40000 ALTER TABLE `article` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cart`
--

DROP TABLE IF EXISTS `cart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cart` (
  `id` int NOT NULL AUTO_INCREMENT,
  `stock` int DEFAULT NULL,
  `container` int DEFAULT NULL,
  `quantity` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cart`
--

LOCK TABLES `cart` WRITE;
/*!40000 ALTER TABLE `cart` DISABLE KEYS */;
INSERT INTO `cart` VALUES (1,3,7,5);
/*!40000 ALTER TABLE `cart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `title` varchar(50) NOT NULL,
  `unit` varchar(10) DEFAULT NULL,
  `prefixes` json DEFAULT NULL,
  PRIMARY KEY (`title`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES ('Bohrung','m','\"[\'m\', \'µ\']\"'),('Farbe',' ','\"[\'Weiß\',\'Rot\',\'Grün\',\'Blau\',\'Schwarz\', \'Silver\']\"'),('Gewinde','M','\"[\' \']\"'),('Höhe','m','\"[\'c\', \'m\', \' \']\"'),('Kapazität','F','\"[\'n\', \'µ\', \'m\', \' \']\"'),('Spannung','V','\"[\' \', \'m\']\"'),('Strom','A','\"[\'µ\', \'m\', \' \', \'k\']\"'),('Widerstand','Ohm','\"[\'M\', \'k\', \' \', \'m\']\"');
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `container`
--

DROP TABLE IF EXISTS `container`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `container` (
  `id` int NOT NULL AUTO_INCREMENT,
  `stocks` json DEFAULT NULL,
  `barcode` bigint unsigned DEFAULT NULL,
  `current_location` int NOT NULL,
  `target_location` int DEFAULT NULL,
  `size` varchar(10) DEFAULT NULL,
  `priority` int DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `current_location` (`current_location`),
  KEY `target_location` (`target_location`),
  CONSTRAINT `container_ibfk_1` FOREIGN KEY (`current_location`) REFERENCES `location` (`id`),
  CONSTRAINT `container_ibfk_2` FOREIGN KEY (`target_location`) REFERENCES `location` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `container`
--

LOCK TABLES `container` WRITE;
/*!40000 ALTER TABLE `container` DISABLE KEYS */;
INSERT INTO `container` VALUES (6,NULL,965854431,0,NULL,'BM',NULL),(7,NULL,314091785,0,NULL,'BM',NULL),(8,NULL,945374583,0,NULL,'BM',NULL);
/*!40000 ALTER TABLE `container` ENABLE KEYS */;
UNLOCK TABLES;

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

--
-- Table structure for table `location`
--

DROP TABLE IF EXISTS `location`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `location` (
  `id` int NOT NULL AUTO_INCREMENT,
  `area` int DEFAULT NULL,
  `category` varchar(20) DEFAULT NULL,
  `occupation_status` tinyint(1) NOT NULL,
  `size` varchar(10) DEFAULT NULL,
  `position` json DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `area` (`area`),
  CONSTRAINT `location_ibfk_1` FOREIGN KEY (`area`) REFERENCES `area` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `location`
--

LOCK TABLES `location` WRITE;
/*!40000 ALTER TABLE `location` DISABLE KEYS */;
INSERT INTO `location` VALUES (0,0,'OUT',0,' ','[0]'),(30,1,'PS',0,'BM','{\"x\": 30, \"y\": 30, \"z\": 0}'),(31,1,'PS',0,'BM','{\"x\": 190, \"y\": 30, \"z\": 0}'),(32,1,'PS',0,'BM','{\"x\": 555, \"y\": 30, \"z\": 0}'),(33,1,'PS',0,'BM','{\"x\": 920, \"y\": 30, \"z\": 0}'),(34,1,'PS',0,'BM','{\"x\": 1080, \"y\": 30, \"z\": 0}'),(35,1,'PS',0,'BM','{\"x\": 1240, \"y\": 30, \"z\": 0}'),(36,1,'PS',0,'BM','{\"x\": 30, \"y\": 110, \"z\": 0}'),(37,1,'PS',0,'BM','{\"x\": 190, \"y\": 110, \"z\": 0}'),(38,1,'PS',0,'BM','{\"x\": 555, \"y\": 110, \"z\": 0}'),(39,1,'PS',0,'BM','{\"x\": 920, \"y\": 110, \"z\": 0}'),(40,1,'PS',0,'BM','{\"x\": 1080, \"y\": 110, \"z\": 0}'),(41,1,'PS',0,'BM','{\"x\": 1240, \"y\": 110, \"z\": 0}'),(42,1,'PS',0,'BM','{\"x\": 30, \"y\": 190, \"z\": 0}'),(43,1,'SF',0,'BM','{\"x\": 190, \"y\": 190, \"z\": 0}'),(44,1,'PS',0,'BM','{\"x\": 555, \"y\": 190, \"z\": 0}'),(45,1,'PS',0,'BM','{\"x\": 920, \"y\": 190, \"z\": 0}'),(46,1,'PS',0,'BM','{\"x\": 1080, \"y\": 190, \"z\": 0}'),(47,1,'PS',0,'BM','{\"x\": 1240, \"y\": 190, \"z\": 0}'),(48,1,'PS',0,'BM','{\"x\": 30, \"y\": 270, \"z\": 0}'),(49,1,'PS',0,'BM','{\"x\": 190, \"y\": 270, \"z\": 0}'),(50,1,'PS',0,'BM','{\"x\": 555, \"y\": 270, \"z\": 0}'),(51,1,'PS',0,'BM','{\"x\": 920, \"y\": 270, \"z\": 0}'),(52,1,'PS',0,'BM','{\"x\": 1080, \"y\": 270, \"z\": 0}'),(53,1,'PS',0,'BM','{\"x\": 1240, \"y\": 270, \"z\": 0}');
/*!40000 ALTER TABLE `location` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `primary_groupes`
--

DROP TABLE IF EXISTS `primary_groupes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `primary_groupes` (
  `title` varchar(50) NOT NULL,
  PRIMARY KEY (`title`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `primary_groupes`
--

LOCK TABLES `primary_groupes` WRITE;
/*!40000 ALTER TABLE `primary_groupes` DISABLE KEYS */;
INSERT INTO `primary_groupes` VALUES ('Elektronik'),('Item'),('Maschinenbau'),('Schrauben'),('V-Slot');
/*!40000 ALTER TABLE `primary_groupes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `seondary_groupes`
--

DROP TABLE IF EXISTS `seondary_groupes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `seondary_groupes` (
  `prim_title` varchar(50) NOT NULL,
  `title` varchar(50) NOT NULL,
  PRIMARY KEY (`prim_title`,`title`),
  CONSTRAINT `seondary_groupes_ibfk_1` FOREIGN KEY (`prim_title`) REFERENCES `primary_groupes` (`title`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `seondary_groupes`
--

LOCK TABLES `seondary_groupes` WRITE;
/*!40000 ALTER TABLE `seondary_groupes` DISABLE KEYS */;
INSERT INTO `seondary_groupes` VALUES ('Elektronik','Kondnsator'),('Elektronik','Spule'),('Elektronik','Widerrstand'),('Item','Nutenstein'),('Item','Verbindungssatz'),('Item','Winkel'),('Maschinenbau','Schrauben'),('Schrauben','Halbrundkopf'),('Schrauben','Zylinderkopf'),('V-Slot','Nutenstein'),('V-Slot','V-Wheel');
/*!40000 ALTER TABLE `seondary_groupes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stack_afss`
--

DROP TABLE IF EXISTS `stack_afss`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stack_afss` (
  `id` int NOT NULL AUTO_INCREMENT,
  `stock` int DEFAULT NULL,
  `container` int DEFAULT NULL,
  `quantity` int DEFAULT NULL,
  `loc_now` int DEFAULT NULL,
  `loc_goal` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stack_afss`
--

LOCK TABLES `stack_afss` WRITE;
/*!40000 ALTER TABLE `stack_afss` DISABLE KEYS */;
/*!40000 ALTER TABLE `stack_afss` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stack_prio_afss`
--

DROP TABLE IF EXISTS `stack_prio_afss`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stack_prio_afss` (
  `id` int NOT NULL AUTO_INCREMENT,
  `stock` int DEFAULT NULL,
  `container` int DEFAULT NULL,
  `quantity` int DEFAULT NULL,
  `loc_now` int DEFAULT NULL,
  `loc_goal` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stack_prio_afss`
--

LOCK TABLES `stack_prio_afss` WRITE;
/*!40000 ALTER TABLE `stack_prio_afss` DISABLE KEYS */;
INSERT INTO `stack_prio_afss` VALUES (1,3,7,5,0,0),(2,4,8,7,0,0),(3,3,7,4,0,0);
/*!40000 ALTER TABLE `stack_prio_afss` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stock`
--

DROP TABLE IF EXISTS `stock`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stock` (
  `id` int NOT NULL AUTO_INCREMENT,
  `container` int DEFAULT NULL,
  `article` int DEFAULT NULL,
  `quantity` int DEFAULT NULL,
  `reserved_quantity` int DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `container` (`container`),
  KEY `article` (`article`),
  CONSTRAINT `stock_ibfk_1` FOREIGN KEY (`container`) REFERENCES `container` (`id`),
  CONSTRAINT `stock_ibfk_2` FOREIGN KEY (`article`) REFERENCES `article` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stock`
--

LOCK TABLES `stock` WRITE;
/*!40000 ALTER TABLE `stock` DISABLE KEYS */;
INSERT INTO `stock` VALUES (1,8,9,15,0),(2,8,12,12,0),(3,7,4,10,0),(4,8,4,8,0);
/*!40000 ALTER TABLE `stock` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `term_frequency_list`
--

DROP TABLE IF EXISTS `term_frequency_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `term_frequency_list` (
  `id` int NOT NULL,
  `terms` json DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `term_frequency_list`
--

LOCK TABLES `term_frequency_list` WRITE;
/*!40000 ALTER TABLE `term_frequency_list` DISABLE KEYS */;
INSERT INTO `term_frequency_list` VALUES (4,'{\"by\": 0.14285714285714285, \"casper\": 0.14285714285714285, \"schrauben\": 0.2857142857142857, \"ascheregen\": 0.14285714285714285, \"maschinenbau\": 0.2857142857142857}'),(5,'{\"scope\": 0.16666666666666666, \"spule\": 0.3333333333333333, \"wegrwg\": 0.16666666666666666, \"elektronik\": 0.3333333333333333}'),(6,'{\"10\": 0.2222222222222222, \"von\": 0.1111111111111111, \"item\": 0.2222222222222222, \"julia\": 0.1111111111111111, \"meladine\": 0.1111111111111111, \"verbindungssatz\": 0.2222222222222222}'),(7,'{\"nicht\": 0.14285714285714285, \"adoptiert\": 0.14285714285714285, \"schrauben\": 0.2857142857142857, \"alligatoah\": 0.14285714285714285, \"maschinenbau\": 0.2857142857142857}'),(8,'{\"4k20\": 0.2857142857142857, \"elektronik\": 0.2857142857142857, \"widerstand\": 0.14285714285714285, \"widerrstand\": 0.2857142857142857}'),(9,'{\"so\": 0.058823529411764705, \"ein\": 0.058823529411764705, \"man\": 0.058823529411764705, \"herz\": 0.1176470588235294, \"item\": 0.1176470588235294, \"kann\": 0.058823529411764705, \"weil\": 0.058823529411764705, \"nicht\": 0.058823529411764705, \"totes\": 0.1176470588235294, \"leicht\": 0.058823529411764705, \"meladin\": 0.058823529411764705, \"begraben\": 0.058823529411764705, \"verbindungssatz\": 0.1176470588235294}'),(10,'{\"a\": 0.03571428571428571, \"in\": 0.03571428571428571, \"is\": 0.03571428571428571, \"r1\": 0.03571428571428571, \"to\": 0.03571428571428571, \"and\": 0.03571428571428571, \"flow\": 0.03571428571428571, \"this\": 0.03571428571428571, \"used\": 0.03571428571428571, \"limit\": 0.03571428571428571, \"adjust\": 0.03571428571428571, \"levels\": 0.03571428571428571, \"signal\": 0.03571428571428571, \"current\": 0.03571428571428571, \"passive\": 0.07142857142857142, \"circuits\": 0.03571428571428571, \"resistor\": 0.07142857142857142, \"component\": 0.03571428571428571, \"components\": 0.14285714285714285, \"electrical\": 0.10714285714285714, \"fundamental\": 0.03571428571428571}'),(11,'{\"c1\": 0.037037037037037035, \"in\": 0.037037037037037035, \"and\": 0.07407407407407407, \"for\": 0.037037037037037035, \"this\": 0.037037037037037035, \"used\": 0.037037037037037035, \"energy\": 0.07407407407407407, \"stores\": 0.037037037037037035, \"tuning\": 0.037037037037037035, \"passive\": 0.07407407407407407, \"storage\": 0.037037037037037035, \"circuits\": 0.037037037037037035, \"commonly\": 0.037037037037037035, \"releases\": 0.037037037037037035, \"capacitor\": 0.07407407407407407, \"filtering\": 0.037037037037037035, \"components\": 0.14814814814814814, \"electrical\": 0.1111111111111111}'),(12,'{\"a\": 0.06451612903225806, \"in\": 0.06451612903225806, \"is\": 0.03225806451612903, \"l1\": 0.03225806451612903, \"and\": 0.03225806451612903, \"the\": 0.03225806451612903, \"coil\": 0.03225806451612903, \"that\": 0.03225806451612903, \"used\": 0.03225806451612903, \"field\": 0.03225806451612903, \"often\": 0.03225806451612903, \"energy\": 0.03225806451612903, \"signal\": 0.03225806451612903, \"stores\": 0.03225806451612903, \"filters\": 0.03225806451612903, \"passive\": 0.06451612903225806, \"circuits\": 0.03225806451612903, \"inductor\": 0.06451612903225806, \"magnetic\": 0.03225806451612903, \"components\": 0.12903225806451613, \"electrical\": 0.06451612903225806, \"processing\": 0.03225806451612903, \"transformers\": 0.03225806451612903}'),(13,'{\"a\": 0.03225806451612903, \"d1\": 0.03225806451612903, \"in\": 0.06451612903225806, \"is\": 0.03225806451612903, \"to\": 0.03225806451612903, \"and\": 0.03225806451612903, \"for\": 0.03225806451612903, \"one\": 0.03225806451612903, \"the\": 0.03225806451612903, \"flow\": 0.03225806451612903, \"that\": 0.03225806451612903, \"used\": 0.03225806451612903, \"diode\": 0.06451612903225806, \"allows\": 0.03225806451612903, \"device\": 0.03225806451612903, \"current\": 0.03225806451612903, \"circuits\": 0.03225806451612903, \"commonly\": 0.03225806451612903, \"direction\": 0.03225806451612903, \"switching\": 0.03225806451612903, \"components\": 0.06451612903225806, \"electrical\": 0.06451612903225806, \"protection\": 0.03225806451612903, \"rectification\": 0.03225806451612903, \"semiconductor\": 0.03225806451612903, \"semiconductors\": 0.06451612903225806}'),(14,'{\"a\": 0.04, \"in\": 0.04, \"is\": 0.04, \"q1\": 0.04, \"and\": 0.04, \"for\": 0.04, \"key\": 0.04, \"the\": 0.04, \"used\": 0.04, \"active\": 0.04, \"signal\": 0.04, \"circuits\": 0.04, \"component\": 0.04, \"switching\": 0.04, \"components\": 0.08, \"electrical\": 0.08, \"electronic\": 0.04, \"processing\": 0.04, \"transistor\": 0.08, \"amplification\": 0.04, \"semiconductors\": 0.08}'),(15,'{\"d2\": 0.03571428571428571, \"it\": 0.03571428571428571, \"and\": 0.03571428571428571, \"for\": 0.03571428571428571, \"led\": 0.07142857142857142, \"the\": 0.03571428571428571, \"used\": 0.03571428571428571, \"when\": 0.03571428571428571, \"diode\": 0.03571428571428571, \"emits\": 0.03571428571428571, \"flows\": 0.03571428571428571, \"light\": 0.07142857142857142, \"widely\": 0.03571428571428571, \"current\": 0.03571428571428571, \"through\": 0.03571428571428571, \"displays\": 0.03571428571428571, \"emitting\": 0.03571428571428571, \"lighting\": 0.03571428571428571, \"components\": 0.07142857142857142, \"electrical\": 0.07142857142857142, \"indicators\": 0.03571428571428571, \"applications\": 0.03571428571428571, \"semiconductors\": 0.07142857142857142}'),(16,'{\"a\": 0.037037037037037035, \"in\": 0.037037037037037035, \"is\": 0.037037037037037035, \"or\": 0.037037037037037035, \"p1\": 0.037037037037037035, \"for\": 0.037037037037037035, \"the\": 0.037037037037037035, \"used\": 0.037037037037037035, \"volume\": 0.037037037037037035, \"passive\": 0.07407407407407407, \"voltage\": 0.037037037037037035, \"circuits\": 0.037037037037037035, \"resistor\": 0.037037037037037035, \"variable\": 0.037037037037037035, \"components\": 0.14814814814814814, \"electrical\": 0.1111111111111111, \"electronic\": 0.037037037037037035, \"resistance\": 0.037037037037037035, \"controlling\": 0.037037037037037035, \"potentiometer\": 0.07407407407407407}'),(17,'{\"a\": 0.034482758620689655, \"is\": 0.034482758620689655, \"or\": 0.034482758620689655, \"t1\": 0.034482758620689655, \"the\": 0.034482758620689655, \"two\": 0.034482758620689655, \"more\": 0.034482758620689655, \"that\": 0.034482758620689655, \"device\": 0.034482758620689655, \"energy\": 0.034482758620689655, \"between\": 0.034482758620689655, \"passive\": 0.10344827586206896, \"through\": 0.034482758620689655, \"circuits\": 0.034482758620689655, \"induction\": 0.034482758620689655, \"transfers\": 0.034482758620689655, \"components\": 0.13793103448275862, \"electrical\": 0.13793103448275862, \"transformer\": 0.06896551724137931, \"electromagnetic\": 0.034482758620689655}'),(18,'{\"a\": 0.06451612903225806, \"f1\": 0.03225806451612903, \"is\": 0.03225806451612903, \"to\": 0.06451612903225806, \"the\": 0.06451612903225806, \"fuse\": 0.06451612903225806, \"when\": 0.03225806451612903, \"value\": 0.03225806451612903, \"damage\": 0.03225806451612903, \"device\": 0.03225806451612903, \"circuit\": 0.03225806451612903, \"current\": 0.03225806451612903, \"exceeds\": 0.03225806451612903, \"passive\": 0.06451612903225806, \"designed\": 0.03225806451612903, \"interrupt\": 0.03225806451612903, \"specified\": 0.03225806451612903, \"components\": 0.16129032258064516, \"electrical\": 0.06451612903225806, \"preventing\": 0.03225806451612903, \"protective\": 0.03225806451612903}'),(19,'{\"an\": 0.03225806451612903, \"in\": 0.03225806451612903, \"is\": 0.03225806451612903, \"to\": 0.03225806451612903, \"and\": 0.03225806451612903, \"the\": 0.03225806451612903, \"rly1\": 0.03225806451612903, \"used\": 0.03225806451612903, \"with\": 0.03225806451612903, \"relay\": 0.06451612903225806, \"switch\": 0.03225806451612903, \"control\": 0.06451612903225806, \"devices\": 0.03225806451612903, \"signals\": 0.03225806451612903, \"systems\": 0.03225806451612903, \"commonly\": 0.03225806451612903, \"employed\": 0.03225806451612903, \"lowpower\": 0.03225806451612903, \"highpower\": 0.03225806451612903, \"automation\": 0.03225806451612903, \"components\": 0.12903225806451613, \"electrical\": 0.06451612903225806, \"electromechanical\": 0.0967741935483871}'),(20,'{\"a\": 0.03571428571428571, \"is\": 0.03571428571428571, \"of\": 0.03571428571428571, \"to\": 0.03571428571428571, \"and\": 0.03571428571428571, \"cn1\": 0.03571428571428571, \"the\": 0.03571428571428571, \"easy\": 0.03571428571428571, \"join\": 0.03571428571428571, \"used\": 0.03571428571428571, \"device\": 0.03571428571428571, \"systems\": 0.03571428571428571, \"assembly\": 0.03571428571428571, \"circuits\": 0.03571428571428571, \"enabling\": 0.03571428571428571, \"together\": 0.03571428571428571, \"connector\": 0.07142857142857142, \"components\": 0.07142857142857142, \"electrical\": 0.10714285714285714, \"electronic\": 0.03571428571428571, \"disassembly\": 0.03571428571428571, \"maintenance\": 0.03571428571428571, \"interconnects\": 0.07142857142857142}'),(21,'{\"a\": 0.03125, \"in\": 0.03125, \"is\": 0.03125, \"to\": 0.03125, \"and\": 0.0625, \"fh1\": 0.03125, \"the\": 0.03125, \"fuse\": 0.0625, \"safe\": 0.03125, \"used\": 0.03125, \"fuses\": 0.03125, \"mount\": 0.03125, \"device\": 0.03125, \"holder\": 0.0625, \"passive\": 0.0625, \"protect\": 0.03125, \"systems\": 0.03125, \"ensuring\": 0.03125, \"reliable\": 0.03125, \"operation\": 0.03125, \"components\": 0.125, \"electrical\": 0.09375, \"mechanical\": 0.03125}'),(22,'{\"a\": 0.0625, \"ic\": 0.0625, \"in\": 0.03125, \"is\": 0.03125, \"on\": 0.03125, \"ic1\": 0.03125, \"the\": 0.03125, \"chip\": 0.03125, \"used\": 0.03125, \"small\": 0.03125, \"device\": 0.03125, \"circuit\": 0.0625, \"complex\": 0.03125, \"various\": 0.03125, \"numerous\": 0.03125, \"components\": 0.09375, \"containing\": 0.03125, \"electrical\": 0.0625, \"electronic\": 0.0625, \"integrated\": 0.0625, \"applications\": 0.03125, \"semiconductor\": 0.03125, \"semiconductors\": 0.0625}'),(23,'{\"a\": 0.03225806451612903, \"an\": 0.03225806451612903, \"is\": 0.03225806451612903, \"of\": 0.03225806451612903, \"or\": 0.03225806451612903, \"to\": 0.03225806451612903, \"and\": 0.03225806451612903, \"sw1\": 0.03225806451612903, \"the\": 0.03225806451612903, \"make\": 0.03225806451612903, \"used\": 0.03225806451612903, \"break\": 0.03225806451612903, \"device\": 0.03225806451612903, \"manual\": 0.03225806451612903, \"switch\": 0.06451612903225806, \"control\": 0.03225806451612903, \"devices\": 0.03225806451612903, \"circuits\": 0.03225806451612903, \"enabling\": 0.03225806451612903, \"components\": 0.12903225806451613, \"connection\": 0.03225806451612903, \"electrical\": 0.0967741935483871, \"mechanical\": 0.03225806451612903, \"electromechanical\": 0.06451612903225806}'),(24,'{\"a\": 0.038461538461538464, \"b1\": 0.038461538461538464, \"is\": 0.038461538461538464, \"of\": 0.038461538461538464, \"to\": 0.038461538461538464, \"and\": 0.038461538461538464, \"the\": 0.038461538461538464, \"power\": 0.1153846153846154, \"energy\": 0.038461538461538464, \"source\": 0.038461538461538464, \"battery\": 0.07692307692307693, \"devices\": 0.038461538461538464, \"sources\": 0.07692307692307693, \"systems\": 0.038461538461538464, \"portable\": 0.038461538461538464, \"supplying\": 0.038461538461538464, \"components\": 0.07692307692307693, \"electrical\": 0.1153846153846154, \"electronic\": 0.038461538461538464}');
/*!40000 ALTER TABLE `term_frequency_list` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-30 19:35:55
