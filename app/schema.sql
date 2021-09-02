DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS sectors;
DROP TABLE IF EXISTS sectors2;

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL

);
CREATE TABLE sectors (
  id_noms INTEGER PRIMARY KEY,
  object1 INTEGER,
  object2 TEXT,

  object3 VARCHAR(20),
  object4 INTEGER,
  object5 DATETIME
);
CREATE TRIGGER DOBDATETIME_voites AFTER INSERT ON sectors
BEGIN
  UPDATE sectors
  SET object5 = DATEtime('NOW')
  WHERE rowid = NEW.rowid;
END;


INSERT INTO users VALUES(1,'a','0cc175b9c0f1b6a831c399e269772661');
INSERT INTO users VALUES(2,'222','bcbe3365e6ac95ea2c0343a2395834dd');
INSERT INTO users VALUES(14,'555','bcbe3365e6ac95ea2c0343a2395834dd');

INSERT INTO sectors VALUES(1,10,'alldays','pole',4,'2020-02-12');
INSERT INTO sectors VALUES(4,14,'alldays','pole',1,'2020-02-23');
INSERT INTO sectors VALUES(2,11,'alldays','pole2',10,'2020-02-23');
INSERT INTO sectors VALUES(5,15,'alldays','pole2',10,'2020-02-23');
INSERT INTO sectors VALUES(3,12,'alldays','pole3',7,'2020-02-23');