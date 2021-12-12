-- CREATE ROLE

DO
$do$
    BEGIN
        IF NOT EXISTS(
            SELECT FROM pg_catalog.pg_roles
            WHERE rolname = 'meteodba') THEN

            CREATE ROLE meteodba LOGIN PASSWORD 'meteodba123'
            NOSUPERUSER NOCREATEDB NOCREATEROLE
            REPLICATION
            VALID UNTIL 'infinity';
        END IF;
    END
$do$;

-- COUNTRIES

CREATE TABLE countries (
   ctr_id SERIAL PRIMARY KEY,
   country_name text NOT NULL UNIQUE
);

ALTER TABLE countries OWNER TO meteodba;

INSERT INTO countries (country_name) VALUES ('Ireland');
INSERT INTO countries (country_name) VALUES ('England');
INSERT INTO countries (country_name) VALUES ('Germany');
INSERT INTO countries (country_name) VALUES ('France');


-- CITIES

CREATE TABLE cities (
   cit_id SERIAL PRIMARY KEY,
   ctr_id integer NOT NULL,
   city_name text NOT NULL
);

ALTER TABLE cities
   ADD FOREIGN KEY (ctr_id) REFERENCES countries ON DELETE CASCADE;

CREATE INDEX ctr_id_idx ON cities (ctr_id);

ALTER TABLE cities OWNER TO meteodba;

INSERT INTO cities (ctr_id, city_name) VALUES ((select ctr_id from countries where country_name='Ireland'), 'Galway');
INSERT INTO cities (ctr_id, city_name) VALUES ((select ctr_id from countries where country_name='Ireland'), 'Dublin');
INSERT INTO cities (ctr_id, city_name) VALUES ((select ctr_id from countries where country_name='Ireland'), 'Cork');
INSERT INTO cities (ctr_id, city_name) VALUES ((select ctr_id from countries where country_name='Ireland'), 'Athlone');

INSERT INTO cities (ctr_id, city_name) VALUES ((select ctr_id from countries where country_name='England'), 'London');
INSERT INTO cities (ctr_id, city_name) VALUES ((select ctr_id from countries where country_name='England'), 'Manchester');
INSERT INTO cities (ctr_id, city_name) VALUES ((select ctr_id from countries where country_name='England'), 'Leeds');

INSERT INTO cities (ctr_id, city_name) VALUES ((select ctr_id from countries where country_name='Germany'), 'Berlin');
INSERT INTO cities (ctr_id, city_name) VALUES ((select ctr_id from countries where country_name='Germany'), 'Munich');
INSERT INTO cities (ctr_id, city_name) VALUES ((select ctr_id from countries where country_name='Germany'), 'Hamburg');

INSERT INTO cities (ctr_id, city_name) VALUES ((select ctr_id from countries where country_name='France'), 'Paris');
INSERT INTO cities (ctr_id, city_name) VALUES ((select ctr_id from countries where country_name='France'), 'Marseille');
INSERT INTO cities (ctr_id, city_name) VALUES ((select ctr_id from countries where country_name='France'), 'Arles');


-- SENSORS

CREATE TABLE sensors (
    sens_id integer PRIMARY KEY UNIQUE,
    cit_id integer NOT NULL
);

ALTER TABLE sensors
    ADD FOREIGN KEY (cit_id) REFERENCES cities ON DELETE CASCADE;

CREATE INDEX cit_id_idx ON sensors (cit_id);

ALTER TABLE sensors OWNER TO meteodba;

-- SENSORS DATA

CREATE TABLE sensors_data (
    id bigserial PRIMARY KEY,
    sens_id integer NOT NULL,
    temperature decimal NOT NULL,
    humidity integer NOT NULL,
    recorded TIMESTAMP without time zone NOT NULL
);

ALTER TABLE sensors_data
    ADD FOREIGN KEY (sens_id) REFERENCES sensors ON DELETE CASCADE;

CREATE INDEX sens_id_idx ON sensors_data (sens_id);

ALTER TABLE sensors_data OWNER TO meteodba;
