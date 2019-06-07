--CREATE SEQUENCE global_serial MINVALUE 0 START 0;
--DROP SEQUENCE global_serial;

-- CZYSZCZENIE 
 drop table if exists "global_ids" cascade;
 drop table if exists "member" cascade;
 drop table if exists "authority" cascade;
 drop table if exists "action" cascade;
 drop table if exists "vote" cascade;
 drop table if exists "project" cascade;
 drop role  if exists app;
 drop extension if exists pgcrypto;
-- RESZTA


CREATE EXTENSION pgcrypto;


CREATE TABLE global_ids (
  ID            bigint NOT NULL, 
  PRIMARY KEY (ID));

CREATE TABLE member (
  ID            bigint NOT NULL, 
  leader        bool NOT NULL, 
  activity      bool NOT NULL, 
  password      varchar(128) NOT NULL, 
  activity_date timestamp NOT NULL, 
  PRIMARY KEY (ID));
  
CREATE TABLE vote (
  ID        bigint NOT NULL, 
  value     bool NOT NULL, 
  vote_date timestamp NOT NULL, 
  memberID  bigint NOT NULL, 
  actionID  bigint NOT NULL, 
  PRIMARY KEY (ID));
  
CREATE TABLE project (
  ID            bigint NOT NULL, 
  --creation_date timestamp NOT NULL, 
  authorityID   bigint NOT NULL, 
  PRIMARY KEY (ID));
  
CREATE TABLE authority (
  ID   bigint NOT NULL, 
  PRIMARY KEY (ID));
  
CREATE TABLE action (
  ID             bigint NOT NULL, 
  type           varchar(255) NOT NULL, 
  --action_date    timestamp NOT NULL, 
  memberID       bigint NOT NULL, 
  projectID      bigint NOT NULL, 
  positive_votes bigint DEFAULT 0 NOT NULL, 
  negative_votes bigint DEFAULT 0 NOT NULL, 
  PRIMARY KEY (ID));
  

ALTER TABLE vote ADD CONSTRAINT "member can vote" FOREIGN KEY (memberID) REFERENCES member (ID);
ALTER TABLE project ADD CONSTRAINT "authority owns projects" FOREIGN KEY (authorityID) REFERENCES authority (ID);
ALTER TABLE action ADD CONSTRAINT " member has action" FOREIGN KEY (memberID) REFERENCES member (ID);
ALTER TABLE action ADD CONSTRAINT "project has actions" FOREIGN KEY (projectID) REFERENCES project (ID);
ALTER TABLE vote ADD CONSTRAINT "votes for action" FOREIGN KEY (actionID) REFERENCES action (ID);


CREATE user app WITH encrypted password 'qwerty';

GRANT INSERT ON global_ids TO app; 
GRANT INSERT ON member TO app; 
GRANT INSERT ON vote TO app; 
GRANT INSERT ON project TO app; 
GRANT INSERT ON authority TO app; 
GRANT INSERT ON action TO app; 

GRANT UPDATE ON global_ids TO app; 
GRANT UPDATE ON member TO app; 
GRANT UPDATE ON vote TO app; 
GRANT UPDATE ON project TO app; 
GRANT UPDATE ON authority TO app; 
GRANT UPDATE ON action TO app; 

GRANT SELECT ON global_ids TO app; 
GRANT SELECT ON member TO app; 
GRANT SELECT ON vote TO app; 
GRANT SELECT ON project TO app; 
GRANT SELECT ON authority TO app; 
GRANT SELECT ON action TO app; 
