from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sock import Sock
import json

from sql_connect import load_db, get_first_identifier, process_keys, get_db_entys_from_keys

app = Flask(__name__)

sock = Sock(app)

@app.route('/')
def root():
    # Redirect to "/sectionb"
    #return redirect(url_for('selection'))
	return render_template('index.html')


all_keys_for_search = get_first_identifier()



@app.route('/selection', methods=["get" ,"post"])
def selection():
	ls_form_values = []
	if request.method == 'POST':
		
		data = request.form.to_dict()

		#handle request for next values
		if "form_values" in data.keys():
			ls_form_values = list(data["form_values"].split(","))
			
			all_keys_defined = False

			if "" not in ls_form_values:
				all_keys_defined = True
					
			if not all_keys_defined:
				key_next_search = process_keys(ls_form_values)
				all_keys_for_search[key_next_search[-1]] =  key_next_search[0]
		
		#handle request for order
		if "order" in data.keys():
			print("Order this Component ", data)

	db_reply = get_db_entys_from_keys(ls_form_values)


	return render_template('selection.html', 
			db_keys_1 = all_keys_for_search, 
			selected_values = ls_form_values,
			db_entrys_from_keys = db_reply
			)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#@app.route("/selection/api", methods=["post"])
#def selection_w_data():
#	data = request.form.to_dict()
#	print(data)
#	ls_form_values = list(data["form_values"].split(","))
#	print(ls_form_values, " form values")
#
#	return render_template('selection.html', 
#			db_keys_1 = [[]],
#			more_data = ls_form_values
#			)

@app.route('/test')
def test():
	return render_template('test.html')

@sock.route('/com_selection')
def echo(sock):
	while True:
		data = sock.receive()
		ls_form_values = list(data.split(","))
		print(ls_form_values)
		sock.send(ls_form_values)

if __name__ == '__main__':
	app.run("0.0.0.0", debug=True)