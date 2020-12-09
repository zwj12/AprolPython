-- mysql -u buradmin -p.buradmin < /home/engin/Documents/AprolPython/Robot-Elog.sql
-- DROP TABLE `Robot-Elog`;

CREATE TABLE IF NOT EXISTS BUR_PDA.`Robot-Elog`
(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, 
    ip_address varchar(64) DEFAULT NULL,
    serial_number varchar(64) DEFAULT NULL,
    controller_name varchar(64) DEFAULT NULL,
    system_name varchar(64) DEFAULT NULL,
    sysid char(36) DEFAULT NULL,
    tstamp datetime DEFAULT NULL,
    elogseqnum integer DEFAULT NULL,
    title varchar(255) DEFAULT NULL,
    code integer DEFAULT NULL,
    msg_type integer DEFAULT NULL,
    UNIQUE KEY `uniq_RobotElog`(ip_address, serial_number, tstamp, controller_name, system_name, sysid, elogseqnum, title, code, msg_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
