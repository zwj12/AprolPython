Backup:
mysqldump -u buradmin -p.buradmin --database BUR_PDA > BUR_PDA.sql
mysqldump -u buradmin -p.buradmin BUR_PDA robot_elog > BUR_PDA.sql
mysqldump -u buradmin -p.buradmin BUR_PDA ABBRAAT-RobotPDA > BUR_PDA.sql

Restore:
use BUR_PDA;
mysql -u buradmin -p.buradmin < BUR_PDA.sql
mysql -h 10.0.2.2 -u root -p.root < BUR_PDA.sql
