-- mysql -u buradmin -p.buradmin < /home/engin/Documents/AprolPython/ABBRAAT-RobotPDA.sql
-- DROP TABLE BUR_PDA.`ABBRAAT-RobotPDA`;

CREATE TABLE IF NOT EXISTS BUR_PDA.`ABBRAAT-RobotPDA`
(
   ts datetime(6) DEFAULT NULL,
   ts_switch_mark varchar(1) DEFAULT NULL,
   project varchar(100) DEFAULT NULL,
   instance varchar(100) DEFAULT NULL,
   rec_rate varchar(100) DEFAULT NULL,
   equip_id varchar(100) DEFAULT NULL,
   ip_address varchar(64) DEFAULT NULL,
   serial_number varchar(64) DEFAULT NULL,
   controller_name varchar(64) DEFAULT NULL,
   system_name varchar(64) DEFAULT NULL,
   robot_ware varchar(64) DEFAULT NULL,
   operating_mode varchar(64) DEFAULT NULL,
   controller_state varchar(64) DEFAULT NULL,
   execution_state varchar(64) DEFAULT NULL,
   run_mode varchar(64) DEFAULT NULL,
   operating_mode_code integer DEFAULT NULL,
   controller_state_code integer DEFAULT NULL,
   execution_state_code integer DEFAULT NULL,
   run_mode_code integer DEFAULT NULL,
   speed_ratio integer DEFAULT NULL,
   task_executing BIT DEFAULT NULL,
   pf_idle1 BIT DEFAULT NULL,
   pf_executing1 BIT DEFAULT NULL,
   pf_active_order1 integer DEFAULT NULL,
   pf_is_service1 BIT DEFAULT NULL,
   part_count integer DEFAULT NULL,
   executing_time integer DEFAULT NULL,
   UNIQUE KEY `uniq_RobotPDA`(ts, instance, ip_address,serial_number,controller_name,system_name,robot_ware,operating_mode,controller_state,execution_state,run_mode,operating_mode_code,controller_state_code,execution_state_code,run_mode_code,speed_ratio,task_executing,pf_idle1,pf_executing1,pf_active_order1,pf_is_service1,part_count,executing_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
