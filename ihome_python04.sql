-- MySQL dump 10.13  Distrib 5.7.33, for Linux (x86_64)
--
-- Host: localhost    Database: ihome_python04
-- ------------------------------------------------------
-- Server version	5.7.33-0ubuntu0.18.04.1-log

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
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('701493f5e564');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ih_area_info`
--

DROP TABLE IF EXISTS `ih_area_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ih_area_info` (
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ih_area_info`
--

LOCK TABLES `ih_area_info` WRITE;
/*!40000 ALTER TABLE `ih_area_info` DISABLE KEYS */;
INSERT INTO `ih_area_info` VALUES (NULL,NULL,1,'西工区'),(NULL,NULL,2,'洛龙区'),(NULL,NULL,3,'涧西区'),(NULL,NULL,4,'老城区'),(NULL,NULL,5,'瀍河区'),(NULL,NULL,6,'吉利区'),(NULL,NULL,7,'新安县'),(NULL,NULL,8,'偃师市'),(NULL,NULL,9,'孟津县'),(NULL,NULL,10,'洛宁县'),(NULL,NULL,11,'宜阳县'),(NULL,NULL,12,'伊川县'),(NULL,NULL,13,'栾川县'),(NULL,NULL,14,'嵩县'),(NULL,NULL,15,'汝阳县');
/*!40000 ALTER TABLE `ih_area_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ih_facility_info`
--

DROP TABLE IF EXISTS `ih_facility_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ih_facility_info` (
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ih_facility_info`
--

LOCK TABLES `ih_facility_info` WRITE;
/*!40000 ALTER TABLE `ih_facility_info` DISABLE KEYS */;
INSERT INTO `ih_facility_info` VALUES (NULL,NULL,1,'无线网络'),(NULL,NULL,2,'热水淋浴'),(NULL,NULL,3,'空调'),(NULL,NULL,4,'暖气'),(NULL,NULL,5,'允许吸烟'),(NULL,NULL,6,'饮水设备'),(NULL,NULL,7,'牙具'),(NULL,NULL,8,'香皂'),(NULL,NULL,9,'拖鞋'),(NULL,NULL,10,'手纸'),(NULL,NULL,11,'毛巾'),(NULL,NULL,12,'沐浴露、洗发露'),(NULL,NULL,13,'冰箱'),(NULL,NULL,14,'洗衣机'),(NULL,NULL,15,'电梯'),(NULL,NULL,16,'允许做饭'),(NULL,NULL,17,'允许带宠物'),(NULL,NULL,18,'允许聚会'),(NULL,NULL,19,'门禁系统'),(NULL,NULL,20,'停车位'),(NULL,NULL,21,'有线网络'),(NULL,NULL,22,'电视'),(NULL,NULL,23,'浴缸');
/*!40000 ALTER TABLE `ih_facility_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ih_house_facility`
--

DROP TABLE IF EXISTS `ih_house_facility`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ih_house_facility` (
  `house_id` int(11) NOT NULL,
  `facility_id` int(11) NOT NULL,
  PRIMARY KEY (`house_id`,`facility_id`),
  KEY `facility_id` (`facility_id`),
  CONSTRAINT `ih_house_facility_ibfk_1` FOREIGN KEY (`facility_id`) REFERENCES `ih_facility_info` (`id`),
  CONSTRAINT `ih_house_facility_ibfk_2` FOREIGN KEY (`house_id`) REFERENCES `ih_house_info` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ih_house_facility`
--

LOCK TABLES `ih_house_facility` WRITE;
/*!40000 ALTER TABLE `ih_house_facility` DISABLE KEYS */;
INSERT INTO `ih_house_facility` VALUES (4,1),(5,1),(7,1),(8,1),(9,1),(10,1),(7,2),(8,2),(9,2),(4,3),(7,3),(8,3),(9,3),(10,3),(7,4),(8,4),(9,4),(4,5),(7,5),(8,5),(9,5),(10,5),(7,6),(8,6),(9,6),(4,7),(7,7),(8,7),(9,7),(10,7),(7,8),(8,8),(9,8),(7,9),(8,9),(9,9),(10,9),(7,10),(8,10),(9,10),(7,11),(8,11),(9,11),(10,11),(7,12),(8,12),(9,12),(7,13),(8,13),(9,13),(10,13),(7,14),(8,14),(9,14),(7,15),(8,15),(9,15),(10,15),(7,16),(8,16),(9,16),(7,17),(8,17),(9,17),(10,17),(7,18),(8,18),(9,18),(7,19),(8,19),(9,19),(10,19),(7,20),(8,20),(9,20),(7,21),(8,21),(9,21),(10,21),(7,22),(8,22),(9,22),(7,23),(8,23),(9,23);
/*!40000 ALTER TABLE `ih_house_facility` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ih_house_image`
--

DROP TABLE IF EXISTS `ih_house_image`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ih_house_image` (
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `house_id` int(11) NOT NULL,
  `url` varchar(256) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `house_id` (`house_id`),
  CONSTRAINT `ih_house_image_ibfk_1` FOREIGN KEY (`house_id`) REFERENCES `ih_house_info` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ih_house_image`
--

LOCK TABLES `ih_house_image` WRITE;
/*!40000 ALTER TABLE `ih_house_image` DISABLE KEYS */;
INSERT INTO `ih_house_image` VALUES ('2020-04-27 19:47:27','2020-04-27 19:47:27',4,4,'home01.jpg'),('2020-04-27 19:48:45','2020-04-27 19:48:45',5,5,'home02.jpg'),('2020-04-27 20:02:09','2020-04-27 20:02:09',6,6,'home03.jpg'),('2020-04-28 19:18:44','2020-04-28 19:18:44',7,7,'FsxYqPJ-fJtVZZH2LEshL7o9Ivxn'),('2020-04-28 19:18:53','2020-04-28 19:18:53',8,7,'FsHyv4WUHKUCpuIRftvwSO_FJWOG'),('2020-04-28 19:19:02','2020-04-28 19:19:02',9,7,'FoZg1QLpRi4vckq_W3tBBQe1wJxn'),('2020-04-30 23:11:36','2020-04-30 23:11:36',10,8,'Fhn6_ENlkRXOIPUlMvK66GAY836_'),('2020-04-30 23:11:43','2020-04-30 23:11:43',11,8,'FkFswoyU5CndfVshYLVIZ3CkKfC1'),('2020-04-30 23:11:51','2020-04-30 23:11:51',12,8,'FqqQyz-SrIOzASzCq2tiXYk3Lpnt'),('2020-04-30 23:15:33','2020-04-30 23:15:33',13,9,'FjVUatl5pGu2MUkP8S5DGTsxnTMv'),('2020-04-30 23:15:38','2020-04-30 23:15:38',14,9,'FjVUatl5pGu2MUkP8S5DGTsxnTMv'),('2020-04-30 23:15:46','2020-04-30 23:15:46',15,9,'Fswz9BZVMQKsSSpKBEfXCpBaV5y6'),('2020-04-30 23:15:53','2020-04-30 23:15:53',16,9,'FtEehcMf4VF1pI3Ev4iix4eIXW26'),('2021-03-24 20:04:35','2021-03-24 20:04:35',17,10,'2021-03-2408:04:34PM');
/*!40000 ALTER TABLE `ih_house_image` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ih_house_info`
--

DROP TABLE IF EXISTS `ih_house_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ih_house_info` (
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `area_id` int(11) NOT NULL,
  `title` varchar(64) NOT NULL,
  `price` int(11) DEFAULT NULL,
  `address` varchar(512) DEFAULT NULL,
  `room_count` int(11) DEFAULT NULL,
  `acreage` int(11) DEFAULT NULL,
  `unit` varchar(32) DEFAULT NULL,
  `capacity` int(11) DEFAULT NULL,
  `beds` varchar(64) DEFAULT NULL,
  `deposit` int(11) DEFAULT NULL,
  `min_days` int(11) DEFAULT NULL,
  `max_days` int(11) DEFAULT NULL,
  `order_count` int(11) DEFAULT NULL,
  `index_image_url` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `area_id` (`area_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `ih_house_info_ibfk_1` FOREIGN KEY (`area_id`) REFERENCES `ih_area_info` (`id`),
  CONSTRAINT `ih_house_info_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `ih_user_profile` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ih_house_info`
--

LOCK TABLES `ih_house_info` WRITE;
/*!40000 ALTER TABLE `ih_house_info` DISABLE KEYS */;
INSERT INTO `ih_house_info` VALUES ('2020-04-27 19:47:09','2020-04-30 17:24:25',4,3,1,'ws',52100,'521',521,521,'521',2,'521',522100,1,5,2,'home01.jpg'),('2020-04-27 19:48:39','2020-04-30 21:18:57',5,3,1,'www',1100,'11',11,11,'11',11,'11',1100,11,11,1,'home02.jpg'),('2020-04-27 20:02:03','2021-03-24 20:14:06',6,3,1,'wsaa',5500,'442',12,555,'455',555,'55',55500,55,555,1,'home03.jpg'),('2020-04-28 19:18:33','2020-04-30 01:21:05',7,3,2,'宜家',35000,'西城区长安大道71号',3,123,'四室两厅',5,'双人床*3',50000,2,7,1,'home04.jpg'),('2020-04-30 23:09:46','2020-04-30 23:11:36',8,3,3,'总统套房',9999900,'希望路38号帝国大酒店',55,500,'啥都有',100,'全套',999900,1,30,0,'home05.jpg'),('2020-04-30 23:15:24','2020-05-01 11:45:01',9,3,4,'女神屋子',999900,'仙女路27号',60,300,'四层八厅',5,'粉色5*5',666600,1,3,1,'home06.jpg'),('2021-03-24 20:03:01','2021-03-24 20:04:35',10,5,7,'情侣套房',99900,'城关镇201号',6,120,'大床房',2,'大床 大电视 高速宽带',5000,2,45,0,'2021-03-2408:04:34PM');
/*!40000 ALTER TABLE `ih_house_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ih_order_info`
--

DROP TABLE IF EXISTS `ih_order_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ih_order_info` (
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `house_id` int(11) NOT NULL,
  `begin_date` datetime NOT NULL,
  `end_date` datetime NOT NULL,
  `days` int(11) NOT NULL,
  `house_price` int(11) NOT NULL,
  `amount` int(11) NOT NULL,
  `status` enum('WAIT_ACCEPT','WAIT_PAYMENT','PAID','WAIT_COMMENT','COMPLETE','CANCELED','REJECTED') DEFAULT NULL,
  `comment` text,
  `trade_no` varchar(80) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `house_id` (`house_id`),
  KEY `user_id` (`user_id`),
  KEY `ix_ih_order_info_status` (`status`),
  CONSTRAINT `ih_order_info_ibfk_1` FOREIGN KEY (`house_id`) REFERENCES `ih_house_info` (`id`),
  CONSTRAINT `ih_order_info_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `ih_user_profile` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=100003 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ih_order_info`
--

LOCK TABLES `ih_order_info` WRITE;
/*!40000 ALTER TABLE `ih_order_info` DISABLE KEYS */;
INSERT INTO `ih_order_info` VALUES ('2021-03-24 20:06:04','2021-03-24 20:14:06',100001,5,6,'2021-03-25 00:00:00','2021-03-25 00:00:00',1,5500,5500,'COMPLETE','傻逼   真恶心\n','2021032422001469920501167099'),('2021-03-24 20:10:34','2021-03-24 20:12:21',100002,5,9,'2021-03-26 00:00:00','2021-03-27 00:00:00',2,999900,1999800,'REJECTED','傻逼  不让你住',NULL);
/*!40000 ALTER TABLE `ih_order_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ih_user_profile`
--

DROP TABLE IF EXISTS `ih_user_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ih_user_profile` (
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `password_hash` varchar(128) NOT NULL,
  `mobile` varchar(11) NOT NULL,
  `real_name` varchar(32) DEFAULT NULL,
  `id_card` varchar(20) DEFAULT NULL,
  `avatar_url` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mobile` (`mobile`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ih_user_profile`
--

LOCK TABLES `ih_user_profile` WRITE;
/*!40000 ALTER TABLE `ih_user_profile` DISABLE KEYS */;
INSERT INTO `ih_user_profile` VALUES ('2020-04-24 14:25:15','2020-04-24 14:25:15',1,'15225433211','pbkdf2:sha256:50000$A92qtBQO$41e098b55e8696bd2fb60220054941bba477c9f26c2849f67064311256b0d024','15225433211',NULL,NULL,NULL),('2020-04-24 16:07:49','2020-04-24 16:07:49',2,'15225433112','pbkdf2:sha256:50000$lbdPOyRu$e5fc2dc95e6ad73ef19b42aa7306ccc9db2a362dc91f4589ba25eb39f70aa7d3','15225433112',NULL,NULL,NULL),('2020-04-24 17:09:00','2020-04-26 14:20:36',3,'ws','pbkdf2:sha256:50000$Y2AnWEN8$1bbd299ca4e12a16fdd4364afad0af203fa62630674487f31890eeb957c6a9dc','15225433210','王某某','410111111111111111','FmT-Qpi7yYr_2GHYOnS6n4r5h8jY'),('2020-04-28 15:14:09','2020-04-30 21:19:40',4,'15539128795','pbkdf2:sha256:50000$f3FO5JSk$dca4aeae4e07d6c1866d60350e8a7c6ff13fe85ac82337d864ee616a60886f3e','15539128795',NULL,NULL,'FpAdLunWJfW-VwzqgwlJCckmjqDp'),('2021-03-24 18:50:20','2021-03-24 20:01:16',5,'张文武','pbkdf2:sha256:50000$Ln9ptpjs$650120bd8f8bb2d5bccf618ab2bee28eeb2d22b393900bb28bc81d1cf382e84d','15539128797','王某某','410111111111111111','2021-03-2407:58:18PM');
/*!40000 ALTER TABLE `ih_user_profile` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-03-24 20:41:34
