from bottle import Bottle,run, route, request, default_app, HTTPResponse, response, template
from ConfigParser import SafeConfigParser
import datetime
import logging
import pymongo
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

@route('/ping')
def ping():
	return 'pong@%d' %time.time()

@route('/')
def index():
	output = template('index')
	return output

@route('/create')
def create():
	car_num = request.query.get('car_num')
	print car_num
	income = request.query.get('income')
	print income
	bon_num = request.query.get('bon_num')
	print bon_num
	company = request.query.get('company')
	print company
	expenses = request.query.get('expenses')
	qry = "INSERT INTO cars (car_num, income, bon_num, company, expenses) VALUES ("+car_num+","+income+","+bon_num+","+company+","+expenses+");"
	cursor.execute(qry)
	db.commit()

	return "Created successfully!"

@route('/update')
def update():
	ids = request.query.get('id')
	qry = "UPDATE "+config.get('mysql','tabname')+" SET id="+ids
	cols = ['car_num','income','company','bon_num','expenses']
	for colName in cols:
		colVal = request.query.get(colName)
		if (colVal!=None and colVal!=''):
			qry+=','+colName+"="+colVal
	qry+=' WHERE id='+ids
	cursor.execute(qry)
	db.commit()

	return "Updated Successfully!"

@route('/view')
def view():
	ids = request.query.get('id')
	qry = "SELECT * FROM "+config.get('mysql','tabname')+" WHERE id ="+ids
	cursor.execute(qry)
	data = cursor.fetchone()
	print type(data)
	output = template('front_end/view', id=data[0], car_num=data[1], income=data[2], bon_num=data[3], company=data[4], expenses=data[5])
	return output

if __name__ == "__main__" :
    run(host=config.get('bottle','host'), port=config.get('bottle','port'), debug=True)
else:
    application = default_app()
