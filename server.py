from flask import Flask, request
from flask.ext.restful import Resource, Api, reqparse
import RPi.GPIO as GPIO
import atexit


NUM_STATIONS = 8


app = Flask(__name__)
api = Api(app)


class SprinklerGPIO():

	# GPIO pins
	PIN_SR_CLK = 4
	PIN_SR_NOE = 17
	PIN_SR_DAT = 21 # NOTE: if you have a RPi rev.2, need to change this to 27
	PIN_SR_LAT = 22

	def __init__(self, numberOfStations):
		self.numberOfStations = numberOfStations
		self.currentValues = [0]*numberOfStations

		GPIO.cleanup()
		# setup GPIO pins to interface with shift register
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.PIN_SR_CLK, GPIO.OUT)
		GPIO.setup(self.PIN_SR_NOE, GPIO.OUT)

		self.disableShiftRegisterOutput()
		GPIO.setup(self.PIN_SR_DAT, GPIO.OUT)
		GPIO.setup(self.PIN_SR_LAT, GPIO.OUT)

		self.updateRegister()
		self.enableShiftRegisterOutput()

	def setStationStatus(self, stationID, status):
		self.currentValues[stationID] = status
		self.updateRegister()
		return self.getStationStatus(stationID)

	def getStationStatus(self, stationID):
		return self.currentValues[stationID]

	def getCurrentValues(self): 
		return self.currentValues

	def enableShiftRegisterOutput(self):
		GPIO.output(self.PIN_SR_NOE, False)

	def disableShiftRegisterOutput(self):
		GPIO.output(self.PIN_SR_NOE, True)

	def updateRegister(self):
		GPIO.output(self.PIN_SR_CLK, False)
		GPIO.output(self.PIN_SR_LAT, False)

		for s in range(0, self.numberOfStations):
			GPIO.output(self.PIN_SR_CLK, False)
			GPIO.output(self.PIN_SR_DAT, self.currentValues[self.numberOfStations-1-s])
			GPIO.output(self.PIN_SR_CLK, True)

		GPIO.output(self.PIN_SR_LAT, True)

	def cleanup(self):
		self.currentValues = [0]*self.numberOfStations
		self.updateRegister()
		GPIO.cleanup()


sgpio = SprinklerGPIO(NUM_STATIONS)


class SprinklerREST(Resource):

	def get(self, stationID):
		status = sgpio.getStationStatus(stationID)

		return {"stationID": stationID, "status": status}

	def put(self, stationID):
		args = parser.parse_args()
		status = sgpio.setStationStatus(stationID, args.status)

		return {"stationID": stationID, "status": status}

class SprinklerListREST(Resource):
    def get(self):
	ret = []
	sv = sgpio.getCurrentValues()
	for s in range(0, NUM_STATIONS):
		cur = NUM_STATIONS - 1 - s
		ret.append({"stationID": cur, "status": sv[cur]})

        return ret

parser = reqparse.RequestParser()
parser.add_argument('status', type=int)

api.add_resource(SprinklerListREST, '/')
api.add_resource(SprinklerREST, '/<int:stationID>')


def progexit():
	sgpio.cleanup()

if __name__ == '__main__':
	atexit.register(progexit)
	app.run(host="0.0.0.0", port=8081, debug=True)

