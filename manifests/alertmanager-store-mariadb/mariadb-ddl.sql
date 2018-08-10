CREATE DATABASE alertmanager;

CREATE
	TABLE
		history(
			seq INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
			alert JSON,
			datetime VARCHAR(30)
		);

SET GLOBAL event_scheduler = ON;
SET @@global.event_scheduler = ON;
SET GLOBAL event_scheduler = 1;
SET @@global.event_scheduler = 1;

CREATE EVENT IF NOT EXISTS history
	ON SCHEDULE
		EVERY 1 DAY
		STARTS CURRENT_TIMESTAMP
	DO
		DELETE FROM history
		WHERE date_format(datetime, '%Y-%m-%d') <= date_sub(curdate(), INTERVAL 1 MONTH)
;
