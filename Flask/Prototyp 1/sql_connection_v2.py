from sqlalchemy import create_engine, text, insert
import json
import re

class Database(object):
    def __init__(self, db_adress, table):
        self.engine = create_engine(db_adress, echo=False)
        self.table_name = table
        self.nf_keys = "Kategorisierungen"

    def res_to_dict(self, res):	
        rows_as_dicts = res.mappings().all()
        results_dicts = []
        # Print each row as a dictionary
        for row_dict in rows_as_dicts:
            results_dicts.append(row_dict)
        if len(rows_as_dicts) < 1:
            results_dicts = None	
        return results_dicts
    
    def execute_query(self, query) -> list[dict]:
        with self.engine.connect() as conn:
            result = conn.execute(text(query))
        return self.res_to_dict(result)
    
    def load_db_all(self):
        result = self.execute_query(f'SELECT * FROM {self.table_name}')
        return result
    
    def load_db_search_category(self, searched_categorys):
        q_orig = f"SELECT * FROM {self.table_name} WHERE"
        for i, key in enumerate(searched_categorys):
            if not key == self.nf_keys:
                print(key)
            else:
                raise "ProgrammerError,cant handle keys, this code is not yet written"

    def get_db_keys(self):
        query = f"SHOW COLUMNS FROM {self.table_name}"
        result = self.execute_query(query)
        keys = []
        for cat in result:
            keys.append(cat['Field'])
        return keys

    def helper_sort_dict_by_value(self, category, dicts):
        sorted_dicts = sorted(dicts, key=lambda x: x[category])
        if sorted_dicts == dicts:
            return sorted(dicts, key=lambda x: x[category], reverse=True)
        return sorted_dicts


if __name__ == '__main__':
    db_test = Database("mysql://root:112358@localhost:3306/test_db_bauteile", "db_factory_p1")
    print(db_test.load_db_search_category({"Bauteilname": "LED"}))
    #print(db_test.get_db_keys())