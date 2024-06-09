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
INSERT INTO `location` VALUES (0,0,'OUT',0,' ','[0]'),(30,1,'PS',0,'BM','{\"x\": 30, \"y\": 30, \"z\": 0}'),(31,1,'PS',0,'BM','{\"x\": 190, \"y\": 30, \"z\": 0}'),(32,1,'PS',0,'BM','{\"x\": 555, \"y\": 30, \"z\": 0}'),(33,1,'PS',0,'BM','{\"x\": 920, \"y\": 30, \"z\": 0}'),(34,1,'PS',0,'BM','{\"x\": 1080, \"y\": 30, \"z\": 0}'),(35,1,'PS',0,'BM','{\"x\": 1240, \"y\": 30, \"z\": 0}'),(36,1,'PS',0,'BM','{\"x\": 30, \"y\": 110, \"z\": 0}'),(37,1,'PS',0,'BM','{\"x\": 190, \"y\": 110, \"z\": 0}'),(38,1,'PS',0,'BM','{\"x\": 555, \"y\": 110, \"z\": 0}'),(39,1,'PS',0,'BM','{\"x\": 920, \"y\": 110, \"z\": 0}'),(40,1,'PS',0,'BM','{\"x\": 1080, \"y\": 110, \"z\": 0}'),(41,1,'PS',0,'BM','{\"x\": 1240, \"y\": 110, \"z\": 0}'),(42,1,'PS',0,'BM','{\"x\": 30, \"y\": 190, \"z\": 0}'),(43,1,'PS',0,'BM','{\"x\": 190, \"y\": 190, \"z\": 0}'),(44,1,'PS',0,'BM','{\"x\": 555, \"y\": 190, \"z\": 0}'),(45,1,'PS',0,'BM','{\"x\": 920, \"y\": 190, \"z\": 0}'),(46,1,'PS',0,'BM','{\"x\": 1080, \"y\": 190, \"z\": 0}'),(47,1,'PS',0,'BM','{\"x\": 1240, \"y\": 190, \"z\": 0}'),(48,1,'PS',0,'BM','{\"x\": 30, \"y\": 270, \"z\": 0}'),(49,1,'PS',0,'BM','{\"x\": 190, \"y\": 270, \"z\": 0}'),(50,1,'PS',0,'BM','{\"x\": 555, \"y\": 270, \"z\": 0}'),(51,1,'PS',0,'BM','{\"x\": 920, \"y\": 270, \"z\": 0}'),(52,1,'PS',0,'BM','{\"x\": 1080, \"y\": 270, \"z\": 0}'),(53,1,'PS',0,'BM','{\"x\": 1240, \"y\": 270, \"z\": 0}');
/*!40000 ALTER TABLE `location` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-28 20:18:25
