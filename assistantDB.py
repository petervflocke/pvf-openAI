import sqlite3
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import os
import json
import os

import sqlite3

class SQLiteHandler:
    def __init__(self, db_name):
        self.db_name = db_name
        self.db_table_ltsm = 'LTSM'
        self.conn = None
        self.cursor = None
        self.create_connection_and_table()

    def create_connection_and_table(self):
        if not os.path.exists(self.db_name):
            self.conn = sqlite3.connect(self.db_name)
            self.create_table()
        else:
            self.conn = sqlite3.connect(self.db_name)
            if not self.check_table_exists(self.db_table_ltsm):
                self.create_table()
        self.cursor = self.conn.cursor()
        #self.conn.set_trace_callback(print)

    def check_table_exists(self, table_name):
        self.cursor = self.conn.cursor()
        self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
        return bool(self.cursor.fetchall())

    def create_table(self):
        query = f"""CREATE TABLE {self.db_table_ltsm} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        original_message TEXT,
                        entities TEXT,
                        relationships TEXT
                    );"""
        self.cursor = self.conn.cursor()
        self.cursor.execute(query)
        self.conn.commit()

    def insert_data(self, table_name, data):
        data = {k: json.dumps(v) if isinstance(v, list) else v for k, v in data.items()}
        columns = ', '.join(data.keys())
        values = ', '.join(['?'] * len(data))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
        self.cursor.execute(query, list(data.values()))
        self.conn.commit()

    def close_connection(self):
        self.conn.close()

    # Not needed
    # def compare_lists(entity, search_term, threshold=80):
    #     entity = entity.strip('][').split(', ')  # parsing string into list
    #     search_term = search_term.strip('][').split(', ')  # parsing string into list
    #     matches = []

    #     for term in search_term:
    #         # extractOne returns the match with highest similarity and the similarity score
    #         match, score = process.extractOne(term, entity)
    #         if score >= threshold:
    #             matches.append(match)
    #     return len(matches)

    def fuzzy_search_entities(self, search_for, threshold=80):
        search_for = search_for.strip('][').split(', ')
        self.cursor.execute(f"SELECT original_message, entities FROM {self.db_table_ltsm}")
        data = self.cursor.fetchall()

        matching_messages = []
        for original_message, entities in data:
            found = False
            print(original_message, entities)
            entities = entities.strip('][').split(', ')
            for entity in entities:
                for search_term in search_for:
                    if fuzz.ratio(entity, search_term) > threshold:
                        matching_messages.append(original_message)
                        found = True
                        break
                if found:
                    break
        print (matching_messages)
        return matching_messages

    # ToDo: remove not needed
    def print_data(self):
        self.cursor.execute(f"SELECT original_message, entities FROM {self.db_table_ltsm}")
        rows = self.cursor.fetchall()
        for row in rows:
            original_message, entities = row
            entities = json.loads(entities)
            print(f"Original message: {original_message}, Entities: {entities}")


if __name__ == "__main__":
    # Example usage
    data1 = {
    "original_message": "Adam ma psa o imieniu Alexa",
    "entities": ["Adam", "pies", "Alexa"],
    "relationships": ["Adam ma psa", "psa o imieniu Alexa"]
    }
    data2 = {
    "original_message": "Adam mieszka w Krakowie",
    "entities": ["Adam", "Kraków"],
    "relationships": ["Adam mieszka w Krakowie"]
    }

    data3 = {
    "original_message": "W Krakowie jest piękny zamek",
    "entities": ["Kraków", "zamek"],
    "relationships": ["Kraków ma piękny zamek"]
    }


    query = {
    "original_message": "Jak ma na imię pies Adama?",
    "entities": ["pies", "Adama"],
    "relationships": ["pies Adama"]
    }

    query = {
    "original_message": "Czy pies Adama mieszka w Krakowie?",
    "entities": ["pies", "Adama", "Kraków"],
    "relationships": ["pies Adama", "mieszka w Krakowie"]
    }

    #json_data = json.dumps(data)
    DATABASE = os.path.dirname(os.path.abspath(__file__)) + "/example.db"
    print (DATABASE)
    handler = SQLiteHandler(DATABASE)
    # handler.insert_data(handler.db_table_ltsm, data1)
    # handler.insert_data(handler.db_table_ltsm, data2)
    # handler.insert_data(handler.db_table_ltsm, data3)

    #handler.print_data()


    qs = query["entities"]
    search_for = json.dumps(qs) if isinstance(qs, list) else qs

    context = handler.fuzzy_search_entities(search_for, threshold=80)
    print (context)

    handler.close_connection()


