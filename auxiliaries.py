from random import seed, random
import numpy as np

# set direction (unnormalized) and magnitude of a vector
def set_vector(direction,vel): return np.multiply(direction, vel/magnitude(direction))

# flip x and y value of a vector
def flip_dir(a): return [a[1],a[0]]

# length of a 2D vector
def magnitude(a): return np.sqrt(a[0]**2+a[1]**2)

# returns equally distributed random numbers in between -d and d
def rnd(d):
	seed()
	return 2*random()*d - d

# checks if a wall is crossed and returns true if yes
def touch_wall(pos):
	rad = 0.25
	touch_flag = False
	if   pos[0] <= 10.+rad and pos[1] <= 10.+rad: touch_flag = True
	elif pos[0] <= 10.+rad and pos[1] >= 15.-rad: touch_flag = True
	elif pos[0] >= 15.-rad and pos[1] <= 10.+rad: touch_flag = True
	elif pos[0] >= 15.-rad and pos[1] >= 15.-rad: touch_flag = True
	return touch_flag

# returns the velocity normal to the wall
def wall_dir(pos, dp):
	vel = magnitude(dp)
	if   touch_wall(np.add(pos,(dp[0],0))): return (0,vel*np.sign(dp[1]))
	elif touch_wall(np.add(pos,(0,dp[1]))): return (vel*np.sign(dp[0]),0)
	else: return (0,0)

# returns vector to nearest wall
def wall_dist(pos):
	rad = 0.25
	# = # 
	if   pos[0] <= 10. and pos[1] >= 12.5: return [ 0 , 15. - pos[1] ]
	elif pos[0] <= 10. and pos[1] <= 12.5: return [ 0 , 10. - pos[1] ]
	elif pos[0] >= 15. and pos[1] >= 12.5: return [ 0 , 15. - pos[1] ]
	elif pos[0] >= 15. and pos[1] <= 12.5: return [ 0 , 10. - pos[1] ]
	# || #
	elif pos[1] <= 10. and pos[0] >= 12.5: return [ 15. - pos[0] , 0 ]
	elif pos[1] <= 10. and pos[0] <= 12.5: return [ 10. - pos[0] , 0 ]
	elif pos[1] >= 15. and pos[0] >= 12.5: return [ 15. - pos[0] , 0 ]
	elif pos[1] >= 15. and pos[0] <= 12.5: return [ 10. - pos[0] , 0 ]
	#
	else: return [999.,999.]
	
#deletes pedestrians from list that have crossed the boundaries
def pedestrians_exit(list_of_pedestrians):
	
	# save every number of every pedestrian that left domain
	check_list = list_of_pedestrians.copy()
	pop_list = []
	for num,pedestrian in enumerate(check_list):
		if   pedestrian.position[0] > 25.: pop_list.append(num)
		elif pedestrian.position[1] > 25.: pop_list.append(num)
		elif pedestrian.position[0] <  0.: pop_list.append(num)
		elif pedestrian.position[1] <  0.: pop_list.append(num)
	
	# sort list upside down and delete all from list of pedestrians
	pop_list.sort(reverse=True)
	for ped in pop_list:
		list_of_pedestrians.pop(ped)
	
	#return list of all pedestrians who are still in the domain
	return list_of_pedestrians