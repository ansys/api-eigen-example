DROP TABLE IF EXISTS eigen_db;
DROP TABLE IF EXISTS types;

CREATE TABLE types (
  eigen_type TEXT NOT NULL,
  PRIMARY KEY (eigen_type)
);

CREATE TABLE eigen_db (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  eigen_type TEXT NOT NULL,
  eigen_value TEXT NOT NULL,
  FOREIGN KEY (eigen_type) REFERENCES types (eigen_type)
);

INSERT INTO types (eigen_type) VALUES ('VECTOR');
INSERT INTO types (eigen_type) VALUES ('MATRIX');
