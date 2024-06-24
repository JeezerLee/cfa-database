CREATE DATABASE  IF NOT EXISTS `cfa_database` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `cfa_database`;
-- MySQL dump 10.13  Distrib 8.0.26, for Win64 (x86_64)
--
-- Host: localhost    Database: cfa_database
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

--
-- Table structure for table `access_logs`
--

DROP TABLE IF EXISTS `access_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `access_logs` (
  `access_id` int NOT NULL,
  `student_accessed` int DEFAULT NULL,
  `accessing_adviser` varchar(45) DEFAULT NULL,
  `time_accessed` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`access_id`),
  KEY `accessed_student_idx` (`student_accessed`),
  KEY `accessing_adviser_idx` (`accessing_adviser`),
  CONSTRAINT `accessing_adviser` FOREIGN KEY (`accessing_adviser`) REFERENCES `accounts` (`username`),
  CONSTRAINT `student_accessed` FOREIGN KEY (`student_accessed`) REFERENCES `database` (`student_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `access_logs`
--

LOCK TABLES `access_logs` WRITE;
/*!40000 ALTER TABLE `access_logs` DISABLE KEYS */;
INSERT INTO `access_logs` VALUES (0,201764529,'admin','18/04/2022 14:22:45'),(1,201764529,'admin','18/04/2022 14:22:49'),(2,201764529,'admin','18/04/2022 14:23:04'),(3,201764529,'admin','18/04/2022 14:23:15'),(4,201764529,'test','18/04/2022 14:26:30'),(5,201764529,'admin','18/04/2022 14:27:38');
/*!40000 ALTER TABLE `access_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts`
--

DROP TABLE IF EXISTS `accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts` (
  `username` varchar(45) NOT NULL,
  `password` varchar(45) DEFAULT NULL,
  `role` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts`
--

LOCK TABLES `accounts` WRITE;
/*!40000 ALTER TABLE `accounts` DISABLE KEYS */;
INSERT INTO `accounts` VALUES ('admin','admin3','user'),('test','test','admin');
/*!40000 ALTER TABLE `accounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `database`
--

DROP TABLE IF EXISTS `database`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `database` (
  `student_id` int NOT NULL,
  `student_name` varchar(45) DEFAULT NULL,
  `link_to_records` varchar(90) DEFAULT NULL,
  PRIMARY KEY (`student_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `database`
--

LOCK TABLES `database` WRITE;
/*!40000 ALTER TABLE `database` DISABLE KEYS */;
INSERT INTO `database` VALUES (201764029,'Jessy James','https://drive.google.com/drive/u/0/');
INSERT INTO `database` VALUES (201964529,'Hikigaya Hachiman','https://drive.google.com/drive/u/0/');
INSERT INTO `database` VALUES (201866080,'Yukinoshita Yukinon','https://drive.google.com/drive/u/0/');
INSERT INTO `database` VALUES (201563039,'Yuigahama Yui','https://drive.google.com/drive/u/0/');
INSERT INTO `database` VALUES (201645675,'Loid Forger','https://drive.google.com/drive/u/0/');
INSERT INTO `database` VALUES (201685478,'Yor Forger','https://drive.google.com/drive/u/0/');
INSERT INTO `database` VALUES (201647837,'Anya Forger','https://drive.google.com/drive/u/0/');
INSERT INTO `database` VALUES (201603536,'Bond Forger','https://drive.google.com/drive/u/0/');
INSERT INTO `database` VALUES (201763479,'Miyuki Shirogane','https://drive.google.com/drive/u/0/');
INSERT INTO `database` VALUES (201810793,'Kaguya Shinomiya','https://drive.google.com/drive/u/0/');
INSERT INTO `database` VALUES (201899824,'Chika Fujiwara','https://drive.google.com/drive/u/0/');
INSERT INTO `database` VALUES (201962901,'Yu Ishigami','https://drive.google.com/drive/u/0/');
INSERT INTO `database` VALUES (201912087,'Miko Iino','https://drive.google.com/drive/u/0/');
INSERT INTO `database` VALUES (201901928,'Ai Hayasaka','https://drive.google.com/drive/u/0/');
/*!40000 ALTER TABLE `database` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `remarks`
--

DROP TABLE IF EXISTS `remarks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `remarks` (
  `remark_id` int NOT NULL,
  `student_id` int DEFAULT NULL,
  `remark` varchar(45) DEFAULT NULL,
  `date` varchar(20) DEFAULT NULL,
  `adviser` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`remark_id`),
  KEY `adviser_idx` (`adviser`),
  KEY `student_id_idx` (`student_id`),
  CONSTRAINT `adviser` FOREIGN KEY (`adviser`) REFERENCES `accounts` (`username`) ON DELETE CASCADE,
  CONSTRAINT `student_id` FOREIGN KEY (`student_id`) REFERENCES `database` (`student_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `remarks`
--

LOCK TABLES `remarks` WRITE;
/*!40000 ALTER TABLE `remarks` DISABLE KEYS */;
INSERT INTO `remarks` VALUES (1,201764529,'test','16/04/2022 22:57:42','test'),(2,201764529,'this is a remark','16/04/2022 23:09:55','test'),(3,201764529,'new remark!','17/04/2022 00:55:36','test'),(4,201764529,'a very long remark to test what it looks like','17/04/2022 00:56:13','test');
/*!40000 ALTER TABLE `remarks` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-04-18 14:33:19
