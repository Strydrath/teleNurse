## Class allowing to interact with the database
## Database has 6 tables:
## patients
## addresses
## visits
## medications
## actions to take during visit
## times of day for medications 
## and helper tables for relations between them:
## medication_taking -> patients, medications and times
## visit_actions -> visits and actions
import sqlite3
from sqlite3 import Error
from datetime import datetime


class Database:
    def __init__(self, db_file):
        self.conn = None
        self.db_file = db_file
        self.create_connection()
        self.create_tables()

    def create_connection(self):
        try:
            self.conn = sqlite3.connect(self.db_file)
            print(sqlite3.version)
        except Error as e:
            print(e)

    def create_tables(self):
        self.create_patients_table()
        self.create_addresses_table()
        self.create_visits_table()
        self.create_medications_table()
        self.create_actions_table()
        self.create_times_table()
        self.create_medication_taking_table()
        self.create_visit_actions_table()
    
    # Inserting new patient to the database
    # patient is a tuple with patient data
    def insert_patient(self, patient):
        sql = ''' INSERT INTO patients(first_name,last_name,birth_date,PESEL,address_id)
                  VALUES(?,?,?,?,?) '''
        cur = self.conn.cursor()
        cur.execute(sql, patient)
        self.conn.commit()
        return cur.lastrowid
    
    # Inserting new address to the database
    # address is a tuple with address data
    def insert_address(self, address):
        sql = ''' INSERT INTO addresses(patient_id,street,city,postal_code)
                  VALUES(?,?,?,?) '''
        cur = self.conn.cursor()
        cur.execute(sql, address)
        self.conn.commit()
        return cur.lastrowid
    
    # Inserting new visit to the database
    # visit is a tuple with visit data
    def insert_visit(self, visit):
        sql = ''' INSERT INTO visits(patient_id,date,time)
                  VALUES(?,?,?) '''
        cur = self.conn.cursor()
        cur.execute(sql, visit)
        self.conn.commit()
        return cur.lastrowid
    
    # Inserting new medication to the database
    # medication is a tuple with medication data
    def insert_medication(self, medication):
        sql = ''' INSERT INTO medications(name,description)
                  VALUES(?,?) '''
        cur = self.conn.cursor()
        cur.execute(sql, medication)
        self.conn.commit()
        return cur.lastrowid
    
    # Inserting new action to the database
    # action is a tuple with action data
    def insert_action(self, action):
        sql = ''' INSERT INTO actions(name)
                  VALUES(?) '''
        cur = self.conn.cursor()
        cur.execute(sql, action)
        self.conn.commit()
        return cur.lastrowid
    
    # Adding action to the visit
    # visit_action is a tuple with visit_action data
    def insert_visit_action(self, visit_action):
        sql = ''' INSERT INTO visit_actions(visit_id,action_id)
                  VALUES(?,?) '''
        cur = self.conn.cursor()
        cur.execute(sql, visit_action)
        self.conn.commit()
        return cur.lastrowid
    
    # Getting all patients from the database
    def get_patients(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM patients")
        rows = cur.fetchall()
        return rows
    
    # Getting all visits from the database
    def get_visits(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM visits")
        rows = cur.fetchall()
        return rows

    
    def create_patients_table(self):
        create_table_sql = """CREATE TABLE IF NOT EXISTS patients (
                                id integer PRIMARY KEY,
                                first_name text NOT NULL,
                                last_name text NOT NULL,
                                birth_date text NOT NULL,
                                PESEL text NOT NULL,
                                address_id integer NOT NULL,
                                FOREIGN KEY (address_id) REFERENCES addresses (id));"""
        self.create_table(create_table_sql)
    
    def create_addresses_table(self):
        create_table_sql = """CREATE TABLE IF NOT EXISTS addresses (
                                id integer PRIMARY KEY,
                                patient_id integer NOT NULL,
                                street text NOT NULL,
                                city text NOT NULL,
                                postal_code text NOT NULL,
                                FOREIGN KEY (patient_id) REFERENCES patients (id));"""
        self.create_table(create_table_sql)
    
    def create_visits_table(self):  
        create_table_sql = """CREATE TABLE IF NOT EXISTS visits (
                                id integer PRIMARY KEY,
                                patient_id integer NOT NULL,
                                date text NOT NULL,
                                time text NOT NULL,
                                FOREIGN KEY (patient_id) REFERENCES patients (id));"""
        self.create_table(create_table_sql)
    
    def create_medications_table(self):
        create_table_sql = """CREATE TABLE IF NOT EXISTS medications (
                                id integer PRIMARY KEY,
                                name text NOT NULL,
                                description text NOT NULL);"""
        self.create_table(create_table_sql)
    
    def create_actions_table(self):
        create_table_sql = """CREATE TABLE IF NOT EXISTS actions (
                                id integer PRIMARY KEY,
                                name text NOT NULL);"""
        self.create_table(create_table_sql)

    def create_times_table(self):
        create_table_sql = """CREATE TABLE IF NOT EXISTS times (
                                id integer PRIMARY KEY,
                                time text NOT NULL);"""
        self.create_table(create_table_sql)
    
    def create_medication_taking_table(self):
        create_table_sql = """CREATE TABLE IF NOT EXISTS medication_taking (
                                id integer PRIMARY KEY,
                                medication_id integer NOT NULL,
                                dose text NOT NULL,
                                time_id integer NOT NULL,
                                patient_id integer NOT NULL,
                                FOREIGN KEY (medication_id) REFERENCES medications (id),
                                FOREIGN KEY (patient_id) REFERENCES patients (id),
                                FOREIGN KEY (time_id) REFERENCES times (id));"""
        self.create_table(create_table_sql)
    
    def create_visit_actions_table(self):
        create_table_sql = """CREATE TABLE IF NOT EXISTS visit_actions (
                                id integer PRIMARY KEY,
                                visit_id integer NOT NULL,
                                action_id integer NOT NULL,
                                FOREIGN KEY (visit_id) REFERENCES visits (id),
                                FOREIGN KEY (action_id) REFERENCES actions (id));"""
        self.create_table(create_table_sql)
    

        
    def create_table(self, create_table_sql):
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)