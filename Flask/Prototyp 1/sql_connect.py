from sqlalchemy import create_engine, text, insert
import json

engine = create_engine("mysql://root:112358@localhost:3306/test_db_bauteile", echo=False)


def res_to_dict(res):	
	rows_as_dicts = result.mappings().all()
	results_dicts = []
	# Print each row as a dictionary
	for row_dict in rows_as_dicts:
		results_dicts.append(row_dict)
	if len(rows_as_dicts) < 1:
		results_dicts = None	
	return results_dicts

def load_db():
	with engine.connect() as conn:
		result = conn.execute(text(f'SELECT * FROM factory_test_db'))
	
	return res_to_dict(result)

def get_num_master_keys():
	with engine.connect() as conn:
		result = conn.execute((text("SELECT id, identifiers FROM factory_test_db")))
	
	list_dict_ident = result.mappings().all()
	
	nums_keys = 0

	for entry in list_dict_ident:
		keys_of_Entry = json.loads(entry['identifiers'])

		if len(keys_of_Entry) > nums_keys:
			nums_keys = len(keys_of_Entry)

	return nums_keys

def get_first_identifier():
	with engine.connect() as conn:
		result = conn.execute((text("SELECT id, identifiers FROM factory_test_db")))
	
	list_dict_ident = result.mappings().all()
	
	possibilities = []
	indentifiers = []


	for k, entry in enumerate(list_dict_ident):
		keys_of_Entry = json.loads(entry['identifiers'])

		key = keys_of_Entry[0]

		if not key in possibilities:
			possibilities.append(key)

		possibilities.sort()

	num_ms_keys = get_num_master_keys()

	for i in range(num_ms_keys - len(indentifiers)):
		indentifiers.append([])
	
	indentifiers[0] = possibilities

	return indentifiers

def process_keys(ls_keys):

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
	keys_gotten_for_sql = str(keys_gotten).replace("'", "\"")
	with engine.connect() as conn:
		query = f"SELECT * FROM factory_test_db WHERE JSON_CONTAINS(identifiers, '{keys_gotten_for_sql}');"
		result = conn.execute(text(query))

	list_dict_res = result.mappings().all()

	#get new ids

	new_ids = []

	for el in list_dict_res:
		list_keys = json.loads(el['identifiers'])
		if list_keys[index] not in new_ids:
			new_ids.append(list_keys[index])


	return [new_ids, index]


def get_db_entys_from_keys(ls_keys):
	keys_gotten = []
	for key in ls_keys:
		if key != "":
			keys_gotten.append(key)
	keys_gotten_for_sql = str(keys_gotten).replace("'", "\"")
	with engine.connect() as conn:
		
		query = f"SELECT * FROM factory_test_db WHERE JSON_CONTAINS(identifiers, '{keys_gotten_for_sql}');"
		result = conn.execute(text(query))

	list_dict_res = result.mappings().all()

	return list_dict_res


if __name__ == '__main__':	
	get_db_entys_from_keys(["Key1", "", "", ""])