import sqlite3
import sys
from sqlite3 import Error

table_command = """
	CREATE TABLE IF NOT EXISTS urls(
		id integer PRIMARY KEY AUTOINCREMENT,
		url text
		);
"""
insert_command = """
	INSERT INTO urls(url) 
	VALUES(?)
"""
select_url_command = """
	SELECT url 
	FROM urls 
	WHERE id=?
"""
select_id_command = """
	SELECT id
	FROM urls
	where url=?
"""

db_name = "url.db"
				
class UrlDb:
	def __init__(self,path=db_name):
		self.table_command = table_command
		self.insert_command = insert_command
		self.db_file = path
		self.conn = self.create_connection()
		self.crsr = self.conn.cursor()
		self.crsr.execute(self.table_command)
	def create_connection(self):
		try:
			conn = sqlite3.connect(self.db_file)
		except Error as e:
			print(e, file=sys.stdout)
		return conn
	def crsr_insert(self,url):
		try:
			self.crsr.execute(insert_command, [url])
			self.commit_connection()
		except Error as e:
			print(e, file=sys.stdout)
	def crsr_select_id(self, url):
		try:
		 	self.crsr.execute(select_id_command, [url])
		 	row = self.crsr.fetchone()
		except Error as e:
			print(e, file=sys.stdout)
		return row[0]
	def crsr_select_url(self, id):
		try:
		 	self.crsr.execute(select_url_command, [id])
		 	row = self.crsr.fetchone()
		except Error as e:
			print(e, file=sys.stdout)
		return row[0]
	def commit_connection(self):
		try:
			self.conn.commit()
		except Error as e:
			print(e, file=sys.stdout)
	def close_connection(self):
		try:
			self.conn.close()
		except Error as e:
			print(e, file=sys.stdout)


	



