PRAGMA foreign_keys=off;

BEGIN TRANSACTION;

ALTER TABLE leaderboard RENAME TO leaderboard_old;

CREATE TABLE leaderboard(
  server varchar(20) NOT NULL,
  user varchar(20) NOT NULL,
  score int NOT NULL,
  collectionDate date NOT NULL,
  PRIMARY KEY (server, user)
  );

INSERT INTO leaderboard SELECT * FROM leaderboard_old;

ALTER TABLE assign_roles RENAME TO assign_roles_old;

CREATE TABLE assign_roles(
  server varchar(20) NOT NULL,
  role varchar(20) NOT NULL,
  PRIMARY KEY (role)
  );

INSERT INTO assign_roles SELECT * FROM assign_roles_old;

ALTER TABLE prefixes RENAME TO prefixes_old;

CREATE TABLE prefixes(
  server varchar(20) NOT NULL,
  prefix text NOT NULL,
  PRIMARY KEY (server)
  );

INSERT INTO prefixes SELECT * FROM prefixes_old;

ALTER TABLE server_settings RENAME TO server_settings_old;

CREATE TABLE server_settings(
  server varchar(20) NOT NULL,
  color_roles bool NOT NULL,
  PRIMARY KEY (server)
  );

INSERT INTO server_settings SELECT * FROM server_settings_old;

DROP TABLE leaderboard_old;
DROP TABLE assign_roles_old;
DROP TABLE prefixes_old;
DROP TABLE server_settings_old;

COMMIT;

PRAGMA foreign_keys=on;