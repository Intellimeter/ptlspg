-- MySQL dump 10.13  Distrib 5.1.61, for Win64 (unknown)
--
-- Host: localhost    Database: ptls
-- ------------------------------------------------------
-- Server version	5.1.61-community

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
-- Table structure for table `accum`
--

DROP TABLE IF EXISTS `accum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `accum` (
  `SN` int(10) unsigned NOT NULL DEFAULT '0',
  `ReadDate` int(10) unsigned NOT NULL DEFAULT '0',
  `RealReadDate` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `TCh1` bigint(20) unsigned DEFAULT '0',
  `TCh2` bigint(20) unsigned DEFAULT '0',
  `TCh3` bigint(20) unsigned DEFAULT '0',
  `TCh4` bigint(20) unsigned DEFAULT '0',
  `TCh5` bigint(20) unsigned DEFAULT '0',
  `TCh6` bigint(20) unsigned DEFAULT '0',
  `TCh7` bigint(20) unsigned DEFAULT '0',
  `TCh8` bigint(20) unsigned DEFAULT '0',
  PRIMARY KEY (`SN`,`RealReadDate`),
  KEY `SN` (`SN`,`ReadDate`),
  KEY `RealReadDate` (`RealReadDate`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dials`
--

DROP TABLE IF EXISTS `dials`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dials` (
  `SN` int(10) unsigned NOT NULL DEFAULT '0',
  `ReadDate` int(10) unsigned NOT NULL DEFAULT '0',
  `RealReadDate` datetime DEFAULT NULL,
  `Ch1` mediumint(8) unsigned DEFAULT '0',
  `Ch2` mediumint(8) unsigned DEFAULT '0',
  `Ch3` mediumint(8) unsigned DEFAULT '0',
  `Ch4` mediumint(8) unsigned DEFAULT '0',
  `Ch5` mediumint(8) unsigned DEFAULT '0',
  `Ch6` mediumint(8) unsigned DEFAULT '0',
  `Ch7` mediumint(8) unsigned DEFAULT '0',
  `Ch8` mediumint(8) unsigned DEFAULT '0',
  `Confirmed` tinyint(3) unsigned DEFAULT '0',
  PRIMARY KEY (`SN`,`ReadDate`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `ins_accum` AFTER INSERT ON `dials` FOR EACH ROW
	BEGIN
	IF NEW.RealReadDate > '2010-01-01 00:00:00' THEN
		UPDATE gross SET ReadDate=NEW.ReadDate, RealReadDate=NEW.RealReadDate, TCh1=NEW.Ch1+TCh1, TCh2=NEW.Ch2+TCh2, TCh3=NEW.Ch3+TCh3, TCh4=NEW.Ch4+TCh4, TCh5=NEW.Ch5+TCh5, TCh6=NEW.Ch6+TCh6, TCh7=NEW.Ch7+TCh7, TCh8=NEW.Ch8+TCh8 WHERE ReadDate < NEW.ReadDate AND SN=NEW.SN ; 
		select row_count() into @rowcount1;
		if @rowcount1 < 1 then
			insert into gross( sn, readdate, realreaddate, tch1, tch2, tch3, tch4, tch5, tch6, tch7, tch8, LastRead, mLastRead) value (new.sn, new.readdate, new.realreaddate, new.ch1, new.ch2, new.ch3, new.ch4, new.ch5, new.ch6, new.ch7, new.ch8, '2010-1-1 00:00:00', '2010-1-1 00:00:00') ;
		end if;
		INSERT INTO accum SELECT SN, ReadDate, RealReadDate, TCh1, TCh2, TCh3, TCh4, TCh5, TCh6, TCh7, TCh8 FROM gross WHERE SN=NEW.SN ;
	END IF ;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `gross`
--

DROP TABLE IF EXISTS `gross`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gross` (
  `SN` int(10) unsigned NOT NULL DEFAULT '0',
  `ReadDate` int(10) unsigned NOT NULL DEFAULT '0',
  `RealReadDate` datetime DEFAULT NULL,
  `TCh1` bigint(20) unsigned DEFAULT '0',
  `TCh2` bigint(20) unsigned DEFAULT '0',
  `TCh3` bigint(20) unsigned DEFAULT '0',
  `TCh4` bigint(20) unsigned DEFAULT '0',
  `TCh5` bigint(20) unsigned DEFAULT '0',
  `TCh6` bigint(20) unsigned DEFAULT '0',
  `TCh7` bigint(20) unsigned DEFAULT '0',
  `TCh8` bigint(20) unsigned DEFAULT '0',
  `LastRead` datetime DEFAULT NULL,
  `mLastRead` datetime DEFAULT NULL,
  PRIMARY KEY (`SN`),
  KEY `SN` (`SN`,`ReadDate`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `info`
--

DROP TABLE IF EXISTS `info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `info` (
  `SN` int(10) unsigned NOT NULL,
  `chan` tinyint(3) unsigned NOT NULL,
  `descpt` varchar(100) DEFAULT NULL,
  `mtpr` double NOT NULL,
  `utility` varchar(20) NOT NULL,
  `unit` varchar(20) NOT NULL,
  PRIMARY KEY (`SN`,`chan`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `info_bkup`
--

DROP TABLE IF EXISTS `info_bkup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `info_bkup` (
  `SN` int(10) unsigned NOT NULL,
  `chan` tinyint(3) unsigned NOT NULL,
  `descpt` varchar(100) DEFAULT NULL,
  `mtpr` double NOT NULL,
  `utility` varchar(20) NOT NULL,
  `unit` varchar(20) NOT NULL,
  PRIMARY KEY (`SN`,`chan`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pdl`
--

DROP TABLE IF EXISTS `pdl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pdl` (
  `SN` int(10) unsigned NOT NULL DEFAULT '0',
  `Name` char(255) DEFAULT '',
  `Mode` tinyint(3) unsigned DEFAULT '0',
  `ConnectAddr` char(50) DEFAULT '',
  `Status` tinyint(3) unsigned DEFAULT '0',
  `SiteID` mediumint(5) unsigned DEFAULT '0',
  `LastReadAddr` int(8) DEFAULT '-1',
  `LastReadAddrBak` int(8) DEFAULT '-1',
  `DeviceName` char(64) DEFAULT '',
  PRIMARY KEY (`SN`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sites`
--

DROP TABLE IF EXISTS `sites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sites` (
  `ID` mediumint(5) unsigned DEFAULT '0',
  `Name` char(32) DEFAULT '',
  `Address` char(32) DEFAULT '',
  `City` char(32) DEFAULT '',
  `State` char(2) DEFAULT '',
  `Country` char(32) DEFAULT '',
  `ZIP` char(6) DEFAULT '',
  `Phone` char(50) DEFAULT '',
  `Status` tinyint(3) unsigned DEFAULT '0',
  `TimeSync` tinyint(3) unsigned DEFAULT '0',
  `TimeZone` smallint(6) DEFAULT '-1'
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tmp`
--

DROP TABLE IF EXISTS `tmp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tmp` (
  `SN` int(10) unsigned NOT NULL DEFAULT '0',
  `ReadDate` int(10) unsigned NOT NULL DEFAULT '0',
  `RealReadDate` datetime DEFAULT NULL,
  `Ch1` mediumint(8) unsigned DEFAULT '0',
  `Ch2` mediumint(8) unsigned DEFAULT '0',
  `Ch3` mediumint(8) unsigned DEFAULT '0',
  `Ch4` mediumint(8) unsigned DEFAULT '0',
  `Ch5` mediumint(8) unsigned DEFAULT '0',
  `Ch6` mediumint(8) unsigned DEFAULT '0',
  `Ch7` mediumint(8) unsigned DEFAULT '0',
  `Ch8` mediumint(8) unsigned DEFAULT '0',
  `Confirmed` tinyint(3) unsigned DEFAULT '0',
  PRIMARY KEY (`SN`,`ReadDate`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-05-17 15:39:16
