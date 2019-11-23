import json
import logging
from flask import Flask, render_template, request
from classes.door import Door
from classes.chickencoop import ChickenCoop
from datetime import datetime

app = Flask(__name__)
global logger

# init logger
logFormat='[%(levelname)s] %(asctime)s: %(message)s'
logDateFormat='%d/%m/%Y %H:%M:%S'
logger = logging.getLogger('chickencoop')
logging.basicConfig(format=logFormat, datefmt=logDateFormat, filename='./logs/'+datetime.now().strftime("%d_%m_%Y - %H:%M:%S")+'.log',level=logging.DEBUG)

# init console logger
consoleLogger = logging.StreamHandler()
consoleLogger.setLevel(logging.DEBUG)
formatter = logging.Formatter(logFormat, datefmt=logDateFormat)
consoleLogger.setFormatter(formatter)
logger.addHandler(consoleLogger)

# def GPIO insideDoor
GPIO_RUN_DOOR = 4
GPIO_DOOR_WAY = 17
GPIO_END_CYCLE_CLOSING = 5
GPIO_END_CYCLE_OPENING = 6

# init doors
insideDoor = Door("Porte interieure", GPIO_RUN_DOOR, GPIO_DOOR_WAY, GPIO_END_CYCLE_OPENING, GPIO_END_CYCLE_CLOSING)
doors = [insideDoor]

# init chicken coop
chickenCoop = ChickenCoop(doors)
chickenCoop.start()

@app.route('/')
def index():

	templateData = {
		'doorOpened' : insideDoor.isOpened,
		'doorClosed' : insideDoor.isClosed,
		'doorOpening' : insideDoor.isOpening,
		'doorClosing' : insideDoor.isClosing,
		'openingTime' : chickenCoop.openingTime,
		'closingTime' : chickenCoop.closingTime,
	}  
	return render_template('index.html', **templateData)

@app.route('/getdata')
def getdata():
	jsonString = chickenCoop.to_json()
	print(jsonString)
		
	return jsonString

@app.route('/postjson', methods=['POST'])
def post():
	print("json received")
	print(request.is_json)
	content = request.get_json()
	print(content['id'])
	print(content['value'])
	
	result = "No id found for " + content['id']
	
	if content['id'] == "openingTime":
		chickenCoop.openingTime = content['value']
		result = "Opening time set with " + chickenCoop.openingTime
		chickenCoop.setupOpeningTime()
		
	if content['id'] == "closingTime":
		chickenCoop.closingTime = content['value']
		result = "Closing time set with " + chickenCoop.closingTime
		
	return result

@app.route("/<action>")
def action(action):
	if action == "open":
		print('Open door')
	if action == "close":
		print('Close door')
	
	templateData = {
		'doorOpened' : insideDoor.isOpened,
		'doorClosed' : insideDoor.isClosed,
		'doorOpening' : insideDoor.isOpening,
		'doorClosing' : insideDoor.isClosing,
		'openingTime' : chickenCoop.openingTime,
		'closingTime' : chickenCoop.closingTime,
	}  
	return render_template('index.html', **templateData)
	
if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
