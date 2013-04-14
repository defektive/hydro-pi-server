from flask import Flask
from flask.ext.restful import Resource, Api, reqparse, abort
import atexit
from lib.SprinklerGPIO import SprinklerGPIO

NUM_STATIONS = 8

app = Flask(__name__)
api = Api(app)
sgpio = SprinklerGPIO(NUM_STATIONS)


class SprinklerREST(Resource):

	def get(self, stationID):
		validateStation(stationID)
		status = sgpio.getStationStatus(stationID)

		return {"stationID": stationID, "status": status}

	def put(self, stationID):
		validateStation(stationID)
		args = parser.parse_args()

		# fail to off, only turn on if we get a 1
		setStatus = 1 if args.status == 1 else 0
		status = sgpio.setStationStatus(stationID, setStatus)

		return {"stationID": stationID, "status": status}


class SprinklerListREST(Resource):

	def get(self):
		ret = []
		sv = sgpio.getCurrentValues()
		for s in range(0, NUM_STATIONS):
			cur = NUM_STATIONS - 1 - s
			ret.insert(0, {"stationID": cur, "status": sv[cur]})

		return ret


def validateStation(stationID):
	if stationID >= NUM_STATIONS:
		abort(404, message="Invalid Station {}".format(stationID))

parser = reqparse.RequestParser()
parser.add_argument('status', type=int)

api.add_resource(SprinklerListREST, '/stations/')
api.add_resource(SprinklerREST, '/stations/<int:stationID>')


def progexit():
	sgpio.cleanup()

if __name__ == '__main__':
	atexit.register(progexit)
	app.run(host="0.0.0.0", port=8081, debug=True)
