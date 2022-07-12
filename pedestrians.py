from auxiliaries import touch_wall, wall_dir, wall_dist, rnd, magnitude,flip_dir, set_vector
import numpy as np

class pedestrian():

	# initialize pedestrians either at bottom end "y" or left end "x" with velocity towards goal
	def __init__(self, direction):
		self.direction = direction	  # define if going up ("X") or right ("Y")
		self.desired_velocity = 1.2 + rnd(.1)	# desired velocity between 1.1 and 1.3 m/s
		
		self.position     = np.array( [0.0,12.5 + rnd(2.)] )	  # initial position
		self.velocity     = np.array( [self.desired_velocity,0] ) # initial velocity
		self.acceleration = np.array( [0,0] )	# initial acceleration
		
		# change direction and start if from the other group
		if self.direction == "y":
			self.position = flip_dir(self.position)
			self.velocity = flip_dir(self.velocity)
	
	# returns a list of all distances to pedestrians closer than cut_off
	def get_distances(self,neighbours):
		cut_off = 3.  	# m maximum interaction length

		distances = []
		for nb in neighbours:
			# calculate direction and distance to other pedestrian
			connecting_vector = np.subtract(nb.position,self.position)	# vector to the other pedestrian
			dist = magnitude(connecting_vector)
			
			# if other pedestrian is not self and closer than cut_off radius, safe to list
			if dist > 0 and dist <= cut_off: distances.append([dist, connecting_vector])

		return distances
	
	# returns current target position. Either closest point on the exit or the middle of the correct lane, when lane was left 
	def get_path(self):
		path = []
		if self.direction == "x":
			path = [25,self.position[1]]
			if self.position[1] < 10. or self.position[1] > 15: path = [15,12.5]
		else:
			path = [self.position[0],25]
			if self.position[0] < 10. or self.position[0] > 15: path = [12.5,15]
		
		return path
	
	# calculate current acceleration considering ideal path, walls and other pedestrians
	def update_acc(self,neighbours):
		radius = 0.25   # m radius of a person
		max_acc = 2. 	# m/s^2
		
		# control parameters for behavior as 
		target_frc = .5	#time to accelerate pedestrian towards target at desired velocity
		wall_frc = 10.	#force that repels pedestrian from wall
		wall_len = 0.15	#interaction lengthscale with wall
		ped_frc  = 7.  #force that repels pedestrian from other ped.
		ped_len  = 0.07 #interaction lengthscale with other pedestrian
		
		# accelerate pedestrian towards its target
		dir_to_target = np.subtract(self.get_path(),self.position)							# vector towards target
		dir_to_target = set_vector(dir_to_target, self.desired_velocity)
		target_acceleration = np.subtract(dir_to_target,self.velocity)/target_frc		# accelerate towards target
		
		# repulsion from walls
		wall_vec = wall_dist(self.position)		# vector to closest wall
		wall_dis = magnitude(wall_vec)-radius	# distance to wall
		wall_pot = wall_frc/wall_len * np.exp(- wall_dis/wall_len)	# exponential potential
		wall_repulsion = - set_vector(wall_vec,wall_pot)	# repulsion away from wall with strength from potential
		
		# repulsion from other pedestrians
		pedestrian_repulsion = 0
		
		#for every neighbouring pedestrian within a cutoff radius
		for nb in self.get_distances(neighbours):
			distance = nb[0] - 2*radius # distance between the two pedestrians (not distance of centers!)
			repulsive_pot = ped_frc/ped_len * np.exp(- distance/ped_len) # exponential potential
			pedestrian_repulsion = pedestrian_repulsion - set_vector(nb[1],repulsive_pot) # repulsion away from other ped.
		
		# total acceleration is sum over all contributions
		acceleration = target_acceleration + wall_repulsion + pedestrian_repulsion
		
		# maximum acceleration is enforced here
		if   magnitude(acceleration) > max_acc: acceleration = set_vector(acceleration, max_acc)
		
		return acceleration
	
	# update position from acceleration -> velocity considering maxima. Hard walls are enforced
	def update_pos(self,acc, time_step):
		max_vel = 1.3 *self.desired_velocity # maximum velocity

		# add vel increment to velocity 
		dv = np.multiply(acc, time_step)
		self.velocity = np.add(self.velocity,dv)

		# if maximum velocity would be violated, set velocity to maximum velocity
		if   magnitude(self.velocity) > max_vel: self.velocity = set_vector(self.velocity, max_vel)	
	
		# add spatial increment dp to position
		dp = np.multiply(self.velocity, time_step)
		self.position = np.add(self.position,dp)
		
		# if wall is touched, walk along the wall with equal velocity
		if touch_wall(self.position):
			self.position = np.subtract(self.position,dp) # revert step
			self.position = np.add(self.position,wall_dir(self.position,dp))
	
	# returns current velocity, drift velocity relative to target and acceleration
	def get_state(self):
		vel = magnitude(self.velocity)
		
		drift = self.velocity[0]
		if self.direction == "y": drift = self.velocity[1]
		
		return vel, drift
