DROP TABLE IF EXISTS User;

CREATE TABLE User (
  pseudo TEXT PRIMARY KEY NOT NULL,
  firstname TEXT NULL,
  lastname TEXT NULL,
  sexe TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  adress TEXT NULL,
  city TEXT NULL,
  postalcode TEXT NULL,
  phone TEXT NULL,
  datebirthday TEXT NOT NULL,
  password TEXT NOT NULL
);