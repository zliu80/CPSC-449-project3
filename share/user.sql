PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE Users(username varchar(128) primary key, password varchar(128));
COMMIT;

