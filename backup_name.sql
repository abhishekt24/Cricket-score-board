-- MySQL dump 10.13  Distrib 5.7.23, for Linux (x86_64)
--
-- Host: localhost    Database: cricket_score
-- ------------------------------------------------------
-- Server version	5.7.23-0ubuntu0.16.04.1

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
-- Table structure for table `ball_wise`
--

DROP TABLE IF EXISTS `ball_wise`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ball_wise` (
  `ball_num` int(11) NOT NULL,
  `over_num` int(11) NOT NULL,
  `run` int(11) DEFAULT NULL,
  `wicket` tinyint(1) DEFAULT NULL,
  `extra` varchar(10) DEFAULT NULL,
  `player_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`ball_num`,`over_num`),
  KEY `fcat` (`over_num`),
  CONSTRAINT `ball_wise_ibfk_1` FOREIGN KEY (`over_num`) REFERENCES `overs_data` (`over_num`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ball_wise`
--

LOCK TABLES `ball_wise` WRITE;
/*!40000 ALTER TABLE `ball_wise` DISABLE KEYS */;
INSERT INTO `ball_wise` VALUES (1,1,3,0,'none',1),(1,2,4,0,'none',1),(2,1,6,0,'none',2),(2,2,4,0,'none',1),(3,1,0,1,'none',2),(3,2,1,0,'Byes',1),(4,1,4,0,'none',2),(4,2,4,0,'none',1),(5,1,4,0,'none',1),(5,2,4,0,'none',1),(6,1,4,0,'none',1),(6,2,0,1,'none',2);
/*!40000 ALTER TABLE `ball_wise` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `overs_data`
--

DROP TABLE IF EXISTS `overs_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `overs_data` (
  `over_num` int(11) NOT NULL,
  `runs` int(11) NOT NULL,
  `wickets` int(11) DEFAULT NULL,
  `extras` int(11) DEFAULT NULL,
  `player1_score` int(11) DEFAULT NULL,
  `player2_score` int(11) DEFAULT NULL,
  PRIMARY KEY (`over_num`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `overs_data`
--

LOCK TABLES `overs_data` WRITE;
/*!40000 ALTER TABLE `overs_data` DISABLE KEYS */;
INSERT INTO `overs_data` VALUES (1,21,1,0,11,4),(2,17,1,0,27,0);
/*!40000 ALTER TABLE `overs_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `players`
--

DROP TABLE IF EXISTS `players`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `players` (
  `player_no` int(11) NOT NULL,
  `runs` int(11) DEFAULT '0',
  `status` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`player_no`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `players`
--

LOCK TABLES `players` WRITE;
/*!40000 ALTER TABLE `players` DISABLE KEYS */;
INSERT INTO `players` VALUES (1,27,'not out'),(2,6,'out'),(3,4,'out'),(4,0,'not out'),(5,0,NULL),(6,0,NULL),(7,0,NULL),(8,0,NULL),(9,0,NULL),(10,0,NULL),(11,0,NULL);
/*!40000 ALTER TABLE `players` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-09-25 21:06:27
