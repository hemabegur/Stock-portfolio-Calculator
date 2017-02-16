CREATE DATABASE  IF NOT EXISTS `portfolio` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `portfolio`;
-- MySQL dump 10.13  Distrib 5.7.12, for osx10.9 (x86_64)
--
-- Host: 127.0.0.1    Database: portfolio
-- ------------------------------------------------------
-- Server version	5.7.16

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `IndexStrategy`
--

DROP TABLE IF EXISTS `IndexStrategy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `IndexStrategy` (
  `ticker_id` int(11) NOT NULL,
  `ticker_name` varchar(45) DEFAULT NULL,
  `time` int(11) DEFAULT NULL,
  `risk` int(11) DEFAULT NULL,
  `income` int(11) DEFAULT NULL,
  `type` varchar(45) NOT NULL,
  PRIMARY KEY (`ticker_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `IndexStrategy`
--

LOCK TABLES `IndexStrategy` WRITE;
/*!40000 ALTER TABLE `IndexStrategy` DISABLE KEYS */;
INSERT INTO `IndexStrategy` VALUES (1,'VTI',1,2,3,'2'),(2,'MGC',1,2,3,'2'),(3,'IWV',1,2,3,'1'),(4,'SIZE',1,2,3,'1'),(5,'OEF',1,2,3,'1'),(6,'IWL',1,2,3,'1'),(7,'THRK',1,2,3,'1'),(8,'ONEK',1,2,3,'1'),(9,'EPS',1,2,3,'1'),(10,'SCHX',1,2,3,'2'),(11,'IVV',1,2,3,'2'),(12,'VOO',1,2,3,'2'),(13,'SPY',1,2,3,'2'),(14,'JHML',1,2,3,'1'),(15,'IYY',1,2,3,'1'),(16,'IWB',1,2,3,'1'),(17,'VONE',1,2,3,'2'),(18,'VTHR',1,2,3,'2'),(19,'SCHB',1,2,3,'2'),(20,'ITOT',1,2,3,'2'),(21,'VEA',1,1,3,'3'),(22,'SCHF',1,2,3,'3'),(23,'IEFA',1,2,3,'3'),(24,'VXUS',1,2,3,'3'),(25,'VEU',1,2,3,'3'),(26,'IXUS',1,2,3,'4'),(27,'IFV',1,2,3,'4'),(28,'EFAV',1,2,3,'4'),(29,'ACWX',1,2,3,'4'),(30,'EFA',1,2,3,'4'),(31,' ILTB',1,1,3,'5'),(32,'BAB',1,2,3,'5'),(33,'BLV',1,2,3,'5');
/*!40000 ALTER TABLE `IndexStrategy` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-12-12 21:32:50
