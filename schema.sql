DROP TABLE IF EXISTS User;

CREATE TABLE User (
  pseudo TEXT PRIMARY KEY,
  firstname TEXT NULL,
  lastname TEXT NULL,
  sexe TEXT NULL,
  email TEXT NOT NULL,
  adress TEXT NULL,
  city TEXT NULL,
  postalcode TEXT NULL,
  phone TEXT NULL,
  datebirthday TEXT NULL,
  password TEXT NOT NULL
);