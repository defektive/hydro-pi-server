hydro-pi-server
===============

python rest api for open sprinkler pi

## How to use

All if the samples below are available in this [postman collection](http://www.getpostman.com/collections/afd2a74a777b2acf79f0).
If you don't use postman I suggest take a look at it [here](https://chrome.google.com/webstore/detail/postman-rest-client/fdmmgilgnpjigdojojpjoooidkmcomcm?hl=en).

### List all stations

	GET http://0.0.0.0:8081/stations

	[
		{
			"status": 0,
			"stationID": 0
		},
		{
			"status": 0,
			"stationID": 1
		},
		{
			"status": 0,
			"stationID": 2
		},
		{
			"status": 0,
			"stationID": 3
		},
		{
			"status": 0,
			"stationID": 4
		},
		{
			"status": 0,
			"stationID": 5
		},
		{
			"status": 0,
			"stationID": 6
		},
		{
			"status": 0,
			"stationID": 7
		}
	]


### Get a specific stations status

	GET http://0.0.0.0:8081/stations/0

	{
	    "status": 0,
	    "stationID": 0
	}

### Turn a station on

	PUT http://0.0.0.0:8081/stations/0
	status=1

	{
	    "status": 1,
	    "stationID": 0
	}

### Turn s specific station off

	PUT http://0.0.0.0:8081/stations/0
	status=0

	{
	    "status": 0,
	    "stationID": 0
	}
