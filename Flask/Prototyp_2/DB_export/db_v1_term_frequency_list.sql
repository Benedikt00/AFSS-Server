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

-- Dump completed on 2024-05-28 20:18:25