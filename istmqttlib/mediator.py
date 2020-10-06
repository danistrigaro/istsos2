# -*- coding: utf-8 -*-
# =============================================================================
#
# Authors: Massimiliano Cannata, Milan Antonovic, Daniele Strigaro
#
# Copyright (c) 2010 - 2017 IST-SUPSI (www.supsi.ch/ist)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA
#
# =============================================================================

import threading
import os
import sys
import requests
import json
import traceback
import psycopg2
sys.path.insert(0, os.path.abspath("."))
import config
from walib import utils, databaseManager, configManager
import isodate as iso
import istmqttlib
from paho.mqtt import client as mqtt_client
from datetime import datetime


class MQTTMediator():

    def __init__(self, conf=None):
        """ Initialize the MQTTMediator class
        conf
        """
        self.MODE_REGULAR = 0
        self.MODE_IRREGULAR = 1
        self.lock = threading.Lock()
        self.conf = conf
        self.broker = {}
        self.services = {}
        self.mqtts = []
        self.procedures = {}
        self.clients = []
        self.threads = []

        defaultCfg = os.path.join(
            config.services_path,
            "default.cfg"
        )

        instances = utils.getServiceList(
            config.services_path,
            listonly=False
        )
        
        for instance in instances:
            sc = configManager.waServiceConfig(defaultCfg, instance['path'])
            mqtt_config = sc.get('mqtt')
            conn = databaseManager.PgDB(
                sc.connection["user"],
                sc.connection["password"],
                sc.connection["dbname"],
                sc.connection["host"],
                sc.connection["port"]
            )
            self.services[instance['service']] = {
                "config": sc,
                "conn": conn
            }
            # Get mqtt configurations
            rows = conn.select("""
                SELECT id_prc, assignedid_prc, mqtt_prc, name_prc FROM %s.procedures""" % (
                instance['service'])
            )
            mqtt_config['procs'] = [row[3] for row in rows]
            mqtt_config['procs_id'] = [row[1] for row in rows]
            mqtt_config['conn'] = sc.connection
            mqtt_config['servicename'] = instance['service']
            # set multiple topics based on assignedid
            # topics = []
            # for row in rows:
            #     if mqtt_config['broker_topic'][-1] == '/':
            #         tmp_topic = mqtt_config['broker_topic']
            #         topic = (f'{tmp_topic}{row[1]}', 1)
            #     else:
            #         tmp_topic = mqtt_config['broker_topic']
            #         topic = (f'{tmp_topic}/{row[1]}', 1)

            #     topics.append(topic)
            # mqtt_config['broker_topic'] = topics
            self.mqtts.append(mqtt_config)

    def insert_observation(
            self, mqtt_data,
            conn_pars, servicename, qi=True):
        now = datetime.now(iso.UTC)
        non_blocking_exceptions = []
        
        # Create data array
        data = mqtt_data.split(";")
        data_log = data[:]

        # Assigned id always in the first position
        assignedid = data[0]

        if len(data) == 4:  # regular time series
            mode = self.MODE_REGULAR

        elif len(data) == 2:  # irregular time series
            mode = self.MODE_IRREGULAR

        else:
            raise Exception(
                "Body content wrongly formatted. Please read the docs."
            )

        try:
            conn = databaseManager.PgDB(
                conn_pars['user'],
                conn_pars['password'],
                conn_pars['dbname'],
                conn_pars['host'],
                conn_pars['port']
            )
            rows = conn.select(
                ("""
                    SELECT
                        procedures.id_prc,
                        proc_obs.id_pro,
                        proc_obs.constr_pro,
                        procedures.stime_prc,
                        procedures.etime_prc,
                        procedures.name_prc
                    FROM
                        %s.procedures,
                        %s.proc_obs
                    WHERE
                        proc_obs.id_prc_fk = procedures.id_prc
                """ % (servicename, servicename)) + """
                  AND
                    assignedid_prc = %s
                  ORDER BY
                    proc_obs.id_pro ASC;
                """,
                (
                    assignedid,
                )
            )
            if len(rows) == 0:
                raise Exception(
                    "Procedure with aid %s.%s not found." % (servicename, assignedid))

            id_prc = rows[0][0]
            name_prc = rows[0][5]
            bp = rows[0][3]
            bpu = False
            ep = rows[0][4]
            epu = False

            def check_sampling(sampling):

                # If the end position exists the new measures must be after
                if ep is not None and sampling_time <= ep:
                    non_blocking_exceptions.append(
                        "Procedure %s, Sampling time (%s) "
                        "is before the end position (%s)" % (
                            name_prc,
                            sampling_time.isoformat(),
                            ep.isoformat())
                    )
                    return False

                # Check that the sampling time is before now
                if sampling_time > now:
                    non_blocking_exceptions.append(
                        "Procedure %s, Sampling time (%s) "
                        "is in the future (%s)" % (
                            name_prc,
                            sampling_time.isoformat(),
                            now.isoformat())
                    )
                    return False

                return True

            tmp_data = []
            if mode == self.MODE_REGULAR:

                try:
                    start = iso.parse_datetime(data[1])
                except Exception:
                    raise Exception(
                        "Procedure %s, Sampling time (%s) "
                        "wrong format" %
                        name_prc, data[1])

                try:
                    step = iso.parse_duration(data[2])
                except Exception:
                    raise Exception(
                        "Procedure %s, duration (%s) "
                        "wrong format" % (
                            name_prc, data[2]
                        )
                    )

                data = data[3].split("@")
                for idx in range(0, len(data)):

                    sampling_time = start + (step * idx)

                    if not check_sampling(sampling_time):
                        continue

                    tmp_data.append([
                        sampling_time.isoformat()
                    ] + data[idx].split(","))

            elif mode == self.MODE_IRREGULAR:
                data = data[1].split("@")
                for i in range(len(data)):
                    data[i] = data[i].split(",")

                    try:
                        try:
                            sampling_time = iso.parse_datetime(data[i][0])
                            if not check_sampling(sampling_time):
                                continue
                        except Exception:
                            raise Exception(
                                "Procedure %s, Sampling time (%s) "
                                "wrong format" % (
                                    name_prc, data[i][0]
                                )
                            )

                        tmp_data.append(data[i])

                    except Exception:
                        non_blocking_exceptions.append(
                            "Procedure %s, Sampling time (%s) "
                            "wrong format" % (
                                name_prc, data[i][0]
                            )
                        )
                        continue

            data = tmp_data

            op_cnt = len(rows)
            for observation in data:
                try:
                    id_eti = conn.executeInTransaction(
                        ("""
                            INSERT INTO %s.event_time (id_prc_fk, time_eti)
                        """ % servicename) + """
                            VALUES (%s, %s::TIMESTAMPTZ) RETURNING id_eti;
                        """,
                        (
                            id_prc, observation[0]
                        )
                    )
                except:
                    id_eti=[[1]]

                if (bp is None) or (bp == '') or (
                        iso.parse_datetime(observation[0]) < bp):
                    bp = iso.parse_datetime(observation[0])
                    bpu = True

                if (ep is None) or (ep == '') or (
                        iso.parse_datetime(observation[0]) > ep):
                    ep = iso.parse_datetime(observation[0])
                    epu = True

                # check if procedure observations length is ok
                #   (-1 remove datetime from lenght of observations array)
                if qi:
                    if op_cnt != (len(observation)-1)/2:
                        non_blocking_exceptions.append(
                            "Procedure %s, Array length missmatch with procedures "
                            "observation number: %s" % (
                                name_prc, observation
                            )
                        )
                        continue
                else:
                    if op_cnt != (len(observation)-1):
                        non_blocking_exceptions.append(
                            "Procedure %s, Array length missmatch with procedures "
                            "observation number: %s" % (
                                name_prc, observation
                            )
                        )
                        continue

                idx_tmp = 1
                for idx in range(0, op_cnt):
                    if ':' in observation[(idx+1)]:
                        try:
                            value_qc = observation[(idx+1)].split(':')
                            if value_qc == '40':
                                value_qc = '400'
                            conn.executeInTransaction(
                                ("""
                                    INSERT INTO %s.measures(
                                        id_eti_fk,
                                        id_qi_fk,
                                        id_pro_fk,
                                        val_msr
                                    )
                                """ % servicename) + """
                                    VALUES (%s, %s, %s, %s);
                                """,
                                (
                                    int(id_eti[0][0]),  # id_eti
                                    float(value_qc[1]), # quality index
                                    int(rows[idx][1]),  # id_pro
                                    float(value_qc[0])
                                )
                            )
                        except Exception as ie:
                            non_blocking_exceptions.append(
                                "Procedure %s, %s" % (
                                    name_prc, ie
                                )
                            )
                    elif qi:
                        try:
                            conn.executeInTransaction(
                                ("""
                                    INSERT INTO %s.measures(
                                        id_eti_fk,
                                        id_qi_fk,
                                        id_pro_fk,
                                        val_msr
                                    )
                                """ % servicename) + """
                                    VALUES (%s, %s, %s, %s);
                                """,
                                (
                                    int(id_eti[0][0]),  # id_eti
                                    float(observation[idx_tmp+1]), # quality index
                                    int(rows[idx][1]),  # id_pro
                                    float(observation[idx_tmp])
                                )
                            )
                            idx_tmp+=2
                        except Exception as ie:
                            non_blocking_exceptions.append(
                                "Procedure %s, %s" % (
                                    name_prc, ie
                                )
                            )
                    else:
                        try:
                            conn.executeInTransaction(
                                ("""
                                    INSERT INTO %s.measures(
                                        id_eti_fk,
                                        id_qi_fk,
                                        id_pro_fk,
                                        val_msr
                                    )
                                """ % servicename) + """
                                    VALUES (%s, 100, %s, %s);
                                """,
                                (
                                    int(id_eti[0][0]),  # id_eti
                                    int(rows[idx][1]),  # id_pro
                                    float(observation[(idx+1)])
                                )
                            )
                        except Exception as ie:
                            non_blocking_exceptions.append(
                                "Procedure %s, %s" % (
                                    name_prc, ie
                                )
                            )

            if bpu:
                conn.executeInTransaction(
                    ("""
                        UPDATE %s.procedures
                    """ % servicename) + """
                        SET stime_prc=%s::TIMESTAMPTZ WHERE id_prc=%s
                    """,
                    (
                        bp.isoformat(),
                        id_prc
                    )
                )

            if epu:
                conn.executeInTransaction(
                    ("""
                        UPDATE %s.procedures
                    """ % servicename) + """
                        SET etime_prc=%s::TIMESTAMPTZ WHERE id_prc=%s
                    """,
                    (
                        ep.isoformat(),
                        id_prc
                    )
                )

            conn.commitTransaction()

            # self.setData(ret)
            # print("Thanks for data")

            if len(non_blocking_exceptions) > 0:
                print(str(non_blocking_exceptions), file=sys.stderr)
                data_log.append(str(non_blocking_exceptions))
            else:
                data_log.append('')
            data_log.insert(0, now.isoformat())

        except Exception as e:
            # print(traceback.print_exc(), file=sys.stderr)
            data_log.append(str(e))
            data_log.insert(0, now.isoformat())
            #traceback.print_exc(file=sys.stderr)
            conn.rollbackTransaction()
            if str(e).find("duplicate key")==-1:
                print(
                    "Error in fast insert (%s): %s" % (type(e), e)
                )

            # print("Thanks for data")

    def client_loop(
        self, mqtt_conf):

        def on_message(client, userdata, message):
            data_csv = str(message.payload.decode("utf-8"))
            procedure = message.topic.split('/')[-1]
            idx_proc = mqtt_conf['procs'].index(procedure)
            assignedid = mqtt_conf['procs_id'][idx_proc]
            data_csv_splitted = data_csv.split('\n')
            header = data_csv_splitted[0].split(',')

            data_tmp = '@'.join(data_csv_splitted[1:])
            data = f'{assignedid};{data_tmp}'
            self.insert_observation(
                data,
                mqtt_conf['conn'],
                mqtt_conf['servicename']
            )
            # print(mqtt_conf)
        
        def on_subscribe(client, userdata, flags, rc):
            print("Subscribed")
        
        def on_connect(client, userdata, flags, rc):
            print("Connected")
            client.subscribe([
                (
                    mqtt_conf['broker_topic'] + '/#',
                    1
                )
            ])

        client = mqtt_client.Client()
        client.on_subscribe = on_subscribe
        client.on_message = on_message
        client.on_connect = on_connect
        # client.on_disconnect = self.on_disconnect
        client.username_pw_set(
            username=mqtt_conf['broker_user'],
            password=mqtt_conf['broker_password']
        )
        client.connect(
            mqtt_conf['broker_url'],
            port=int(mqtt_conf['broker_port']),
        )
        
        client.loop_forever()

    def start(self):
        print("Start")
        for mqtt_conf in self.mqtts:
            if mqtt_conf['broker_url']:
                
                t = threading.Thread(
                    target=self.client_loop,
                    args=(mqtt_conf,)
                )
                self.threads.append(t)
                t.start()
                # print(mqtt_conf)

    # def stop(self):
        # while len(self.threads) > 0:
        #     thread = self.threads.pop()
        #     del thread
