import numpy as np
import cv2

prev_kadr = []
current_kadr = []

def m_rec(image):
	global prev_kadr
	global current_kadr

	if(len(prev_kadr) == 0): #first call of function
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		prev_kadr = cv2.blur(gray, (5, 5))

	else: #non first call of function
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		current_kadr = cv2.blur(gray, (5, 5))

		# diff = np.abs(current_kadr - prev_kadr)  # find diff
		# mask = diff > 50  # threshold (don't use rgb here...)

		# res_kadr = np.zeros_like(current_kadr)
		# res_kadr[mask] = current_kadr[mask]

		# compute difference
		difference = cv2.subtract(current_kadr, prev_kadr)

		mask = cv2.threshold(difference, 20, 255, cv2.THRESH_BINARY)[1]

		# percentage = (cv2.sumElems(difference)[0] * 100)/ (difference.size*255)
		percentage = (np.count_nonzero(mask) * 100)/ mask.size
		# if percentage >= 100:
		# 	print("FUUUCK")
		if percentage >= 0.1:# 0.1 percent (0.1%)
			print("move")
		else:
			print("stay")

		# mask = difference
		# height = mask.shape[0]
		# width = mask.shape[1]
		#res_kadr = mask

		# # color the mask red
		# Conv_hsv_Gray = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
		# ret, mask = cv2.threshold(Conv_hsv_Gray, 50, 255, cv2.THRESH_BINARY_INV)# |cv2.THRESH_OTSU
		# res_kadr = mask

		prev_kadr = current_kadr

		cv2.imshow("Diff: ", difference)
		#print("percentage: " + str(percentage) + " non_z: " + str(np.count_nonzero(mask)) + " size: " + str(mask.size))
		cv2.imshow("Mask: ", mask)

count = 0
N = 5 # How many kadrs missing

def n_kadr_diff_m_rec(image):
	global count

	global prev_kadr
	global current_kadr

	if count % N == 0:
		if(len(prev_kadr) == 0): #first call of function
			gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			prev_kadr = cv2.blur(gray, (5, 5))

		else: #non first call of function
			gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			current_kadr = cv2.blur(gray, (5, 5))

			# diff = np.abs(current_kadr - prev_kadr)  # find diff
			# mask = diff > 50  # threshold (don't use rgb here...)

			# res_kadr = np.zeros_like(current_kadr)
			# res_kadr[mask] = current_kadr[mask]

			# compute difference
			difference = cv2.subtract(current_kadr, prev_kadr)

			mask = cv2.threshold(difference, 20, 255, cv2.THRESH_BINARY)[1]

			# percentage = (cv2.sumElems(difference)[0] * 100)/ (difference.size*255)
			percentage = (np.count_nonzero(mask) * 100)/ mask.size
			# if percentage >= 100:
			# 	print("FUUUCK")
			if percentage >= 0.1:# 0.1 percent (0.1%)
				print("move")
			else:
				print("stay")

			# mask = difference
			# height = mask.shape[0]
			# width = mask.shape[1]
			#res_kadr = mask

			# # color the mask red
			# Conv_hsv_Gray = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
			# ret, mask = cv2.threshold(Conv_hsv_Gray, 50, 255, cv2.THRESH_BINARY_INV)# |cv2.THRESH_OTSU
			# res_kadr = mask

			prev_kadr = current_kadr

			cv2.imshow("Diff: ", difference)
			#print("percentage: " + str(percentage) + " non_z: " + str(np.count_nonzero(mask)) + " size: " + str(mask.size))
			cv2.imshow("Mask: ", mask)

		count = count + 1

	else:
		count = count + 1

def mesh_m_rec(image):
	global prev_kadr
	global current_kadr

	if(len(prev_kadr) == 0): #first call of function
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		prev_kadr = cv2.blur(gray, (5, 5))

	else: #non first call of function
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		current_kadr = cv2.blur(gray, (5, 5))

		# diff = np.abs(current_kadr - prev_kadr)  # find diff
		# mask = diff > 50  # threshold (don't use rgb here...)

		# res_kadr = np.zeros_like(current_kadr)
		# res_kadr[mask] = current_kadr[mask]

		# compute difference
		difference = cv2.subtract(current_kadr, prev_kadr)

		mask = cv2.threshold(difference, 20, 255, cv2.THRESH_BINARY)[1]

		rgb_mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)

		# creating mesh 4*4
		squares_with_moves = []
		num_of_square = 0
		#---------------
		# 0  1  2  3
		# 4  5  6  7
		# 8  9  10 11
		# 12 13 14 15
		#---------------

		height = mask.shape[0]
		width = mask.shape[1]

		h_step = int(height/4)
		w_step = int(width/4)

		for i in range(0, height, h_step):
			for j in range(0, width, w_step):
				roi_of_mask = mask[i:i+h_step, j:j+w_step]
				percentage = (np.count_nonzero(roi_of_mask) * 100)/ roi_of_mask.size
				if percentage >= 0.5: # 0.5 precent (0.5%)
					squares_with_moves.append(num_of_square)

				num_of_square = num_of_square + 1

				rgb_mask = cv2.rectangle(rgb_mask, (j, i), (j+w_step, i+h_step), (0, 255, 0), 2)
				#print("i: " + str(i) + " j: " + str(j) + " i+h_step: " + str(i+h_step) + " j+w_step: " + str(j+w_step))

		# percentage = (cv2.sumElems(difference)[0] * 100)/ (difference.size*255)
		# percentage = (np.count_nonzero(mask) * 100)/ mask.size
		# if percentage >= 100:
		# # 	print("FUUUCK")
		# if percentage >= 0.1:# 0.1 percent (0.1%)
		# 	print("move")
		# else:
		# 	print("stay")

		# mask = difference
		# height = mask.shape[0]
		# width = mask.shape[1]
		#res_kadr = mask

		# # color the mask red
		# Conv_hsv_Gray = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
		# ret, mask = cv2.threshold(Conv_hsv_Gray, 50, 255, cv2.THRESH_BINARY_INV)# |cv2.THRESH_OTSU
		# res_kadr = mask

		prev_kadr = current_kadr

		cv2.imshow("Diff: ", difference)
		#print("percentage: " + str(percentage) + " non_z: " + str(np.count_nonzero(mask)) + " size: " + str(mask.size))
		print("squares_with_moves: " + str(squares_with_moves))
		cv2.imshow("rgb_Mask: ", rgb_mask)

def main():
	#cap = cv2.VideoCapture("/home/slava/Source/YoloV3_OVN_Inference/input.avi")
	cap = cv2.VideoCapture(0)

	if (cap.isOpened() == False):
		print("Error opening video stream or file")
		exit()

	while(cap.isOpened()):
		# Capture frame-by-frame
		ret, frame = cap.read()
		if ret == True:
 
			# Display the resulting frame
			cv2.imshow('Frame',frame)
			#m_rec(frame) #work good
			#n_kadr_diff_m_rec(frame) #work good
			mesh_m_rec(frame)

			# Press Q on keyboard to  exit
			if cv2.waitKey(25) & 0xFF == ord('q'):
				break
 
		# Break the loop
		else:
			break
 
	# When everything done, release the video capture object
	cap.release()
 
	# Closes all the frames
	cv2.destroyAllWindows()

main()





