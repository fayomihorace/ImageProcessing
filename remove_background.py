"""
Create by fayomi horace at 07/10/2019
Replace background by your background colors [R,G,B]
Replace path by your input image path

"""
import numpy as np
from PIL import Image
from skimage import io
import matplotlib

def remove(path):
    print('start\n Please wait....')
    background = [0,0,0]
    img= io.imread(path)
    width, height = len(img) , len(img[0] ) 
    new_img = np.zeros((width, height, 4), dtype=np.uint8)
    for i in range(width):
        for j in range(height):
            if img[i][j][0] >background[0] and img[i][j][1] >background[1]  and img[i][j][2] >background[2] :
                new_img[i][j][0]= new_img[i][j][1]= new_img[i][j][2]= new_img[i][j][3]= 0
            else:
                new_img[i][j][0]= img[i][j][0]
                new_img[i][j][1]= img[i][j][1]
                new_img[i][j][2]= img[i][j][2]
                new_img[i][j][3]= 255
    img = Image.fromarray(new_img, 'RGB')
    print('end')
    new_path = path.split('.')[0] + '.out.png'
    matplotlib.image.imsave(new_path, new_img)
    print('Image succesfully created at '+ new_path)

path = 'img.jpg'
remove(path)