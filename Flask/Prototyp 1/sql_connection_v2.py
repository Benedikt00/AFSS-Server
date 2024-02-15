from sqlalchemy import create_engine, text, insert
import json
import re
import logging as log

log.basicConfig(format='%(levelname)s: %(message)s', encoding='utf-8', level=log.DEBUG) #filename='logs/app.log'


class Database(object):
    def __init__(self, db_adress, table):
        self.engine = create_engine(db_adress, echo=False)
        self.table_name = table
        self.nf_keys = "Kategorisierungen"
        self.max_db_rows = 100

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
    
    def load_db_all(self) -> list[dict]:
        result = self.execute_query(f'SELECT * FROM {self.table_name}')
        return result
    

    def get_db_keys(self) -> list[str]:
        query = f"SHOW COLUMNS FROM {self.table_name}"
        result = self.execute_query(query)
        keys = []
        for cat in result:
            keys.append(cat['Field'])
        return keys

    def helper_sort_dict_by_value(self, category: str, dicts: dict): 
        print(dicts)
        sorted_dicts = sorted(dicts, key=lambda x: x[category])
        if sorted_dicts == dicts:
            return sorted(dicts, key=lambda x: x[category], reverse=True)
        #log.info(sorted_dicts[0])
        return sorted_dicts
    
    def load_first_x_rows(self, num_rows: int) -> list[dict]:
        query = f"""SELECT * FROM {self.table_name}
                    LIMIT {num_rows};"""
        
        res = self.execute_query(query)
        return res
    
    def get_min_max_val(self, category: str) -> list[int, int]:
        query = f"""SELECT MIN({category}) FROM {self.table_name}"""
        min = self.execute_query(query)
        query = f"""SELECT MAX({category}) FROM {self.table_name}"""
        max = self.execute_query(query)

        return [min[0][f"MIN({category})"], max[0][f"MAX({category})"]]
        
    def get_keys_of_type_num(self):
        query = f"""SELECT COLUMN_NAME
                    FROM INFORMATION_SCHEMA.COLUMNS
                    WHERE TABLE_NAME = '{self.table_name}'
                    AND (DATA_TYPE = 'int' OR DATA_TYPE = 'float');"""
        res = self.execute_query(query)
        keys = []
        for el in res:
            keys.append(el["COLUMN_NAME"])
        return keys
    
    def load_db_search(self, search_values: dict[dict]) -> list[dict]:
        
        cat_to_search = self.get_db_keys()

        cat_searched = []

        base_query = f"Select * FROM {self.table_name} WHERE"

        first = True

        for search in search_values:
            for possible_category in cat_to_search:
                if (possible_category in search) and not (possible_category in cat_searched):

                    query = ""
                    search_cleaned = search.replace(possible_category, "")

                    if "min" in search_cleaned:
                        query = f"{possible_category} BETWEEN {search_values[search]} AND {search_values[f'inp_max_{possible_category}']}"
                        
                    if "max" in search_cleaned:
                        query = f"{possible_category} BETWEEN {search_values[f'inp_min_{possible_category}']} AND {search_values[search]}"

                    if "text_" in search_cleaned:
                        if (search_values[search]) != "":
                            query = f"{possible_category} LIKE '%{search_values[search]}%'"

                    if query != "":
                        if first:
                            base_query = f"{base_query} {query}"
                            first = False
                        else:
                            base_query = f"{base_query} AND {query}"
                    cat_searched.append(possible_category)

                    break
        
        res = self.execute_query(f"{base_query} LIMIT {self.max_db_rows}")
        #log.info(f'res {type(res)}: {res}')

        return res

        


if __name__ == '__main__':
    db_test = Database("mysql://root:112358@localhost:3306/test_db_bauteile", "db_factory_p1")
    
    log.info(db_test.load_db_search({'inp_min_id': '1', 'inp_max_id': '20', 'text_search_Bauteilname': 'a', 'text_search_Kategorisierungen': '', 'text_search_Platz': '', 'inp_min_Bauteilanzahl': '8', 'inp_max_Bauteilanzahl': '200', 'inp_min_Bauteilanzahl_min': '1', 'inp_max_Bauteilanzahl_min': '20', 'inp_min_Gewicht_pro_teil_in_g': '0', 'inp_max_Gewicht_pro_teil_in_g': '1000', 'submit': 'Search'}))

    #print(db_test.get_db_keys())