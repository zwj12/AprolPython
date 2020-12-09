-- mysql -u buradmin -p.buradmin < /home/engin/Documents/AprolPython/ABBRAAT-PLCPDA.sql
-- DROP TABLE BUR_PDA.`ABBRAAT-PLCPDA`;

CREATE TABLE IF NOT EXISTS BUR_PDA.`ABBRAAT-PLCPDA`
(
   ts datetime(6) DEFAULT NULL,
   ts_switch_mark varchar(1) DEFAULT NULL,
   project varchar(100) DEFAULT NULL,
   instance varchar(100) DEFAULT NULL,
   rec_rate varchar(100) DEFAULT NULL,
   equip_id varchar(100) DEFAULT NULL,
   ip_address varchar(64) DEFAULT NULL,
   connected BIT DEFAULT NULL,
   state_num integer UNSIGNED DEFAULT NULL,
   station_name varchar(64) DEFAULT NULL,
   line_name varchar(64) DEFAULT NULL,
   workshop_name varchar(64) DEFAULT NULL,
   station_status integer DEFAULT NULL,
   alarm BIT DEFAULT NULL,
   alarm_code integer UNSIGNED DEFAULT NULL,
   product_name varchar(64) DEFAULT NULL,
   program_number integer UNSIGNED DEFAULT NULL,
   product_count integer UNSIGNED DEFAULT NULL,
   executing_time integer UNSIGNED DEFAULT NULL,
   UNIQUE KEY `uniq_PLCPDA`(ts, instance, ip_address,connected,state_num,station_name,line_name,workshop_name,station_status,alarm,alarm_code,product_name,program_number,product_count,executing_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
