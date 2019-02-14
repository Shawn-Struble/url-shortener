from flask import Flask, render_template, redirect, request
from url_db import UrlDb
import sys
import string
# base62 alphabet [0..9..a..z..A..Z]
base_62_alpha = string.digits + string.ascii_lowercase + string.ascii_uppercase
db = UrlDb()
app = Flask(__name__)

def encode_base_62(index_id, alphabet = base_62_alpha):
	"""
	Takes database index of URL and returns base 62 representation 

	:param index_id: a numeric value to be converted to base62
	:param alphabet: a string which contains the base62 alphabet
	:returns: A converted base62 string of the index
	"""
	if(index_id == 0):
		return alphabet[0]
	if(len(alphabet) <= 0 or len(alphabet) > 62):
		return 0
	arr = []
	div_base = len(alphabet)

	while(index_id):
		remainder = index_id % div_base
		index_id = index_id // div_base
		arr.append(alphabet[remainder])
	arr.reverse()
	return ''.join(arr)


#TODO:
# rewrite this
def decode_base_62(encoded_str, alphabet = base_62_alpha):
	"""
	Takes in encoded base 62 string and converts it

	:param index_id: a numeric value to be converted to base62
	:param alphabet: a string which contains the base62 alphabet
	:returns: A converted base62 string of the index
	"""
	# initialize convert loop variables
	base_62 = len(alphabet)
	str_len = len(encoded_str)
	index = 0
	converted_index = 0
	for i in range(str_len):
		converted_index = base_62 * converted_index + alphabet.find(encoded_str[i])
	return converted_index
def write_to_db_and_convert(url):
	db = UrlDb()
	# get the url
	# write the url to the database
	db.crsr_insert(url)
	# get the index id back from the database using the url
	url_id = db.crsr_select_id(url)
	# convert the id to base62
	short_url = encode_base_62(int(url_id))
	# print the url to the console
	print(short_url, file=sys.stdout)
	db.close_connection()
	# return the shortened url
	return short_url


@app.route('/', methods=['GET','POST'])
def index():
	if (request.method == 'GET'):
		return render_template('index.html')
	if (request.method == 'POST'):
		url = request.form.get("url")
		short_url = write_to_db_and_convert(url)
		return render_template('index.html',url = short_url)


@app.route('/<string:id>/')
def reroute(id):
	db = UrlDb()
	# receive base62 string
	# convert base62 to base10
	base10_id = decode_base_62(id)
	url = db.crsr_select_url(id)
	db.close_connection()

	return redirect("http://www.{0}.com".format(url), code=302)

if __name__=='__main__':
	app.run(debug=True)

	
