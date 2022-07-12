from pedestrians import pedestrian
from auxiliaries import pedestrians_exit
from visualization import print_png
import numpy as np

def main(*args):
	# temporal parameters
	dt    =  0.1	#s time step
	t_end = 60.	 	#s end time
	
	# pedestrian flow 
	ped_density  = 2. #ped/s
	
	# observation times
	img_out_time = .1 #s
	stat_time    = 1. #s
	
	# state variables time and pedestrians
	t     =  0.		#s
	list_of_ped  = [] #list of all pedestrians currently in the simulation domain
	
	# main loop
	while (t <= t_end+dt):
	
		#spawn new pedestrian according to fixed pedestrian flow
		if (t % (1./ped_density) < dt):
			list_of_ped.append(pedestrian("x"))	# walks from left to right
			list_of_ped.append(pedestrian("y"))	# walks from bottom to top
		
		# update pedestrian acceleration, velocity and position
		for ped in list_of_ped:
			ped.acceleration = ped.update_acc(list_of_ped)
			ped.update_pos(ped.acceleration, dt)
		
		# check for pedestrians leaving the domain
		list_of_ped = pedestrians_exit(list_of_ped)
	
		# observables
		# print png 
		if (t%img_out_time<=dt):
			mean_drift = 0
			for ped in list_of_ped:
				mean_drift = mean_drift + ped.get_state()[1]
			mean_drift = mean_drift / len(list_of_ped)
			
			print_png("out/out_%03.0f.png" % (10*t), list_of_ped,"pedestrian flux %2.1f/s\nt = %4.1f s\n%d pedestrians\nmean vel: %2.3f m/s" % (ped_density,t, len(list_of_ped), mean_drift))
		if (t%stat_time<=dt):
			mean_vel = [0,0]
			for ped in list_of_ped:
				mean_vel = np.add(mean_vel, ped.get_state())
			mean_vel = np.divide(mean_vel,len(list_of_ped))
			
			print("t = %2.0f n = %2d v = %2.3f d = %2.3f" % (t, len(list_of_ped),mean_vel[0],mean_vel[1]) )
			#print(list_of_ped[0].get_state())
		t = t+dt

if __name__ == "__main__":
	main()
