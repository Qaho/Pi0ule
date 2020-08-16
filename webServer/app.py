import json
import logging
from flask import Flask, render_template, request
from classes.door import Door
from classes.chickencoop import ChickenCoop
from classes.rainmeter import Rainmeter
from classes.network.response import Response, Status
from datetime import datetime

app = Flask(__name__)
global logger

# init logger
logFormat='[%(levelname)s] %(asctime)s: %(message)s'
logDateFormat='%d/%m/%Y %H:%M:%S'
logger = logging.getLogger('chickencoop')
logging.basicConfig(format=logFormat, datefmt=logDateFormat, filename='/home/pi/webServer/logs/'+datetime.now().strftime("%d_%m_%Y - %H:%M:%S")+'.log',level=logging.DEBUG)

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

# def GPIO rainmeter
GPIO_RAINMETER = 13

# init doors
insideDoor = Door("Porte interieure", GPIO_RUN_DOOR, GPIO_DOOR_WAY, GPIO_END_CYCLE_OPENING, GPIO_END_CYCLE_CLOSING)
doors = [insideDoor]

# init threads
chickenCoop = ChickenCoop(doors)
chickenCoop.start()

rainmeter = Rainmeter(GPIO_RAINMETER)
rainmeter.start()

@app.route('/')
def index():

	return render_template('index.html', doors=doors, chickenCoop=chickenCoop)

@app.route('/getdata')
def getdata():
	jsonString = chickenCoop.to_json()
	logger.info(jsonString)
		
	return jsonString

@app.route('/postjson', methods=['POST'])
def postjson():
	logger.info("postjson received: " + request)
	content = request.get_json()
	
	response = Response(Status.ERROR, "")
	
	if content['id'] == "openingTime":
		response.status = Status.OK
		chickenCoop.openingTime = content['value']
		logger.info("Opening time set to: " + chickenCoop.openingTime)
		
	if content['id'] == "closingTime":
		response.status = Status.OK
		chickenCoop.closingTime = content['value']
		logger.info("Opening time set to: " + chickenCoop.closingTime)

	response.data = chickenCoop.to_json()
		
	return response.to_json()

@app.route('/setclosingtime', methods=['POST'])
def setclosingtime():
	status = False
	if request.method == 'POST':
		chickenCoop.closingTime = request.form['closingTime']
		status = True
		logger.info("Closing time set to: " + chickenCoop.closingTime)

	return render_template('index.html', doors=doors, chickenCoop=chickenCoop, setClosingTimeStatus=status)

@app.route('/setopeningtime', methods=['POST'])
def setopeningtime():
	status = False
	if request.method == 'POST':
		chickenCoop.openingTime = request.form['openingTime']
		status = True
		logger.info("Opening time set to: " + chickenCoop.openingTime)

	return render_template('index.html', doors=doors, chickenCoop=chickenCoop, setOpeningTimeStatus=status)

@app.route("/<device>/<action>", methods=['POST'])
def action(device, action):
	logger.info("Action " + action + " received for device " + device)
	chickenCoop.handleDoorAction(device, action)
	
	return render_template('index.html', doors=doors, chickenCoop=chickenCoop)

@app.route("/rain/getdata")
def rain_getdata():
	jsonString = rainmeter.getData()
	logger.info(jsonString)
		
	return jsonString
	
if __name__ == '__main__' and "get_ipython" not in locals():
    app.run(debug=True, port=80, host='0.0.0.0', use_reloader=False)	