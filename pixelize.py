from PIL import Image
import numpy as np
from utils import convert_to_RGB
from utils import verify_PNG_JPG
from utils import resize_images
from utils import mean_color_DB_images
from utils import mean_color_pixels_image
from utils import color_distance
import os
import shutil
import argparse


# Define the command line arguments
parser = argparse.ArgumentParser(description='Pixelize an image using a database of images')
parser.add_argument('database_path', type=str, help='Path to the image database')
parser.add_argument('input_image_path', type=str, help='Path to the input image')
parser.add_argument('ratio', type=int, help='ratio equal to 3 by default (the kernel will be replaced by an image of size = ratio*kernel) size')
parser.add_argument('kernel_size', type=int, help='Size of the kernel for mean color calculation equal to 10 by default')
parser.add_argument('-s', '--save_image', type=bool, default=False, help='Save the pixelized image to file')
args = parser.parse_args()

dataBase_Path = args.database_path # path to directory containing images to be used for pixelization
img_to_pixelize_path = args.input_image_path # path to input image to be pixelized
ratio = args.ratio #the size ratio if it is two, the size is two times the kernel
kernel_size = args.kernel_size # size of the kernel used to calculate mean color of each pixel in input image
resize_size = ratio*kernel_size # size of the output images of database 
temporary_dir_path = "temporary_directory" # path to temporary directory to store resized images and calculate mean colors

#make sure that the temporary_folder doesn't exist
try:
    if os.path.exists(temporary_dir_path):
        shutil.rmtree(temporary_dir_path)
        print("we found a folder named temporary directory and we did delete it.\n")
except Exception as e:
    print("you need to delete the temporary_directory befor running the program :", e)

# Verify that all images in the data base are either PNG or JPG
verify_PNG_JPG(dataBase_Path)

# Resize all images in the data base to a fixed size and store them in a temporary directory
resize_images(dataBase_Path, resize_size, temporary_dir_path)

# Convert all images in the temporary directory to RGB format
convert_to_RGB(temporary_dir_path)

# Calculate the mean color of each image in the temporary directory and store them in a list
DB_colorsList = mean_color_DB_images(temporary_dir_path)

# Calculate the mean color of each pixel in the input image using a kernel and store it in a numpy array
mean_color_image = mean_color_pixels_image(img_to_pixelize_path,kernel_size)

# Initialize an empty numpy array to store the final pixelized image
height, width, *channels = mean_color_image.shape
downscaled_shape = (height*resize_size, width*resize_size, *channels)
final_image = np.zeros(downscaled_shape, dtype=np.uint8)

# Loop over each pixel in the mean color image and find the closest match in the data base
for i in range(mean_color_image.shape[0]):
    print("processing...")
    for j in range(mean_color_image.shape[1]):
        closest_distance = float('inf')
        closest_image_color = None
        for image_name, mean_color in DB_colorsList:
            # Calculate the color distance between the current pixel in the mean color image and the mean color of the current image in the data base
            distance = color_distance(mean_color_image[i,j], mean_color,image_name, temporary_dir_path)
            # If the color distance is smaller than the previous smallest distance, update the closest distance and closest image color
            if distance < closest_distance:
                closest_distance = distance
                closest_image_color = image_name
        # Load the closest image from the data base, resize it to the desired pixel size, and store it in the final image array
        chosed_image = np.array(Image.open(os.path.join("temporary_directory",closest_image_color)))
        final_image[i*resize_size:(i+1)*resize_size,j*resize_size:(j+1)*resize_size] = chosed_image.astype(np.uint8)
    print("please wait...")

image2 = Image.fromarray(final_image)

print("Here's the result in some seconds...")


if args.save_image == True:
    image2.save("pixelized_image.png")
    print("Pixelized image saved to pixelized_image.png")
else:
    image2.show()

shutil.rmtree(temporary_dir_path)