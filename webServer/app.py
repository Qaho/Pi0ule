import json
from flask import Flask, render_template, request
from classes.door import Door
from classes.timecontrol import TimeControl
from classes.chickencoop import ChickenCoop

app = Flask(__name__)

# def GPIO insideDoor
GPIO_RUN_DOOR = 4
GPIO_DOOR_WAY = 17
GPIO_END_CYCLE_CLOSING = 5
GPIO_END_CYCLE_OPENING = 6

# init doors
insideDoor = Door("Porte intérieure", GPIO_RUN_DOOR, GPIO_DOOR_WAY, GPIO_END_CYCLE_OPENING, GPIO_END_CYCLE_CLOSING)
doors = [insideDoor]

# init time control
timeControl = TimeControl()

# init chicken coop
chickenCoop = ChickenCoop(timeControl, doors)

@app.route('/')
def index():

	templateData = {
		'doorOpened' : insideDoor.isOpened,
		'doorClosed' : insideDoor.isClosed,
		'doorOpening' : insideDoor.isOpening,
		'doorClosing' : insideDoor.isClosing,
		'openingTime' : timeControl.openingTime,
		'closingTime' : timeControl.closingTime,
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
		timeControl.openingTime = content['value']
		result = "Opening time set with " + timeControl.openingTime
	if content['id'] == "closingTime":
		timeControl.closingTime = content['value']
		result = "Closing time set with " + timeControl.closingTime
		
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
		'openingTime' : timeControl.openingTime,
		'closingTime' : timeControl.closingTime,
	}  
	return render_template('index.html', **templateData)
	
if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
