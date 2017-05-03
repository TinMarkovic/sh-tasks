CREATE TABLE crew (
    id              SERIAL PRIMARY KEY,
    full_name       VARCHAR(100) NOT NULL,
    arrival_date    TIMESTAMP
);

CREATE TABLE aircraft (
    id       SERIAL PRIMARY KEY,
    name     VARCHAR(100) NOT NULL
);

CREATE TABLE aircraft_crew (
    id              SERIAL PRIMARY KEY,
    aircraft_id     INTEGER REFERENCES aircraft,
    crew_id         INTEGER REFERENCES crew,
    date_assigned   TIMESTAMP,
    date_removed    TIMESTAMP
);

/* Some random entries for query testing */
INSERT INTO crew(full_name, arrival_date) VALUES ('Mike Pence', 'YESTERDAY');
INSERT INTO crew(full_name, arrival_date) VALUES ('Barack Obama', 'NOW');
INSERT INTO crew(full_name, arrival_date) VALUES ('Donald Trump', 'TOMORROW');
INSERT INTO crew(full_name, arrival_date) VALUES ('Hillary Clinton', 'TODAY');
INSERT INTO aircraft(name) VALUES ('Leopard');
INSERT INTO aircraft(name) VALUES ('Lion');
INSERT INTO aircraft(name) VALUES ('Lark');
INSERT INTO aircraft_crew(aircraft_id, crew_id, date_assigned) VALUES (1,1,'YESTERDAY');
INSERT INTO aircraft_crew(aircraft_id, crew_id, date_assigned) VALUES (1,2,'NOW');
INSERT INTO aircraft_crew(aircraft_id, crew_id, date_assigned) VALUES (2,2,'TOMORROW');
INSERT INTO aircraft_crew(aircraft_id, crew_id, date_assigned) VALUES (3,2,'TODAY');
INSERT INTO aircraft_crew(aircraft_id, crew_id, date_assigned) VALUES (1,3,'YESTERDAY');

SELECT full_name FROM crew ORDER BY arrival_date LIMIT 1; /* Oldest */
SELECT full_name FROM crew ORDER BY arrival_date LIMIT 1 OFFSET 3; /* Third oldest */
SELECT full_name FROM crew ORDER BY (SELECT COUNT(*) FROM aircraft_crew WHERE aircraft_crew.crew_id = crew.id) DESC LIMIT 1; /* Most experienced */
SELECT full_name FROM crew ORDER BY (SELECT COUNT(*) FROM aircraft_crew WHERE aircraft_crew.crew_id = crew.id) LIMIT 1; /* Least experienced */