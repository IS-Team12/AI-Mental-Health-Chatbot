-- MySQL dump 10.13  Distrib 8.0.32, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: ai_mental_health_chatbot
-- ------------------------------------------------------
-- Server version	8.0.32

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
-- Table structure for table `account_type`
--

DROP TABLE IF EXISTS `account_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_type` (
  `account_type_id` int NOT NULL,
  `account_name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`account_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_type`
--

LOCK TABLES `account_type` WRITE;
/*!40000 ALTER TABLE `account_type` DISABLE KEYS */;
INSERT INTO `account_type` VALUES (1,'Free'),(2,'Premium'),(3,'Enterprise'),(4,'Trial'),(5,'Student'),(6,'Family'),(7,'Business'),(8,'Group'),(9,'Lifetime'),(10,'Monthly'),(11,'Yearly'),(12,'Gold'),(13,'Silver'),(14,'Bronze'),(15,'Professional'),(16,'Standard'),(17,'VIP'),(18,'Basic'),(19,'Plus'),(20,'Deluxe');
/*!40000 ALTER TABLE `account_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `billing`
--

DROP TABLE IF EXISTS `billing`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `billing` (
  `billing_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `billing_amount` decimal(10,2) DEFAULT NULL,
  `billing_date` date DEFAULT NULL,
  PRIMARY KEY (`billing_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `billing_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `billing`
--

LOCK TABLES `billing` WRITE;
/*!40000 ALTER TABLE `billing` DISABLE KEYS */;
INSERT INTO `billing` VALUES (1,1,15.99,'2024-09-01'),(2,2,25.99,'2024-09-01'),(3,3,15.99,'2024-09-01'),(4,4,15.99,'2024-09-01'),(5,5,29.99,'2024-10-01'),(6,6,19.99,'2024-10-01'),(7,7,35.99,'2024-10-01'),(8,8,24.99,'2024-10-01'),(9,9,14.99,'2024-10-01'),(10,10,19.99,'2024-10-01'),(11,11,29.99,'2024-10-01'),(12,12,15.99,'2024-10-01'),(13,13,22.99,'2024-10-01'),(14,14,18.99,'2024-10-01'),(15,15,14.99,'2024-10-01'),(16,16,32.99,'2024-10-01'),(17,17,27.99,'2024-10-01'),(18,18,15.99,'2024-10-01'),(19,19,24.99,'2024-10-01'),(20,20,19.99,'2024-10-01');
/*!40000 ALTER TABLE `billing` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chat_session`
--

DROP TABLE IF EXISTS `chat_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chat_session` (
  `session_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `start_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  `chat_log` text,
  PRIMARY KEY (`session_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `chat_session_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chat_session`
--

LOCK TABLES `chat_session` WRITE;
/*!40000 ALTER TABLE `chat_session` DISABLE KEYS */;
INSERT INTO `chat_session` VALUES (1,1,'2024-10-05 09:00:00','2024-10-05 09:15:00','Hi Sarah, how are you feeling today?'),(2,2,'2024-10-05 10:00:00','2024-10-05 10:30:00','Hello John, let’s work through your day'),(3,3,'2024-10-06 14:00:00','2024-10-06 14:20:00','Hi Rachel, how can I assist you today?'),(4,4,'2024-10-06 15:00:00','2024-10-06 15:10:00','Hi David, let’s talk about your mood'),(5,5,'2024-10-07 08:00:00','2024-10-07 08:30:00','Good morning Lisa, how was your sleep?'),(6,6,'2024-10-07 09:00:00','2024-10-07 09:10:00','Hey Tom, what\'s on your mind today?'),(7,7,'2024-10-07 10:00:00','2024-10-07 10:15:00','Emma, any challenges recently?'),(8,8,'2024-10-08 11:00:00','2024-10-08 11:25:00','Mark, let’s check on your progress'),(9,9,'2024-10-08 12:00:00','2024-10-08 12:30:00','Susan, tell me how you’re doing'),(10,10,'2024-10-08 13:00:00','2024-10-08 13:20:00','Chris, let’s reflect on last week'),(11,11,'2024-10-09 08:00:00','2024-10-09 08:20:00','Laura, any updates on your goals?'),(12,12,'2024-10-09 09:00:00','2024-10-09 09:25:00','Nancy, let’s discuss your progress'),(13,13,'2024-10-09 10:00:00','2024-10-09 10:15:00','Peter, how’s your mood today?'),(14,14,'2024-10-10 11:00:00','2024-10-10 11:30:00','Jessica, any recent stress?'),(15,15,'2024-10-10 12:00:00','2024-10-10 12:20:00','Paul, how can I help you today?'),(16,16,'2024-10-10 13:00:00','2024-10-10 13:25:00','Anna, let’s chat about work'),(17,17,'2024-10-11 08:00:00','2024-10-11 08:20:00','Robert, checking in on you'),(18,18,'2024-10-11 09:00:00','2024-10-11 09:10:00','Mary, any highs or lows?'),(19,19,'2024-10-11 10:00:00','2024-10-11 10:30:00','Linda, what’s new with you?'),(20,20,'2024-10-11 11:00:00','2024-10-11 11:25:00','George, tell me about your weekend');
/*!40000 ALTER TABLE `chat_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `emotion_tracking`
--

DROP TABLE IF EXISTS `emotion_tracking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `emotion_tracking` (
  `emotion_id` int NOT NULL AUTO_INCREMENT,
  `session_id` int DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `mood` varchar(50) DEFAULT NULL,
  `mood_score` int DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`emotion_id`),
  KEY `session_id` (`session_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `emotion_tracking_ibfk_1` FOREIGN KEY (`session_id`) REFERENCES `chat_session` (`session_id`),
  CONSTRAINT `emotion_tracking_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `emotion_tracking`
--

LOCK TABLES `emotion_tracking` WRITE;
/*!40000 ALTER TABLE `emotion_tracking` DISABLE KEYS */;
INSERT INTO `emotion_tracking` VALUES (1,1,1,'Stressed',8,'2024-10-05 09:10:00'),(2,1,1,'Calm',4,'2024-10-05 09:12:00'),(3,2,2,'Anxious',9,'2024-10-05 10:15:00'),(4,3,3,'Happy',2,'2024-10-06 14:05:00'),(5,4,4,'Angry',7,'2024-10-06 15:03:00'),(6,5,5,'Relaxed',3,'2024-10-07 08:05:00'),(7,6,6,'Sad',6,'2024-10-07 09:03:00'),(8,7,7,'Neutral',5,'2024-10-07 10:05:00'),(9,8,8,'Excited',1,'2024-10-08 11:10:00'),(10,9,9,'Happy',2,'2024-10-08 12:15:00'),(11,10,10,'Calm',4,'2024-10-08 13:03:00'),(12,11,11,'Tense',7,'2024-10-09 08:04:00'),(13,12,12,'Sad',6,'2024-10-09 09:10:00'),(14,13,13,'Relaxed',3,'2024-10-09 10:05:00'),(15,14,14,'Happy',2,'2024-10-10 11:07:00'),(16,15,15,'Stressed',8,'2024-10-10 12:05:00'),(17,16,16,'Anxious',9,'2024-10-10 13:08:00'),(18,17,17,'Calm',4,'2024-10-11 08:10:00'),(19,18,18,'Tired',7,'2024-10-11 09:05:00'),(20,19,19,'Energized',1,'2024-10-11 10:15:00');
/*!40000 ALTER TABLE `emotion_tracking` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment`
--

DROP TABLE IF EXISTS `payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment` (
  `payment_id` int NOT NULL AUTO_INCREMENT,
  `billing_id` int DEFAULT NULL,
  `payment_amount` decimal(10,2) DEFAULT NULL,
  `payment_date` date DEFAULT NULL,
  PRIMARY KEY (`payment_id`),
  KEY `billing_id` (`billing_id`),
  CONSTRAINT `payment_ibfk_1` FOREIGN KEY (`billing_id`) REFERENCES `billing` (`billing_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment`
--

LOCK TABLES `payment` WRITE;
/*!40000 ALTER TABLE `payment` DISABLE KEYS */;
INSERT INTO `payment` VALUES (1,1,15.99,'2024-09-02'),(2,2,25.99,'2024-09-02'),(3,3,15.99,'2024-09-02'),(4,4,15.99,'2024-09-02'),(5,5,29.99,'2024-10-02'),(6,6,19.99,'2024-10-02'),(7,7,35.99,'2024-10-02'),(8,8,24.99,'2024-10-02'),(9,9,14.99,'2024-10-02'),(10,10,19.99,'2024-10-02'),(11,11,29.99,'2024-10-02'),(12,12,15.99,'2024-10-02'),(13,13,22.99,'2024-10-02'),(14,14,18.99,'2024-10-02'),(15,15,14.99,'2024-10-02'),(16,16,32.99,'2024-10-02'),(17,17,27.99,'2024-10-02'),(18,18,15.99,'2024-10-02'),(19,19,24.99,'2024-10-02'),(20,20,19.99,'2024-10-02');
/*!40000 ALTER TABLE `payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL,
  `username` varchar(50) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `account_type_id` int DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  KEY `account_type_id` (`account_type_id`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`account_type_id`) REFERENCES `account_type` (`account_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'SarahM','sarah@example.com','******',1),(2,'JohnD','john.doe@example.com','******',2),(3,'RachelK','rachelk@example.com','******',1),(4,'DavidS','david.s@example.com','******',1),(5,'LisaP','lisa.p@example.com','******',2),(6,'TomA','toma@example.com','******',1),(7,'EmmaJ','emma.j@example.com','******',2),(8,'MarkC','mark.c@example.com','******',1),(9,'SusanR','susan.r@example.com','******',2),(10,'ChrisL','chris.l@example.com','******',1),(11,'LauraG','laura.g@example.com','******',2),(12,'NancyH','nancy.h@example.com','******',1),(13,'PeterQ','peter.q@example.com','******',2),(14,'JessicaB','jessica.b@example.com','******',1),(15,'PaulF','paul.f@example.com','******',1),(16,'AnnaT','anna.t@example.com','******',2),(17,'RobertN','robert.n@example.com','******',1),(18,'MaryZ','mary.z@example.com','******',2),(19,'LindaV','linda.v@example.com','******',1),(20,'GeorgeK','george.k@example.com','******',2);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `utilization`
--

DROP TABLE IF EXISTS `utilization`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `utilization` (
  `utilization_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `data_usage` int DEFAULT NULL,
  `service_usage` int DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`utilization_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `utilization_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `utilization`
--

LOCK TABLES `utilization` WRITE;
/*!40000 ALTER TABLE `utilization` DISABLE KEYS */;
INSERT INTO `utilization` VALUES (1,1,500,30,'2024-10-05 09:20:00'),(2,2,1200,60,'2024-10-05 10:45:00'),(3,3,800,40,'2024-10-06 14:30:00'),(4,4,300,20,'2024-10-06 15:20:00'),(5,5,700,35,'2024-10-07 08:35:00'),(6,6,450,45,'2024-10-07 09:15:00'),(7,7,850,50,'2024-10-07 10:40:00'),(8,8,320,30,'2024-10-08 11:35:00'),(9,9,900,60,'2024-10-08 12:50:00'),(10,10,400,20,'2024-10-08 13:25:00'),(11,11,650,25,'2024-10-09 08:50:00'),(12,12,480,40,'2024-10-09 09:45:00'),(13,13,550,30,'2024-10-09 10:20:00'),(14,14,780,45,'2024-10-10 11:55:00'),(15,15,290,20,'2024-10-10 12:10:00'),(16,16,850,50,'2024-10-10 13:15:00'),(17,17,520,35,'2024-10-11 08:25:00'),(18,18,770,45,'2024-10-11 09:55:00'),(19,19,430,30,'2024-10-11 10:35:00'),(20,20,680,40,'2024-10-11 11:20:00');
/*!40000 ALTER TABLE `utilization` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-11-12 16:13:25
