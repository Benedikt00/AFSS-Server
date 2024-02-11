from sqlalchemy import create_engine, text, insert
import json
import re

engine = create_engine("mysql://root:112358@localhost:3306/test_db_bauteile", echo=False)

#TODO: Reformat to object oriented approach

def res_to_dict(res):	
	rows_as_dicts = res.mappings().all()
	results_dicts = []
	# Print each row as a dictionary
	for row_dict in rows_as_dicts:
		results_dicts.append(row_dict)
	if len(rows_as_dicts) < 1:
		results_dicts = None	
	return results_dicts

def load_db():
	with engine.connect() as conn:
		result = conn.execute(text(f'SELECT * FROM db_factory_p1'))
	bck = res_to_dict(result)
	return bck

def get_num_master_keys():
	with engine.connect() as conn:
		result = conn.execute(text("SELECT id, Kategorisierungen FROM db_factory_p1"))
	
	list_dict_ident = result.mappings().all()
	
	nums_keys = 0

	for entry in list_dict_ident:
		keys_of_Entry = json.loads(entry['Kategorisierungen'])

		if len(keys_of_Entry) > nums_keys:
			nums_keys = len(keys_of_Entry)

	return nums_keys

def get_first_identifier():
	with engine.connect() as conn:
		result = conn.execute((text("SELECT id, Kategorisierungen FROM db_factory_p1")))
	
	list_dict_ident = result.mappings().all()
	
	possibilities = []
	indentifiers = []


	for k, entry in enumerate(list_dict_ident):
		keys_of_Entry = json.loads(entry['Kategorisierungen'])

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
		query = f"SELECT * FROM db_factory_p1 WHERE JSON_CONTAINS(Kategorisierungen, '{keys_gotten_for_sql}');"
		result = conn.execute(text(query))

	list_dict_res = result.mappings().all()

	#get new ids

	new_ids = []

	for el in list_dict_res:
		list_keys = json.loads(el['Kategorisierungen'])
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
		
		query = f"SELECT * FROM db_factory_p1 WHERE JSON_CONTAINS(Kategorisierungen, '{keys_gotten_for_sql}');"
		result = conn.execute(text(query))

	list_dict_res = result.mappings().all()

	return list_dict_res

def get_db_element_by_id(id):
	with engine.connect() as conn:
		try:
			int(id)
		except Exception as e:
			return []

		result = conn.execute((text(f"SELECT * FROM db_factory_p1 WHERE id = {id}")))
	
	list_dict_ident = result.mappings().all()
	return list_dict_ident

def edit_db_entry_after_cat(id, category, new):

	type_of_inp = "string"

	with engine.connect() as conn:
		query = f"SHOW COLUMNS FROM db_factory_p1 WHERE FIELD = '{category}';"
		result = conn.execute((text(query)))
		res_clean = result.mappings().first()

		type = res_clean['Type']

		#handle different types

		#string 
		match = re.search(r'\((\d+)\)', type)
		if match:
			length = int(match.group(1))

			if type_of_inp == "string" and len(new) <= length:
				try:
					query = f"UPDATE db_factory_p1 SET {category} = '{new}' WHERE id = {id};"
					result = conn.execute((text(query)))
					conn.commit()
				except:
					return "Errror handeling this Request"
				return "It might have worked"
			else:
				return "String too long"

		if (type == "int") and new.isnumeric():
			try:
				query = f"UPDATE db_factory_p1 SET {category} = '{new}' WHERE id = {id};"
				result = conn.execute((text(query)))
				conn.commit()
				return "It might have worked"
			except:
				return "Errror handeling this Request"
			
		



	return "Type is unnacounted for"

if __name__ == '__main__':	
	pass