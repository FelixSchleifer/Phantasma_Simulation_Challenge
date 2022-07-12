from PIL import Image, ImageDraw,ImageFont
from pedestrians import pedestrian

# print png with walls and pedestrians and text
def print_png(name, ped_list, text):
	# creating new Image object 1 m is resolved by "res" pixels
	res = 30
	img = Image.new("RGB", (25*res, 25*res), color = "white")
	rad = .25*res
	
	# fill walls black
	img1 = ImageDraw.Draw(img)  
	img1.rectangle([(     0,      0), (10*res, 10*res)], fill ="black")
	img1.rectangle([(     0, 15*res), (10*res, 25*res)], fill ="black")
	img1.rectangle([(15*res,      0), (25*res, 10*res)], fill ="black")
	img1.rectangle([(15*res, 15*res), (25*res, 25*res)], fill ="black")
	
	# add text to top left wall
	img1.text((0, 0),text,(255,255,255))
	
	# draw every pedestrian as circle. Red pedestrians go bottom-up, blue ones go left-right
	for dot in ped_list:
		dot_color = "red"
		if dot.direction == "x": dot_color = "blue"
		img1.ellipse((dot.position[0]*res-rad, (25-dot.position[1])*res-rad, dot.position[0]*res+rad, (25-dot.position[1])*res+rad), fill =dot_color)

	# safe image as "name"
	img.save(name,"PNG")

def main(*args):
	list_of_ped = []
	list_of_ped.append(	pedestrian("x"))
	list_of_ped.append(	pedestrian("y"))
	print_png("test.png",list_of_ped,"test drawing")

if __name__ == "__main__":
	main()