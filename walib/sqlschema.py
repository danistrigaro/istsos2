# -*- coding: utf-8 -*-
# ===============================================================================
#
# Authors: Massimiliano Cannata, Milan Antonovic
#
# Copyright (c) 2015 IST-SUPSI (www.supsi.ch/ist)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#
# ===============================================================================
createsqlschema = """

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;
SET default_tablespace = '';
SET default_with_oids = false;
SET TimeZone='0';

--=====================================

CREATE TABLE event_time (
    id_eti bigint NOT NULL,
    id_prc_fk integer NOT NULL,
    time_eti timestamp with time zone NOT NULL
);
COMMENT ON TABLE event_time IS 'Stores Observation''s eventTime.';

CREATE SEQUENCE event_time_id_eti_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
ALTER SEQUENCE event_time_id_eti_seq OWNED BY event_time.id_eti;

--=====================================

CREATE TABLE feature_type (
    name_fty character varying(25) NOT NULL,
    id_fty integer NOT NULL
);
COMMENT ON TABLE feature_type IS 'Definition of FeatureOfInterest type.';

CREATE SEQUENCE feature_type_id_fty_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
ALTER SEQUENCE feature_type_id_fty_seq OWNED BY feature_type.id_fty;

--=====================================

CREATE TABLE foi (
    desc_foi text,
    id_fty_fk integer NOT NULL,
    id_foi integer NOT NULL,
    name_foi character varying(25) NOT NULL
);
SELECT AddGeometryColumn('foi', 'geom_foi', $SRID, 'POINT', 3);
COMMENT ON TABLE foi IS 'Stores FeatureOfInterest type.';

CREATE SEQUENCE foi_id_foi_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
ALTER SEQUENCE foi_id_foi_seq OWNED BY foi.id_foi;


--=====================================

CREATE TABLE specimens
(
    id_spec bigint NOT NULL,
    identifier VARCHAR(36),
    id_qi_fk integer NOT NULL,
    id_eti_fk bigint NOT NULL,
    specimen json
);

CREATE SEQUENCE specimens_id_spec_seq
    INCREMENT 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
ALTER SEQUENCE specimens_id_spec_seq OWNED BY specimens.id_spec;

--=====================================

CREATE TABLE measures (
    id_msr bigint NOT NULL,
    id_eti_fk bigint NOT NULL,
    id_qi_fk integer NOT NULL,
    id_pro_fk integer NOT NULL,
    val_msr numeric(10,6) NOT NULL
);
COMMENT ON TABLE measures IS 'Stores the measures of the Procedure.';

CREATE SEQUENCE measures_id_msr_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
ALTER SEQUENCE measures_id_msr_seq OWNED BY measures.id_msr;

--=====================================

CREATE TABLE positions (
    id_pos bigint NOT NULL,
    id_qi_fk integer NOT NULL,
    id_eti_fk bigint NOT NULL
);
SELECT AddGeometryColumn('positions', 'geom_pos', $SRID, 'POINT', 3);
COMMENT ON TABLE positions IS 'Stores the location for mobile-points Procedure.';

CREATE SEQUENCE measures_mobile_id_mmo_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
ALTER SEQUENCE measures_mobile_id_mmo_seq OWNED BY positions.id_pos;

--=====================================

CREATE TABLE observed_properties (
    name_opr character varying(60) NOT NULL,
    def_opr character varying(80) NOT NULL,
    desc_opr text,
    constr_opr character varying,
    id_opr integer NOT NULL
);
COMMENT ON TABLE observed_properties IS 'Stores the ObservedProperties.';

CREATE SEQUENCE obs_pr_id_opr_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
ALTER SEQUENCE obs_pr_id_opr_seq OWNED BY observed_properties.id_opr;

--=====================================

CREATE TABLE obs_type (
    id_oty integer NOT NULL,
    name_oty character varying(60) NOT NULL,
    desc_oty character varying(120)
);
COMMENT ON TABLE obs_type IS 'Stores the type of observation (e.g.: mobile or fix).';

CREATE SEQUENCE obs_type_id_oty_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
ALTER SEQUENCE obs_type_id_oty_seq OWNED BY obs_type.id_oty;

--=====================================

CREATE TABLE off_proc (
    id_off_prc integer NOT NULL,
    id_off_fk integer NOT NULL,
    id_prc_fk integer NOT NULL
);
COMMENT ON TABLE off_proc IS 'Association table between Offerings and Procedures.';

CREATE SEQUENCE off_proc_id_opr_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
ALTER SEQUENCE off_proc_id_opr_seq OWNED BY off_proc.id_off_prc;

--=====================================

CREATE TABLE offerings (
    name_off character varying(64) NOT NULL,
    desc_off text,
    expiration_off timestamp with time zone,
    active_off boolean DEFAULT true NOT NULL,
    id_off integer NOT NULL
);
COMMENT ON TABLE offerings IS 'Stores the Offerings.';

CREATE SEQUENCE offerings_id_off_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
ALTER SEQUENCE offerings_id_off_seq OWNED BY offerings.id_off;

--=====================================

CREATE TABLE proc_obs (
    id_pro integer NOT NULL,
    id_prc_fk integer NOT NULL,
    id_uom_fk integer NOT NULL,
    id_opr_fk integer NOT NULL,
    constr_pro character varying
);
COMMENT ON TABLE proc_obs IS 'Association table between Procedures, ObservedProperty and UnitOfMeasure.';

CREATE SEQUENCE prc_obs_id_pro_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
ALTER SEQUENCE prc_obs_id_pro_seq OWNED BY proc_obs.id_pro;

--=====================================

CREATE TABLE procedures (
    id_prc integer NOT NULL,
    assignedid_prc character varying(32) NOT NULL,
    name_prc character varying(30) NOT NULL,
    desc_prc text,
    stime_prc timestamp with time zone,
    etime_prc timestamp with time zone,
    time_res_prc integer,
    time_acq_prc integer,
    id_oty_fk integer,
    id_foi_fk integer,
    mqtt_prc character varying
);
COMMENT ON TABLE procedures IS 'Stores the Procedures.';

CREATE SEQUENCE procedures_id_prc_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
ALTER SEQUENCE procedures_id_prc_seq OWNED BY procedures.id_prc;

--=====================================

CREATE TABLE quality_index (
    name_qi character varying(50) NOT NULL,
    desc_qi text,
    id_qi integer NOT NULL
);
COMMENT ON TABLE quality_index IS 'Stores the QualityIndexes.';

--=====================================

--CREATE TABLE time_res_unit (
--    id_tru integer NOT NULL,
--    name_tru character varying(15)
--);
--COMMENT ON TABLE time_res_unit IS 'Stores the Procedure''s time resolution units.';

--CREATE SEQUENCE time_res_unit_id_tru_seq
--    INCREMENT BY 1
--    NO MAXVALUE
--    NO MINVALUE
--    CACHE 1;
--ALTER SEQUENCE time_res_unit_id_tru_seq OWNED BY time_res_unit.id_tru;

--=====================================

CREATE TABLE uoms (
    name_uom character varying(20) NOT NULL,
    desc_uom text,
    id_uom integer NOT NULL
);
COMMENT ON TABLE uoms IS 'Stores the Units of Measures.';

CREATE SEQUENCE uoms_id_uom_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
ALTER SEQUENCE uoms_id_uom_seq OWNED BY uoms.id_uom;

--=====================================

CREATE TABLE tran_log (
    id_trl integer NOT NULL,
    transaction_time_trl timestamp without time zone DEFAULT now(),
    operation_trl character varying NOT NULL,
    procedure_trl character varying(30) NOT NULL,
    begin_trl timestamp with time zone,
    end_trl timestamp with time zone,
    count integer,
    stime_prc timestamp with time zone,
    etime_prc timestamp with time zone
);
COMMENT ON TABLE tran_log IS 'Log table for transactional operations.';

CREATE SEQUENCE tran_log_id_trl_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;
ALTER SEQUENCE tran_log_id_trl_seq OWNED BY tran_log.id_trl;

--=====================================
CREATE TYPE status AS ENUM ('verified','pending');
CREATE TABLE cron_log
(
   id_clo serial NOT NULL,
   id_prc_fk integer NOT NULL,              -- "5"
   process_clo character varying NOT NULL, -- "acquisizione"
   element_clo character varying NOT NULL, -- "T_TREVANO"
   datetime_clo timestamp with time zone NOT NULL, -- "NOW"
   message_clo character varying NOT NULL, -- "TIPO DI ECCEZIONE"
   details_clo character varying, -- "MESSAGGIO LIBERO"
   status_clo status,            -- "error"
   PRIMARY KEY (id_clo)
);
--=====================================
-- NEXTVALS
--=====================================

ALTER TABLE event_time ALTER COLUMN id_eti SET DEFAULT nextval('event_time_id_eti_seq'::regclass);
ALTER TABLE feature_type ALTER COLUMN id_fty SET DEFAULT nextval('feature_type_id_fty_seq'::regclass);
ALTER TABLE foi ALTER COLUMN id_foi SET DEFAULT nextval('foi_id_foi_seq'::regclass);
ALTER TABLE measures ALTER COLUMN id_msr SET DEFAULT nextval('measures_id_msr_seq'::regclass);
ALTER TABLE obs_type ALTER COLUMN id_oty SET DEFAULT nextval('obs_type_id_oty_seq'::regclass);
ALTER TABLE observed_properties ALTER COLUMN id_opr SET DEFAULT nextval('obs_pr_id_opr_seq'::regclass);
ALTER TABLE off_proc ALTER COLUMN id_off_prc SET DEFAULT nextval('off_proc_id_opr_seq'::regclass);
ALTER TABLE offerings ALTER COLUMN id_off SET DEFAULT nextval('offerings_id_off_seq'::regclass);
ALTER TABLE positions ALTER COLUMN id_pos SET DEFAULT nextval('measures_mobile_id_mmo_seq'::regclass);
ALTER TABLE proc_obs ALTER COLUMN id_pro SET DEFAULT nextval('prc_obs_id_pro_seq'::regclass);
ALTER TABLE procedures ALTER COLUMN id_prc SET DEFAULT nextval('procedures_id_prc_seq'::regclass);
--ALTER TABLE time_res_unit ALTER COLUMN id_tru SET DEFAULT nextval('time_res_unit_id_tru_seq'::regclass);
ALTER TABLE uoms ALTER COLUMN id_uom SET DEFAULT nextval('uoms_id_uom_seq'::regclass);
ALTER TABLE tran_log ALTER COLUMN id_trl SET DEFAULT nextval('tran_log_id_trl_seq'::regclass);

--=====================================
-- CONSTRAINTS
--=====================================
ALTER TABLE ONLY event_time
    ADD CONSTRAINT event_time_id_prc_fk_key UNIQUE (id_prc_fk, time_eti);
ALTER TABLE ONLY event_time
    ADD CONSTRAINT event_time_pkey PRIMARY KEY (id_eti);
ALTER TABLE ONLY feature_type
    ADD CONSTRAINT feature_type_pkey PRIMARY KEY (id_fty);
ALTER TABLE ONLY foi
    ADD CONSTRAINT foi_name_foi_key UNIQUE (name_foi);
ALTER TABLE ONLY foi
    ADD CONSTRAINT foi_pkey PRIMARY KEY (id_foi);
ALTER TABLE ONLY measures
    ADD CONSTRAINT measures_fix_pkey PRIMARY KEY (id_msr);
ALTER TABLE ONLY measures
    ADD CONSTRAINT measures_id_eti_fk_key UNIQUE (id_eti_fk, id_pro_fk);
ALTER TABLE ONLY positions
    ADD CONSTRAINT measures_mobile_pkey PRIMARY KEY (id_pos);
ALTER TABLE ONLY observed_properties
    ADD CONSTRAINT obs_pr_def_opr_key UNIQUE (def_opr);
ALTER TABLE ONLY observed_properties
    ADD CONSTRAINT obs_pr_pkey PRIMARY KEY (id_opr);
ALTER TABLE ONLY obs_type
    ADD CONSTRAINT obs_type_pkey PRIMARY KEY (id_oty);
ALTER TABLE ONLY off_proc
    ADD CONSTRAINT off_proc_id_off_fk_key UNIQUE (id_off_fk, id_prc_fk);
ALTER TABLE ONLY off_proc
    ADD CONSTRAINT off_proc_pkey PRIMARY KEY (id_off_prc);
ALTER TABLE ONLY offerings
    ADD CONSTRAINT offerings_name_off_key UNIQUE (name_off);
ALTER TABLE ONLY offerings
    ADD CONSTRAINT offerings_pkey PRIMARY KEY (id_off);
ALTER TABLE ONLY proc_obs
    ADD CONSTRAINT prc_obs_pkey PRIMARY KEY (id_pro);
ALTER TABLE ONLY proc_obs
    ADD CONSTRAINT proc_obs_id_uom_fk_key UNIQUE (id_uom_fk, id_opr_fk, id_prc_fk);
ALTER TABLE ONLY procedures
    ADD CONSTRAINT procedures_assignedid_prc_key UNIQUE (assignedid_prc);
ALTER TABLE ONLY procedures
    ADD CONSTRAINT procedures_pkey PRIMARY KEY (id_prc);
ALTER TABLE ONLY quality_index
    ADD CONSTRAINT quality_index_pkey PRIMARY KEY (id_qi);
--ALTER TABLE ONLY time_res_unit
--    ADD CONSTRAINT time_res_unit_pkey PRIMARY KEY (id_tru);
ALTER TABLE ONLY uoms
    ADD CONSTRAINT uoms_pkey PRIMARY KEY (id_uom);
ALTER TABLE ONLY event_time
    ADD CONSTRAINT event_time_id_prc_fk_fkey FOREIGN KEY (id_prc_fk) REFERENCES procedures(id_prc) ON DELETE CASCADE;
ALTER TABLE ONLY foi
    ADD CONSTRAINT foi_id_fty_fk_fkey FOREIGN KEY (id_fty_fk) REFERENCES feature_type(id_fty);
ALTER TABLE ONLY measures
    ADD CONSTRAINT measures_fix_id_qi_fk_fkey FOREIGN KEY (id_qi_fk) REFERENCES quality_index(id_qi) ON UPDATE CASCADE;
ALTER TABLE ONLY measures
    ADD CONSTRAINT measures_id_eti_fk_fkey FOREIGN KEY (id_eti_fk) REFERENCES event_time(id_eti) ON DELETE CASCADE;
ALTER TABLE ONLY measures
    ADD CONSTRAINT measures_id_pro_fk_fkey FOREIGN KEY (id_pro_fk) REFERENCES proc_obs(id_pro);
ALTER TABLE ONLY positions
    ADD CONSTRAINT measures_mobile_id_qi_fk_fkey FOREIGN KEY (id_qi_fk) REFERENCES quality_index(id_qi) ON UPDATE CASCADE;
ALTER TABLE ONLY off_proc
    ADD CONSTRAINT off_proc_id_off_fk_fkey FOREIGN KEY (id_off_fk) REFERENCES offerings(id_off) ON DELETE CASCADE;
ALTER TABLE ONLY off_proc
    ADD CONSTRAINT off_proc_id_prc_fk_fkey FOREIGN KEY (id_prc_fk) REFERENCES procedures(id_prc) ON DELETE CASCADE;
ALTER TABLE ONLY positions
    ADD CONSTRAINT positions_id_eti_fk_fkey FOREIGN KEY (id_eti_fk) REFERENCES event_time(id_eti) ON DELETE CASCADE;
ALTER TABLE ONLY proc_obs
    ADD CONSTRAINT prc_obs_id_opr_fk_fkey FOREIGN KEY (id_opr_fk) REFERENCES observed_properties(id_opr);
ALTER TABLE ONLY proc_obs
    ADD CONSTRAINT prc_obs_id_uom_fk_fkey FOREIGN KEY (id_uom_fk) REFERENCES uoms(id_uom);
ALTER TABLE ONLY proc_obs
    ADD CONSTRAINT proc_obs_id_prc_fk_fkey FOREIGN KEY (id_prc_fk) REFERENCES procedures(id_prc) ON DELETE CASCADE;
ALTER TABLE ONLY procedures
    ADD CONSTRAINT procedures_id_foi_fk_fkey FOREIGN KEY (id_foi_fk) REFERENCES foi(id_foi);
ALTER TABLE ONLY procedures
    ADD CONSTRAINT procedures_id_oty_fk_fkey FOREIGN KEY (id_oty_fk) REFERENCES obs_type(id_oty);
--ALTER TABLE ONLY procedures
--    ADD CONSTRAINT procedures_id_tru_fk_fkey FOREIGN KEY (id_tru_fk) REFERENCES time_res_unit(id_tru);
ALTER TABLE ONLY tran_log
    ADD CONSTRAINT tran_log_pkey PRIMARY KEY (id_trl);
ALTER TABLE ONLY cron_log
    ADD CONSTRAINT cron_log_id_prc_fk_fkey FOREIGN KEY (id_prc_fk) REFERENCES procedures(id_prc) ON DELETE CASCADE;

ALTER TABLE ONLY specimens
	ADD CONSTRAINT specimens_pkey PRIMARY KEY (id_spec);
ALTER TABLE ONLY specimens
    	ADD CONSTRAINT specimens_id_eti_fk_fkey FOREIGN KEY (id_eti_fk) REFERENCES event_time(id_eti) ON DELETE CASCADE;
ALTER TABLE ONLY specimens    
	ADD CONSTRAINT specimens_id_qi_fk_fkey FOREIGN KEY (id_qi_fk) REFERENCES quality_index(id_qi);


--=====================================
-- INDEXES
--=====================================
CREATE INDEX idx_eti_pk_date
ON event_time USING btree (id_eti, time_eti);

CREATE INDEX idx_eti_prc_date
ON event_time USING btree (id_prc_fk, time_eti);

CREATE INDEX idx_msr_id_eti_fk
ON measures USING btree (id_eti_fk);

CREATE INDEX idx_msr_eti_pro
ON measures USING btree (id_eti_fk, id_pro_fk);

CREATE UNIQUE INDEX idx_spec_identifier
ON specimens(identifier);

--=====================================
-- CONSTANT/DEFAULT VALUES
--=====================================

INSERT INTO quality_index (name_qi, desc_qi, id_qi) VALUES ('aggregation no data', 'no values are present for this aggregation interval', -100);
INSERT INTO quality_index (name_qi, desc_qi, id_qi) VALUES ('aggregation no data sent', 'no values are present for this aggregation interval and it is sent correctly', -110);
INSERT INTO quality_index (name_qi, desc_qi, id_qi) VALUES ('erroneous', 'gross error', 000);
INSERT INTO quality_index (name_qi, desc_qi, id_qi) VALUES ('erroneous sent', 'gross error, value sent to the server', 010);
INSERT INTO quality_index (name_qi, desc_qi, id_qi) VALUES ('QC0 - raw', 'the format is correct', 100);
INSERT INTO quality_index (name_qi, desc_qi, id_qi) VALUES ('QC0 - raw sent', 'the format is correct, value sent to the server', 110);
INSERT INTO quality_index (name_qi, desc_qi, id_qi) VALUES ('QC0 - range test1', 'range test using measuring range of the sensor', 101);
INSERT INTO quality_index (name_qi, desc_qi, id_qi) VALUES ('QC0 - range test1 sent', 'range test using sensor limits values, value sent to the server ', 111);
INSERT INTO quality_index (name_qi, desc_qi, id_qi) VALUES ('QC0 - range test2', 'the value is in a resonable range for that observed property', 102);
INSERT INTO quality_index (name_qi, desc_qi, id_qi) VALUES ('QC0 - range test2 sent', 'the value is in a resonable range for that observed property', 112);
INSERT INTO quality_index (name_qi, desc_qi, id_qi) VALUES ('QC0 - step test', 'the value is coherent with the previous', 103);
INSERT INTO quality_index (name_qi, desc_qi, id_qi) VALUES ('QC0 - step test sent', 'the value is coherent with the previous, value sent to the server', 113);
INSERT INTO quality_index (name_qi, desc_qi, id_qi) VALUES ('QC0 - time consistency', 'the value is timely consistent', 104);
INSERT INTO quality_index (name_qi, desc_qi, id_qi) VALUES ('QC0 - time consistency sent', 'the value is timely consistent, value sent to the server', 114);

INSERT INTO quality_index (name_qi, desc_qi, id_qi) VALUES ('QC1 - value aggregated with < 0.6', 'the value has been aggregated with less than 0.6 of good values', 200);
INSERT INTO quality_index (name_qi, desc_qi, id_qi) VALUES ('QC1 - value aggregated with < 0.6', 'the value has been aggregated with less than 0.6 of good values, value sent ot the server', 210);
INSERT INTO quality_index (name_qi, desc_qi, id_qi) VALUES ('QC1 - value aggregated', 'the value has been aggregated correctly', 201);
INSERT INTO quality_index (name_qi, desc_qi, id_qi) VALUES ('QC1 - value aggregated sent', 'the value has been aggregated correctly, value sent ot the server', 211);
INSERT INTO quality_index (name_qi, desc_qi, id_qi) VALUES ('QC1 - range test', 'the value is in a resonable range for that observed property', 202);
INSERT INTO quality_index (name_qi, desc_qi, id_qi) VALUES ('QC1 - range test sent', 'the value is in a resonable range for that observed property', 212);
INSERT INTO quality_index (name_qi, desc_qi, id_qi) VALUES ('QC1 - step test', 'the value is coherent with the previous', 203);
INSERT INTO quality_index (name_qi, desc_qi, id_qi) VALUES ('QC1 - step test sent', 'the value is coherent with the previous, value sent to the server', 213);
INSERT INTO quality_index (name_qi, desc_qi, id_qi) VALUES ('QC1 - time consistency', 'the value is timely consistent', 204);
INSERT INTO quality_index (name_qi, desc_qi, id_qi) VALUES ('QC1 - time consistency sent', 'the value is timely consistent, value sent to the server', 214);

INSERT INTO quality_index (name_qi, desc_qi, id_qi) VALUES ('QC2 - consistency time', 'the value is coherent with time-series', 300);
INSERT INTO quality_index (name_qi, desc_qi, id_qi) VALUES ('QC2 - spatially coherent', 'the value is coherent with close by observations', 301);
INSERT INTO quality_index (name_qi, desc_qi, id_qi) VALUES ('HQ - manually adjusted', 'the value has been manually corrected', 900);
INSERT INTO quality_index (name_qi, desc_qi, id_qi) VALUES ('HQ - correct', 'the value is correct', 909);

INSERT INTO obs_type (id_oty, name_oty, desc_oty) VALUES (1, 'insitu-fixed-point', 'fixed, in-situ, pointwise observation');
INSERT INTO obs_type (id_oty, name_oty, desc_oty) VALUES (2, 'insitu-mobile-point', 'mobile, in-situ, pointwise observation');
INSERT INTO obs_type (id_oty, name_oty, desc_oty) VALUES (3, 'virtual', 'virtual procedure');
INSERT INTO obs_type (id_oty, name_oty, desc_oty) VALUES (4, 'insitu-fixed-specimen', 'fixed, in-situ, pointwise observation from specimen');
INSERT INTO obs_type (id_oty, name_oty, desc_oty) VALUES (5, 'profile', 'virtual profile');

--=====================================
-- ADDING OBSERVED PROPERTIES
--=====================================
INSERT INTO observed_properties VALUES ('air-temperature', 'urn:ogc:def:parameter:x-istsos:1.0:meteo:air:temperature', 'air temperature at 2 meters above terrain', '{"interval": ["-40", "100"], "role": "urn:x-ogc:def:classifiers:x-istsos:1.0:qualityIndexCheck:level0"}', 1);
INSERT INTO observed_properties VALUES ('air-rainfall', 'urn:ogc:def:parameter:x-istsos:1.0:meteo:air:rainfall', 'liquid precipitation or snow water equivalent', '{"role": "urn:x-ogc:def:classifiers:x-istsos:1.0:qualityIndexCheck:level0", "min": "0"}', 2);
INSERT INTO observed_properties VALUES ('air-relative-humidity', 'urn:ogc:def:parameter:x-istsos:1.0:meteo:air:humidity:relative', 'absolute humidity relative to the maximum for that air', '{"interval": ["0", "100"], "role": "urn:x-ogc:def:classifiers:x-istsos:1.0:qualityIndexCheck:level0"}', 3);
INSERT INTO observed_properties VALUES ('air-wind-velocity', 'urn:ogc:def:parameter:x-istsos:1.0:meteo:air:wind:velocity', 'wind speed at 1 meter above terrain', '{"role": "urn:x-ogc:def:classifiers:x-istsos:1.0:qualityIndexCheck:level0", "min": "0"}', 4);
INSERT INTO observed_properties VALUES ('solar-radiation', 'urn:ogc:def:parameter:x-istsos:1.0:meteo:solar:radiation', 'Direct radiation sum in spectrum rand', NULL, 5);
INSERT INTO observed_properties VALUES ('river-height', 'urn:ogc:def:parameter:x-istsos:1.0:river:water:height', '', '{"interval": ["0", "10"], "role": "urn:x-ogc:def:classifiers:x-istsos:1.0:qualityIndexCheck:level0"}', 6);
INSERT INTO observed_properties VALUES ('river-discharge', 'urn:ogc:def:parameter:x-istsos:1.0:river:water:discharge', '', NULL, 7);
INSERT INTO observed_properties VALUES ('soil-evapotranspiration', 'urn:ogc:def:parameter:x-istsos:1.0:meteo:soil:evapotranspiration', '', NULL, 8);
INSERT INTO observed_properties VALUES ('air-heatindex', 'urn:ogc:def:parameter:x-istsos:1.0:meteo:air:heatindex', '', NULL, 9);
INSERT INTO observed_properties VALUES ('ground-water-height', 'urn:ogc:def:parameter:x-istsos:1.0:ground:water:height', '', NULL, 10);
INSERT INTO observed_properties VALUES ('water-ph', 'urn:ogc:def:parameter:x-istsos:1.0:water:ph', 'water pH', '{"interval": ["0", "14"], "role": "urn:x-ogc:def:classifiers:x-istsos:1.0:qualityIndexCheck:level0"}', 11);
INSERT INTO observed_properties VALUES ('water-dox', 'urn:ogc:def:parameter:x-istsos:1.0:water:dox', 'water dissolved oxygen', '{"interval": ["0", "1000"], "role": "urn:x-ogc:def:classifiers:x-istsos:1.0:qualityIndexCheck:level0"}', 12);
INSERT INTO observed_properties VALUES ('water-temperature', 'urn:ogc:def:parameter:x-istsos:1.0:water:temperature', 'water temperature', NULL, 13);
INSERT INTO observed_properties VALUES ('water-pressure', 'urn:ogc:def:parameter:x-istsos:1.0:water:pressure', 'water pressure', NULL, 14);
INSERT INTO observed_properties VALUES ('water-depth', 'urn:ogc:def:parameter:x-istsos:1.0:water:depth', 'Depth from surface', NULL, 15);
-- SIMILE PROJECT
INSERT INTO observed_properties VALUES ('water-Turb', 'urn:ogc:def:parameter:x-istsos:1.0:water:Turb', 'Turbidity', NULL, 16);
INSERT INTO observed_properties VALUES ('water-TSS', 'urn:ogc:def:parameter:x-istsos:1.0:water:TSS', 'Total suspended solids', NULL, 17);
INSERT INTO observed_properties VALUES ('water-SDT', 'urn:ogc:def:parameter:x-istsos:1.0:water:SDT', 'Secchi Disk Transparency', NULL, 18);
INSERT INTO observed_properties VALUES ('water-O2D', 'urn:ogc:def:parameter:x-istsos:1.0:water:O2D', 'Dissolved oxygen', NULL, 19);
INSERT INTO observed_properties VALUES ('water-O2S', 'urn:ogc:def:parameter:x-istsos:1.0:water:O2S', 'Oxygen saturation', NULL, 20);
INSERT INTO observed_properties VALUES ('water-O2C', 'urn:ogc:def:parameter:x-istsos:1.0:water:O2C', 'Oxygen concentration', NULL, 21);
INSERT INTO observed_properties VALUES ('water-EH', 'urn:ogc:def:parameter:x-istsos:1.0:water:EH', 'Redox potential', NULL, 22);
INSERT INTO observed_properties VALUES ('water-pH', 'urn:ogc:def:parameter:x-istsos:1.0:water:pH', 'pH', NULL, 23);
INSERT INTO observed_properties VALUES ('water-cond20', 'urn:ogc:def:parameter:x-istsos:1.0:water:cond20', 'Conductivity at 20 °C', NULL, 24);
INSERT INTO observed_properties VALUES ('water-cond25', 'urn:ogc:def:parameter:x-istsos:1.0:water:cond25', 'Conductivity at 25 °C', NULL, 25);
INSERT INTO observed_properties VALUES ('water-Alk', 'urn:ogc:def:parameter:x-istsos:1.0:water:Alk', 'Alkalinity', NULL, 26);
INSERT INTO observed_properties VALUES ('water-Cl', 'urn:ogc:def:parameter:x-istsos:1.0:water:Cl', 'Chloride', NULL, 27);
INSERT INTO observed_properties VALUES ('water-SO4', 'urn:ogc:def:parameter:x-istsos:1.0:water:SO4', 'Sulphate', NULL, 28);
INSERT INTO observed_properties VALUES ('water-NO3N', 'urn:ogc:def:parameter:x-istsos:1.0:water:NO3N', 'Nitrates as nitrogen', NULL, 29);
INSERT INTO observed_properties VALUES ('water-NH4N', 'urn:ogc:def:parameter:x-istsos:1.0:water:NH4N', 'Ammonium as nitrogen', NULL, 30);
INSERT INTO observed_properties VALUES ('water-Ca', 'urn:ogc:def:parameter:x-istsos:1.0:water:Ca', 'Calcium', NULL, 31);
INSERT INTO observed_properties VALUES ('water-Mg', 'urn:ogc:def:parameter:x-istsos:1.0:water:Mg', 'Magnesium', NULL, 32);
INSERT INTO observed_properties VALUES ('water-Na', 'urn:ogc:def:parameter:x-istsos:1.0:water:Na', 'Sodium', NULL, 33);
INSERT INTO observed_properties VALUES ('water-K', 'urn:ogc:def:parameter:x-istsos:1.0:water:K', 'Potassium', NULL, 34);
INSERT INTO observed_properties VALUES ('water-PO4P', 'urn:ogc:def:parameter:x-istsos:1.0:water:PO4P', 'Phosphate as phosporus', NULL, 35);
INSERT INTO observed_properties VALUES ('water-PTOT', 'urn:ogc:def:parameter:x-istsos:1.0:water:PTOT', 'Total phosporus', NULL, 36);
INSERT INTO observed_properties VALUES ('water-TN', 'urn:ogc:def:parameter:x-istsos:1.0:water:TN', 'Total Nitrogen', NULL, 37);
INSERT INTO observed_properties VALUES ('water-Si', 'urn:ogc:def:parameter:x-istsos:1.0:water:Si', 'Silica', NULL, 38);
INSERT INTO observed_properties VALUES ('water-NO2N', 'urn:ogc:def:parameter:x-istsos:1.0:water:NO2N', 'Nitrate as nitrogen', NULL, 39);
INSERT INTO observed_properties VALUES ('water-TOC', 'urn:ogc:def:parameter:x-istsos:1.0:water:TOC', 'Total organic carbon', NULL, 40);
INSERT INTO observed_properties VALUES ('water-DOC', 'urn:ogc:def:parameter:x-istsos:1.0:water:DOC', 'Dissolved organic carbon', NULL, 41);
INSERT INTO observed_properties VALUES ('water-Chl-a', 'urn:ogc:def:parameter:x-istsos:1.0:water:Chl-a', 'Chlorophyll a', NULL, 42);
INSERT INTO observed_properties VALUES ('water-chl', 'urn:ogc:def:parameter:x-istsos:1.0:water:chl', 'Total chlorophyll', NULL, 43);
INSERT INTO observed_properties VALUES ('water-PC', 'urn:ogc:def:parameter:x-istsos:1.0:water:PC', 'Phycocianin', NULL, 44);
INSERT INTO observed_properties VALUES ('water-PE', 'urn:ogc:def:parameter:x-istsos:1.0:water:PE', 'Phycoeritrin', NULL, 45);
INSERT INTO observed_properties VALUES ('water-PAR', 'urn:ogc:def:parameter:x-istsos:1.0:water:PAR', 'Photosynthetic active radiation', NULL, 46);
INSERT INTO observed_properties VALUES ('water-CO3', 'urn:ogc:def:parameter:x-istsos:1.0:water:CO3', 'Carbonate', NULL, 47);
INSERT INTO observed_properties VALUES ('water-Fe', 'urn:ogc:def:parameter:x-istsos:1.0:water:Fe', 'Iron', NULL, 48);
INSERT INTO observed_properties VALUES ('water-Mn', 'urn:ogc:def:parameter:x-istsos:1.0:water:Mn', 'Manganese', NULL, 49);
INSERT INTO observed_properties VALUES ('water-S', 'urn:ogc:def:parameter:x-istsos:1.0:water:S', 'Sulfur', NULL, 50);
INSERT INTO observed_properties VALUES ('water-CH4', 'urn:ogc:def:parameter:x-istsos:1.0:water:CH4', 'Methane', NULL, 51);
INSERT INTO observed_properties VALUES ('Autoscale', 'urn:ogc:def:parameter:x-istsos:1.0:Autoscale', 'Autoscale', NULL, 52);


SELECT pg_catalog.setval('obs_pr_id_opr_seq', 52, true);

--=====================================
-- ADDING UNIT OF MEASURES
--=====================================
INSERT INTO uoms VALUES ('null', '', 0);
INSERT INTO uoms VALUES ('mm', 'millimeter', 1);
INSERT INTO uoms VALUES ('°C', 'Celsius degree', 2);
INSERT INTO uoms VALUES ('%', 'percentage', 3);
INSERT INTO uoms VALUES ('m/s', 'metre per second', 4);
INSERT INTO uoms VALUES ('W/m2', 'Watt per square metre', 5);
INSERT INTO uoms VALUES ('°F', 'Fahrenheit degree', 6);
INSERT INTO uoms VALUES ('m', 'metre', 7);
INSERT INTO uoms VALUES ('m3/s', 'cube meter per second', 8);
INSERT INTO uoms VALUES ('mm/h', 'millimiters per hour', 9);
INSERT INTO uoms VALUES ('mg/l', 'milligrams per liter', 10);
INSERT INTO uoms VALUES ('hPa', 'hecto Pascal', 11);
-- SIMILE PROJECT
INSERT INTO uoms VALUES ('FTU', '', 12);
INSERT INTO uoms VALUES ('mg l-1', '', 13);
INSERT INTO uoms VALUES ('mV', '', 14);
INSERT INTO uoms VALUES ('µS cm-1', '', 15);
INSERT INTO uoms VALUES ('meq l-1', '', 16);
INSERT INTO uoms VALUES ('µg l-1', '', 17);
INSERT INTO uoms VALUES ('μmoles/sec/m²', '', 18);
INSERT INTO uoms VALUES ('μeq l-1', '', 19);

SELECT pg_catalog.setval('uoms_id_uom_seq', 19, true);

--=====================================
-- ADDING FUNCTIONS
--=====================================
CREATE OR REPLACE FUNCTION public.json_merge(
	data json,
	merge_data json)
    RETURNS json
    LANGUAGE 'sql'

    COST 100
    IMMUTABLE 
AS $BODY$
  SELECT json_object_agg(key, value)
  FROM (
    WITH to_merge AS (
      SELECT * FROM json_each(merge_data)
    )
    SELECT *
    FROM json_each(data)
    WHERE key NOT IN (SELECT key FROM to_merge)
    UNION ALL
    SELECT * FROM to_merge
  ) t;
$BODY$;

CREATE AGGREGATE json_collect(json) (
  SFUNC = json_merge,
  STYPE = json,
  INITCOND = '{}'
);

"""
