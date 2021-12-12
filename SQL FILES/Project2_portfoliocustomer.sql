-- MySQL dump 10.13  Distrib 8.0.26, for Win64 (x86_64)
--
-- Host: db-mysql-nyc3-51583-do-user-8820074-0.b.db.ondigitalocean.com    Database: Project2
-- ------------------------------------------------------
-- Server version	8.0.26

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
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '71b2c3a9-5097-11ec-ac32-16947e70e213:1-111';

--
-- Table structure for table `portfoliocustomer`
--

DROP TABLE IF EXISTS `portfoliocustomer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `portfoliocustomer` (
  `id` int NOT NULL AUTO_INCREMENT,
  `customerssn` int NOT NULL,
  `companyid` int NOT NULL,
  `companysharecode` varchar(120) NOT NULL,
  `quantity` int NOT NULL,
  `purchasedprice` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `portfoliocustomer_company_fk_idx` (`companyid`),
  KEY `portfoliocustomer_customer_fk_idx` (`customerssn`),
  CONSTRAINT `portfoliocustomer_company_fk` FOREIGN KEY (`companyid`) REFERENCES `company` (`id`),
  CONSTRAINT `portfoliocustomer_customer_fk` FOREIGN KEY (`customerssn`) REFERENCES `customer` (`ssn`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `portfoliocustomer`
--

LOCK TABLES `portfoliocustomer` WRITE;
/*!40000 ALTER TABLE `portfoliocustomer` DISABLE KEYS */;
INSERT INTO `portfoliocustomer` VALUES (1,951847623,101,'AAPL',5000,158),(2,951847623,102,'TSLA',1000,1091),(3,951847623,101,'AAPL',1000,158),(4,951847623,102,'TSLA',10000,1091);
/*!40000 ALTER TABLE `portfoliocustomer` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-11-28 19:37:03
