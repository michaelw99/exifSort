from subprocess import call, check_output
from os.path import expanduser
import os
import shutil
import imghdr

# priority queue to keep sorted by time? 
EXIF_INFO = {}
main_path = ''

def main():
	print("Welcome to exifSort! \nTo begin, input your image folder path: ")
	path = raw_input('> ')
	import_data(path)

	print("Import complete. You may now input commands. Enter 'help' for a list of commands.")
	while True:
		command = raw_input('> ')
		if command == 'swap':
			new_path = raw_input('Please enter the new folder path to sort: ')
			swap(new_path)
		elif command == 'type':
			copy = raw_input('Keep copy of original files? (Y/N): ')
			if copy == 'Y':
				x = True
				type(x)
			elif copy == 'N':
				x = False
				type(x)
			else:
				print('Please only enter Y or N.')
		elif command == 'shutter':
			# should probably add wrong input check too
			def shutterkey(string):
				if '/' in string:
					num1, den1 = string.split('/')
					den1 = den1.strip()
					num1 = num1.strip()
					return float(num1) / float(den1)
				else:
					return float(string)

			inp = raw_input('Enter the speed(s) in seconds separated by "," to separate into, i.e 1/200,1/20,4: ')
			boundaries = inp.split(',')
			boundaries = sorted([val.strip() for val in boundaries], key=shutterkey)
			copy = raw_input('Keep copy of original files? (Y/N): ')
			if copy == 'Y':
				x = True
				shutter(boundaries, x)
			elif copy == 'N':
				x = False
				shutter(boundaries, x)
			else:
				print('Please only enter Y or N.')
		elif command == 'help':
			print("You're outta luck bub.")
		else:
			print("Please input a proper command.")

# gets all exif data from folder
def import_data(path):
	# weird input? Clarify. Right now, no home directory or beginning / needed.
	global main_path 
	main_path = expanduser("~") + '/' + path
	for file_name in os.listdir(main_path):
		try:
			if imghdr.what(main_path + '/' + file_name):
		# if os.path.isfile(main_path + '/' + file_name):
				exif = check_output(['exiv2', '-p', 's', main_path + '/' + file_name])
				one = exif.split('\n')
				# this may not be safe. Not sure if it's always 4 at the end. CHECK.
				two = one[:len(one) - 4]
				dic = {}
				for item in two:
					k, v = item.split(':', 1)
					dic[k.strip()] = v.strip()
				EXIF_INFO[file_name] = dic
		except:
			pass

# moves file to folder, creates folder if necessary
# maybe add feature to create folder in new destination. Currently creates in place.
def move_file(file_name, dest_name, copy):
	if not os.path.exists(dest_name):
		os.makedirs(dest_name)
	if copy:
		shutil.copy2(main_path + '/' + file_name, dest_name + '/' + file_name)
	else:
		shutil.move(main_path + '/' + file_name, dest_name + '/' + file_name)

# changes the folder that the program is sorting
def swap(path):
	global main_path
	main_path = expanduser("~") + '/' + path

# organize by image type, maybe allow more granularity (FINE, MEDIUM, etc.)
def type(copy):
	for image in EXIF_INFO:
		if imghdr.what(main_path + '/' + image) == 'jpeg':
			move_file(image, main_path + '/JPEG', copy)
		else:
			move_file(image, main_path + '/RAW', copy)

# organize by shutter speed
def shutter(boundaries, copy):
	print(boundaries)
	for image in EXIF_INFO:
		shutter_speed = EXIF_INFO[image]["Exposure time"]
		print(shutter_speed)
		if '/' in shutter_speed:
			num1, den1 = shutter_speed.split('/')
			den1 = den1.split(' ')[0].strip()
			num1 = num1.strip()
			speed1 = float(num1) / float(den1)
			print(speed1)
		else:
			speed1 = float(shutter_speed.split(' ')[0].strip())
			print(speed1)

		for i in range(len(boundaries)):
			print(boundaries[i])
			print(i)
			print(len(boundaries))
			if '/' in boundaries[i]:
				num2, den2 = boundaries[i].split('/')
				num2 = num2.strip()
				den2 = den2.strip()
				speed2 = float(num2) / float(den2)
				print(speed2)
			else:
				speed2 = float(boundaries[i].split('/')[0].strip())
			if speed1 <= speed2:
				move_file(image, main_path + '/' + boundaries[i].replace('/', 'x') + '-', copy)
				print('MOVING ' + image)
				break
			if i == len(boundaries) - 1:
				move_file(image, main_path + '/' + boundaries[i].replace('/', 'x') + '+', copy)
				print('MOVING ' + image)

def iso(boundaries, copy):
	pass

def aperture(boundaries, copy):
	pass

def date(boundaries, copy):
	pass

main()