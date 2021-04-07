DROP TABLE IF EXISTS User;

CREATE TABLE User (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  pseudo TEXT NOT NULL,
  firstname TEXT NULL,
  lastname TEXT NULL,
  sexe TEXT NULL,
  email TEXT NOT NULL,
  adress TEXT NULL,
  city TEXT NULL,
  postalcode TEXT NULL,
  phone TEXT NULL,
  datebirthday DATE NULL,
  password TEXT NOT NULL
);