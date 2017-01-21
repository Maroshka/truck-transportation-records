from bottle import Bottle,run, route, request, default_app, HTTPResponse, response, template
from ConfigParser import SafeConfigParser
import datetime
import time,sys
import re
import MySQLdb as msql 
import numpy as np 
import itertools
import json
from random import shuffle

config = SafeConfigParser()
config.read('config.ini')

db = msql.connect(config.get('mysql','host'), config.get('mysql','user'), config.get('mysql','passwd'), config.get('mysql','dbname'), charset='utf8', use_unicode=True)
cursor = db.cursor()
app = application = Bottle()
cursor.execute('SHOW COLUMNS FROM '+config.get('mysql','tabname'))
columns = [column[0] for column in cursor.fetchall()]

@route('/ping')
def ping():
	return 'pong@%d' %time.time()

@route('/')
@route('/index')
def index():
	output = template('index')
	return output

@route('/create')
def create():

	render = request.query.get('render', None)
	print render 
	if render != None:
		view = template('front_end/create')
		return view
	response = {'status':200, 'title':'Done!','msg':'Query has been excuted successfully!' }
	qry = "INSERT INTO "+config.get('mysql','tabname')+" ("
	c = 0
	vals = []
	print columns
	for col in columns:
		colVal = request.query.get(col, None)
		if colVal != None and colVal!='' and colVal !="''":
			if qry[-1] != '(' and qry[-1]!=',':
				qry+=','
			qry+=col
			vals.append(colVal)
			print colVal
			c+=1
			print c
	if c>=2:
		qry+=") VALUES ("
		for val in vals:
			if qry[-1] != '(' and qry[-1]!=',':
				qry+=','
			qry+=val
		qry+=");"
		cursor.execute(qry)
		db.commit()
	else: 
		response['status'] = 400
		response['title'] = 'Failed'
		response['msg'] = 'Invalid Query!'
		
	return response

@route('/status')
def status():
	msg = request.query.get('msg')
	title= request.query.get('title')
	return template('front_end/status', msg=msg, title=title)

@route('/update')
def update():
	ids = request.query.get('id')
	qry = "UPDATE "+config.get('mysql','tabname')+" SET id="+ids
	cols = columns
	for colName in cols:
		colVal = request.query.get(colName)
		if (colVal!=None and colVal!=''):
			qry+=','+colName+"="+colVal
	qry+=' WHERE id='+ids
	cursor.execute(qry)
	data = cursor.fetchone()
	db.commit()
	print data

	return "Updated Successfully!"

@route('/view')
def view():
	ids = request.query.get('id')
	qry = "SELECT * FROM "+config.get('mysql','tabname')+" WHERE id ="+ids
	print qry
	cursor.execute(qry)
	data = cursor.fetchone()
	print type(data)
	output = template('front_end/view', id=data[0], truck_num=data[1], income=data[2], bon_num=data[3], company=data[4], expenses=data[5])

	return output
@route('/getRecord')
def getRecord():
	yes = request.query.get('all')
	if yes == 'yes':
		qry = "SELECT * FROM "+config.get('mysql','tabname')
		cursor.execute(qry)
		data = cursor.fetchall()
		print type(data)
		# print data
		response = [dict([(columns[i], data[j][i]) for i in range(len(columns))]) for j in range(len(data))]
		print response

	return json.dumps(response)

@route('/del')
def delete():
	ids = request.query.get('id')
	return 'oops'

@route('/viewAll')
def viewAll():
	view = template('front_end/all')
	return view


if __name__ == "__main__" :
    run(host=config.get('bottle','host'), port=config.get('bottle','port'), debug=True)
else:
    application = default_app()
