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
  password TEXT NOT NULL,
  temporarypassword TEXT
  isadmin TEXT
);

DROP TABLE IF EXISTS Category;

CREATE TABLE "Category" (
	"name"	TEXT NOT NULL UNIQUE,
	"main_category"	TEXT,
	PRIMARY KEY("name"),
	FOREIGN KEY("main_category") REFERENCES "Main_categories"("name")
);

DROP TABLE IF EXISTS Main_categories;

CREATE TABLE Main_categories (
  name TEXT PRIMARY KEY NOT NULL UNIQUE
);

DROP TABLE IF EXISTS Product;

CREATE TABLE Product (
  id INTEGER NOT NULL UNIQUE,
  name TEXT NOT NULL UNIQUE,
  category TEXT,
  price REAL,
  image TEXT,
  description TEXT,
  PRIMARY KEY(id AUTOINCREMENT),
  FOREIGN KEY(category) REFERENCES Category(name)
);

DROP TABLE IF EXISTS Card;

CREATE TABLE Card (
	id INTEGER NOT NULL UNIQUE,
  user TEXT NOT NULL,
  product TEXT NOT NULL,
	PRIMARY KEY(id AUTOINCREMENT),
  FOREIGN KEY(user) REFERENCES User(pseudo),
  FOREIGN KEY(product) REFERENCES Product(name)
);