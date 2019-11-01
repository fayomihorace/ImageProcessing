"""
Created by Horace FAYOMI at 1/11/2019
"""

import cv2, os, sys
import numpy as np# Reading in and displaying our image

folder=None

class Slice:
	def __init__(self, xmin, ymin, xmax, ymax):
		self.xmin = xmin
		self.ymin = ymin
		self.xmax = xmax
		self.ymax = ymax

	def print(self):
		print(self.xmin, ' ', self.ymin, ' ', self.xmax, ' ', self.ymax)

	def write(self, img, path):
		roi = img[self.ymin:self.ymax,self.xmin:self.xmax]
		cv2.imwrite(path, roi)



def sharp(image):
	cv2.imshow('Original', image)# Create our shapening kernel, it must equal to one eventually
	kernel_sharpening = np.array([[-1,-1,-1], 
	                              [-1, 9,-1],
	                              [-1,-1,-1]])# applying the sharpening kernel to the input image & displaying it.
	sharpened = cv2.filter2D(image, -1, kernel_sharpening)
	cv2.imshow('Image Sharpening', sharpened)
	cv2.waitKey(0)
	cv2.destroyAllWindows()



def rotate_im(imgName, angle):
    
    image = cv2.imread(folder+ '/'+ imgName)
    image_height = image.shape[0]
    image_width = image.shape[1]
    diagonal_square = (image_width*image_width) + (
        image_height* image_height
    )
    #
    diagonal = round( (diagonal_square)**(0.5))
    padding_top = round((diagonal-image_height) / 2)
    padding_bottom = round((diagonal-image_height) / 2)
    padding_right = round((diagonal-image_width) / 2)
    padding_left = round((diagonal-image_width) / 2)
    padded_image = cv2.copyMakeBorder(image,
                                      top=padding_top,
                                      bottom=padding_bottom,
                                      left=padding_left,
                                      right=padding_right,
                                      borderType=cv2.BORDER_CONSTANT,
                                      value=0
            )
    padded_height = padded_image.shape[0]
    padded_width = padded_image.shape[1]
    transform_matrix = cv2.getRotationMatrix2D(
                (padded_height/2,
                 padded_width/2), # center
                angle, # angle
      1.0) # scale
    rotated_image = cv2.warpAffine(padded_image,
                                   transform_matrix,
                                   (diagonal, diagonal),
                                   flags=cv2.INTER_LANCZOS4)
    new_path = folder +'/new_images/rotate/' + imgName.split('.')[0]+ 'rotated'+ str(angle) +'.jpg'	
    print('write' , new_path)
    cv2.imwrite(new_path, rotated_image)



def affine(imgName, v1):
	img = cv2.imread(folder+ '/'+ imgName)
	rows,cols,ch = img.shape
	pts1 = np.float32([[v1,v1],[ 150+v1, v1],[v1,150+v1]])
	pts2 = np.float32([[ max(10, v1-40), 50+v1], [150+v1,v1],[50+v1,200+v1]])
	M = cv2.getAffineTransform(pts1,pts2)
	dst = cv2.warpAffine(img,M,(cols+300,rows+100))

	new_path =   folder+'/new_images/affine/' + imgName.split('.')[0]+ 'affine'+ str(v1) +'.jpg'
	print('write' , new_path)
	cv2.imwrite(new_path, dst)



def sliceImage(img, img_name, number_x, number_y):
	height, width, channels = img.shape	
	x_coordinates = [ int(width*i/number_x) for i in range(number_x+1) ]
	y_coordinates = [ int(height*i/number_y) for i in range(number_y+1) ]

	#print(x_coordinates,'\n', y_coordinates)
	slices = []
	xs = []
	ys = []
	for i in range(1, len(x_coordinates)):
		xs.append( ( x_coordinates[i-1], x_coordinates[i] ) )

	for i in range(1, len(y_coordinates)):
		ys.append( ( y_coordinates[i-1], y_coordinates[i] ) )
	#print(xs,'\n', ys)
	#"""
	for x in  xs:
		for y in ys:
			slices.append( Slice(x[0], y[0], x[1],y[1]) )

	for i in range(len(slices)):
		s= slices[i]
		#s.print()
		s.write( img, folder+'/new_images/slice/' + str(i)+ '_'+ img_name.split('.')[0]+ '.jpg')
	#"""



def reduce( img_name):
	img0 = cv2.imread( folder+'/' + img_name)
	height, width, channels = img0.shape	
	scale_percent = 640*100/width 
	width = int(img0.shape[1] * scale_percent / 100)
	height = int(img0.shape[0] * scale_percent / 100)
	#dim = (width, height)
	dim = (640, 480)
	# resize image
	img = cv2.resize(img0, dim, interpolation = cv2.INTER_AREA)
	cv2.imwrite( folder+"/new_images/reduce/"+ img_name, img)








def help():
	print("Use command")
	print("	-rotation: 	python run.py  <input_images_folder_path>  -r  <number>    <angle_incrementation> ")
	print("	-slice:		python run.py  <input_images_folder_path>  -s  <number_x>  <number_y> ")
	print("	-affine:	python run.py  <input_images_folder_path>  -a  <var>     (var is integer and var >=40) ")
	exit()

try:
	if (sys.argv[2]!='-r' and sys.argv[2]!='-s' and sys.argv[2]!='-a'): help()
except Exception as e:
	help()

else:
	#try:
	if (1==1):
		print('please wait .....')
		folder = sys.argv[1]
		type_ = sys.argv[2]
		os.popen('mkdir -p '+ folder+"/new_images/slice/")
		os.popen('mkdir -p '+ folder+"/new_images/rotate/")
		os.popen('mkdir -p '+ folder+"/new_images/affine/")
		imgs = [ img.split('/')[-1] for img in os.popen('ls  '+folder+'/*.*' ).read().split('\n')[:-1] ]
		print(imgs) 
		if type_== '-r':
			angle = 0
			for i in range( int(sys.argv[3]) ):
				angle+= int(sys.argv[4])
				for img in imgs: rotate_im( img, angle )
		
		elif type_== '-s':
			#for each images
			i = 0
			for i in range(len(imgs)):
				img= imgs[i]
				imgFile = cv2.imread(folder+'/' +img)
				sliceImage( imgFile, img , int(sys.argv[3]), int(sys.argv[4]))

		elif type_== '-a':
			i = 0
			for i in range(len(imgs)):
				img= imgs[i]
				affine( img, int(sys.argv[3]) )

		print('end')
