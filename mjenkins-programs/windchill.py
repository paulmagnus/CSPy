def windChill():
	print 'Welcome to the windchill calculator!'
	temperature = input("Enter the temperature: ")
	windspeed = input("Enter the wind speed: ")
	windchill = 35.74 + (0.6215 * temperature) - (35.75 * (windspeed ** 0.16)) + (0.4275 * temperature * (windspeed ** 0.16))
	print 'At ' + str(temperature) + ' degrees, with a wind speed of ' + str(windspeed) + ' miles per hour, the windchill is: ' + str(windchill) + ' degrees'

windChill()
