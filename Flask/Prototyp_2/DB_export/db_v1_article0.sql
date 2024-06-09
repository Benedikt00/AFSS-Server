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
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-28 20:18:26
