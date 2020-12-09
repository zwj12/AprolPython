-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.5.6-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             11.0.0.5919
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

use BUR_PDA

-- Dumping structure for table bur_pda.robot-msgtype
CREATE TABLE IF NOT EXISTS BUR_PDA.`robot-msgtype` (
  `msg_type` int(11) NOT NULL,
  `msg_type_text` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`msg_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table bur_pda.robot-msgtype: ~2 rows (approximately)
/*!40000 ALTER TABLE `robot-msgtype` DISABLE KEYS */;
INSERT INTO BUR_PDA.`robot-msgtype` (`msg_type`, `msg_type_text`) VALUES
	(1, 'Information'),
	(2, 'Warning'),
	(3, 'Error');
/*!40000 ALTER TABLE `robot-msgtype` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
