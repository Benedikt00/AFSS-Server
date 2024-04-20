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
-- Table structure for table `article`
--

DROP TABLE IF EXISTS `article`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `article` (
  `id` int NOT NULL AUTO_INCREMENT,
  `article_name` varchar(50) DEFAULT NULL,
  `article_description` tinytext,
  `category` json DEFAULT NULL,
  `groupes` json DEFAULT NULL,
  `weight` int DEFAULT NULL,
  `picture` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `article`
--

LOCK TABLES `article` WRITE;
/*!40000 ALTER TABLE `article` DISABLE KEYS */;
INSERT INTO `article` VALUES (4,'Ascheregen','by Casper','\"\\n[{\'cat\': \'Farbe\', \'value\': \'\', \'prefix\': \'Schwarz\', \'unit\': \' \'}]\\n\"','[\"Maschinenbau\", \"Schrauben\"]',999,'makeitmeme_OcYCK.jpeg'),(5,'Scope','wegrwg','\"\\n[{\'cat\': \'Farbe\', \'value\': \'\', \'prefix\': \'Schwarz\', \'unit\': \' \'}, {\'cat\': \'Höhe\', \'value\': \'10\', \'prefix\': \'m\', \'unit\': \'m\'}]\\n\"','[\"Elektronik\", \"Spule\"]',132,'LWL Dämpfungsmessung.jpg'),(6,'10 von 10','Julia Meladine','\"\\n[{\'cat\': \'Farbe\', \'value\': \'\', \'prefix\': \'Schwarz\', \'unit\': \' \'}, {\'cat\': \'Spannung\', \'value\': \'4\', \'prefix\': \'m\', \'unit\': \'V\'}]\\n\"','[\"Item\", \"Verbindungssatz\"]',8,'asd.jpeg'),(7,'Nicht adoptiert','Alligatoah','\"\\n[{\'cat\': \'Höhe\', \'value\': \'1\', \'prefix\': \'m\', \'unit\': \'m\'}]\\n\"','[\"Maschinenbau\", \"Schrauben\"]',66,'Whiteboard.png'),(8,'4k20','Widerstand 4K20','\"\\n[{\'cat\': \'Widerstand\', \'value\': \'4200\', \'prefix\': \' \', \'unit\': \'Ohm\'}]\\n\"','[\"Elektronik\", \"Widerrstand\"]',2,'p1.jpeg'),(9,'Totes Herz - Meladin','weil man ein Totes herz nicht so leicht begraben kann','\"\\n[{\'cat\': \'Farbe\', \'value\': \'\', \'prefix\': \'Schwarz\', \'unit\': \' \'}]\\n\"','[\"Item\", \"Verbindungssatz\"]',8,'Figure_1.png');
/*!40000 ALTER TABLE `article` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-04-19 14:51:52
