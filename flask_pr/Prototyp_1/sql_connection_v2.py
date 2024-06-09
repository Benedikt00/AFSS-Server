from sqlalchemy import create_engine, text, insert
import json
import re
import logging as log
import unittest

log.basicConfig(
    format="%(levelname)s: %(message)s", encoding="utf-8", level=log.DEBUG
)  # filename='logs/app.log'


class Database(object):
    def __init__(self, db_adress, table):
        self.engine = create_engine(db_adress, echo=True)
        self.table_name = table
        self.nf_keys = "Kategorisierungen" # name for keys
        self.max_db_rows = 100

        # TODO: write a check, if the database suits the form we need; keys, datatypes ect
        # TODO: write tests

    def res_to_dict(self, res):
        rows_as_dicts = res.mappings().all()
        results_dicts = []
        # Print each row as a dictionary
        for row_dict in rows_as_dicts:
            results_dicts.append(row_dict)
        if len(rows_as_dicts) < 1:
            results_dicts = None
        return results_dicts

    def execute_query(self, query, no_return = False, commit = False) -> list[dict]:
        with self.engine.connect() as conn:
            result = conn.execute(text(query))
            if commit:
                conn.commit()
            
        if not no_return:
            return self.res_to_dict(result)
        else:
            return
    

    def load_db_all(self) -> list[dict]:
        result = self.execute_query(f"SELECT * FROM {self.table_name} LIMIT {self.max_db_rows}")
        return result

    def get_db_keys(self) -> list[str]:
        query = f"SHOW COLUMNS FROM {self.table_name}"
        result = self.execute_query(query)
        keys = []
        for cat in result:
            keys.append(cat["Field"])
        return keys

    def helper_sort_dict_by_value(self, category: str, dicts: dict):
        print(dicts)
        sorted_dicts = sorted(dicts, key=lambda x: x[category])
        if sorted_dicts == dicts:
            return sorted(dicts, key=lambda x: x[category], reverse=True)
        # log.info(sorted_dicts[0])
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

    def get_keys_of_type_num(self) -> list[str]:
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
        """gets all db elements which fit the search descriptions
        
        Keyword arguments:
        search_values -- the output of the html post request in dict format
        Return: returns all db elements which fit the search description
        """
        
        cat_to_search = self.get_db_keys()
        cat_searched = []

        base_query = f"Select * FROM {self.table_name} WHERE"
        first = True

        for search in search_values:
            for possible_category in cat_to_search:
                if (possible_category in search) and not (
                    possible_category in cat_searched
                ):

                    query = ""
                    search_cleaned = search.replace(possible_category, "")

                    if "min" in search_cleaned:
                        query = f"{possible_category} BETWEEN {search_values[search]} AND {search_values[f'inp_max_{possible_category}']}"

                    if "max" in search_cleaned:
                        query = f"{possible_category} BETWEEN {search_values[f'inp_min_{possible_category}']} AND {search_values[search]}"

                    if "text_" in search_cleaned:
                        if (search_values[search]) != "":
                            query = (
                                f"{possible_category} LIKE '%{search_values[search]}%'"
                            )

                    if query != "":
                        if first:
                            base_query = f"{base_query} {query}"
                            first = False
                        else:
                            base_query = f"{base_query} AND {query}"
                    cat_searched.append(possible_category)

                    break

        res = self.execute_query(f"{base_query} LIMIT {self.max_db_rows}")
        # log.info(f'res {type(res)}: {res}')

        return res


    def get_num_master_keys(self) -> int:

        list_dict_ident = self.execute_query(
            f"SELECT id, {self.nf_keys} FROM {self.table_name}"
        )

        nums_keys = 0

        for entry in list_dict_ident:
            keys_of_Entry = json.loads(entry[self.nf_keys])

            if len(keys_of_Entry) > nums_keys:
                nums_keys = len(keys_of_Entry)

        return nums_keys

    def get_first_identifiers(self) -> list[str]:

        list_dict_ident = self.execute_query(
            f"SELECT id, {self.nf_keys} FROM {self.table_name}"
        )

        possibilities = []
        indentifiers = []

        for k, entry in enumerate(list_dict_ident):
            keys_of_Entry = json.loads(entry[self.nf_keys])

            key = keys_of_Entry[0]
            if not key in possibilities:
                possibilities.append(key)

            possibilities.sort()

        num_ms_keys = self.get_num_master_keys()

        for i in range(num_ms_keys - len(indentifiers)):
            indentifiers.append([])

        indentifiers[0] = possibilities

        return indentifiers


    def process_keys(self, ls_keys: list[str]):
        index = -1

        for i, key in enumerate(ls_keys):
            if key == "":
                index = i
                break

        if index == -1:
            return ls_keys

        keys_gotten = []
        for key in ls_keys:
            if key != "":
                keys_gotten.append(key)
        keys_gotten_for_sql = str(keys_gotten).replace("'", '"')

        query = f"SELECT * FROM {self.table_name} WHERE JSON_CONTAINS({self.nf_keys}, '{keys_gotten_for_sql}');"
        result = self.execute_query(query)

        # get new ids
        new_ids = []

        for el in result:
            list_keys = json.loads(el[self.nf_keys])
            if list_keys[index] not in new_ids:
                new_ids.append(list_keys[index])

        return [new_ids, index]


    def load_db_entries_from_keys(self, ls_keys: list[str]) -> list[dict]:

        keys_gotten = []
        for key in ls_keys:
            if key != "":
                keys_gotten.append(key)
        keys_gotten_for_sql = str(keys_gotten).replace("'", '"')

        query = f"SELECT * FROM {self.table_name} WHERE JSON_CONTAINS({self.nf_keys}, '{keys_gotten_for_sql}');"

        return self.execute_query(query)
    
    def edit_db_entry_after_cat(self, id, category, new):

        type_of_inp = "string"
        query = f"SHOW COLUMNS FROM {self.table_name} WHERE FIELD = '{category}';"
        res_clean = self.execute_query(query)
        
        type = res_clean[0]['Type']

        #handle different types

        #string 
        if new == "":
            return ""

        match = re.search(r'\((\d+)\)', type)
        if match:
            length = int(match.group(1))

            if type_of_inp == "string" and len(new) <= length:
                try:
                    query = f"UPDATE {self.table_name} SET {category} = '{new}' WHERE id = {id};"
                    self.execute_query(query, no_return=True, commit=True)
                except:
                    return "Errror handeling this Request"
                return "It might have worked"
            else:
                return "String too long"

        if (type == "int") and new.isnumeric():
            try:
                query = f"UPDATE {self.table_name} SET {category} = '{new}' WHERE id = {id};"
                self.execute_query(query, no_return=True, commit=True)
                return "It might have worked"
            except Exception as e:
                log.info(e)
                return "Errror handeling this Request"
            
        
        return "Type is unnacounted for"
    


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database('mysql://root:112358@localhost:3306/test_db_bauteile', 'db_factory_p1')

    def test_get_db_keys(self):
        keys = self.db.get_db_keys()
        self.assertIsInstance(keys, list)
        self.assertTrue(all(isinstance(key, str) for key in keys))

    def test_load_db_all(self):
        data = self.db.load_db_all()
        self.assertIsInstance(data, list)

    # Add more test cases for other methods as needed

if __name__ == "__main__":
    #db_test = Database(
    #    "mysql://root:112358@localhost:3306/test_db_bauteile", "db_factory_p1"
    #    
    #)
    unittest.main()

    #log.info(
    #    db_test.load_db_search(
    #        {
    #            "inp_min_id": "1",
    #            "inp_max_id": "20",
    #            "text_search_Bauteilname": "a",
    #            "text_search_Kategorisierungen": "",
    #            "text_search_Platz": "",
    #            "inp_min_Bauteilanzahl": "8",
    #            "inp_max_Bauteilanzahl": "200",
    #            "inp_min_Bauteilanzahl_min": "1",
    #            "inp_max_Bauteilanzahl_min": "20",
    #            "inp_min_Gewicht_pro_teil_in_g": "0",
    #            "inp_max_Gewicht_pro_teil_in_g": "1000",
    #            "submit": "Search",
    #        }
    #    )
    #) 

    # print(db_test.get_db_keys())
