#!/usr/bin/python

# Pseudo code: controller loop for house heating
from datetime import datetime

class Schedule:
	pass
		
class EnvironmentSensor:
	pass
	
class HeatingSystem:
	pass
	
class House:
	pass

schedule = Schedule()

sensor = EnvironmentSensor() # the Particle
heating_system = Lyric() # the Honeywell
house = House(sensor, heating_system)

def is_time_to_start_heating(
		required_time, 
		required_temperature, 
		current_temperature, 
		warm_up_gradient
	):
	"""
	Returns True if it is time to start heating the house
	"""
	warm_up_time = (required_temperature - current_temperature) / warm_up_gradient
	warm_up_start_time = required_time - warm_up_time
	
	return now() > warm_up_start_time
	
	
# main loop
while True:
	
	current_temperature = house.sensor.indoor_temperature
	required_temperature = schedule.minimum_temperature
	is_too_cold = current_temperature < required_temperature
		
	if schedule.is_active_period():
				
		if is_too_cold:
			house.heating_system.turn_on()
		else:
			house.heating_system.turn_off()
	
	else:
		
		required_time = schedule.period.end_time
		warm_up_gradient = house.warm_up_gradient	
		
		if is_too_cold or is_time_to_start_heating(
									required_time, 
									required_temperature, 
									current_temperature, 
									warm_up_gradient):
			house.heating_system.turn_on()
		else:
			house.heating_system.turn_off()
