from PIL import Image
import numpy as np
import os
from os import listdir
import math
import shutil


def verify_PNG_JPG(folder_path):
    """
    Verify that all files in a folder are PNG or JPG images, rename them, and remove any non-image files.

    :param folder_path: Path to the folder containing the files.

    """
    try:
        # set a prefix for the new image names
        prefix = "img"
        # set the starting index for the new image names
        index = 1
        # loop through each file in the folder
        for image_name in os.listdir(folder_path):
            # check if the file is an image file with a valid extension (png, jpg, or jpeg)
            if image_name.lower().endswith((".png",".jpg",".jpeg")):
                # get the file extension
                extension = os.path.splitext(image_name)[1]
                # create a new name for the file with the prefix, index, and original extension
                new_name = os.path.join(folder_path, f"{prefix}{index}{extension}")
                # check if a file with the new name already exists and increment the index if it does
                while os.path.exists(new_name):
                    index += 1
                    new_name = os.path.join(folder_path, f"{prefix}{index}{extension}")
                # rename the file with the new name
                old_path = os.path.join(folder_path, image_name)
                os.rename(old_path, new_name)
                # increment the index for the next file
                index += 1
            else:
                # remove the file if it doesn't have a valid image extension
                file_path = os.path.join(folder_path, image_name)
                os.remove(file_path)
        # print a message indicating that the filtering and renaming is complete
        print("Done filtering and renaming files.\n")
    except Exception as e:
        # if an error occurs, print an error message
        print(f"An error occurred in filtering the valid extensions => {str(e)}\n")


def resize_images(folder_path, finale_size, output_dir):
    """
    Resize all images in a folder to a specified size.

    :param folder_path: path to the folder containing images.
    :param size: size of the output images (both width and height).
    :param output_dir: path to the output directory. If None, the resized images will be saved in the original folder.
    """
    # create the output directory if it doesn't exist
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # loop through each image in the folder
    for image_name in os.listdir(folder_path):
        try:
            # open the image and resize it to the specified size
            image_path = os.path.join(folder_path, image_name)
            with Image.open(image_path) as img:
                img = img.resize((finale_size, finale_size))
                # save the resized image to the output directory or the original folder
                if output_dir:
                    output_path = os.path.join(output_dir, image_name)
                else:
                    output_path = image_path
                img.save(output_path)
        except Exception as e:
            # if an error occurs, print an error message and remove any partial output
            print(f"Failed to resize image {image_name}: {str(e)}\n")
            if output_dir:
                shutil.rmtree(output_path)

    # print a message indicating that the resizing is complete
    print("Done resizing database images.\n")


def convert_to_RGB(folder_path):
    """
    Convert all images in a folder to the RGB color mode.

    :param folder_path: path to the folder containing images.
    """
    # loop through each image in the folder
    for image_name in os.listdir(folder_path):
        try:
            # open the image and check if it's already in RGB mode
            image_path = os.path.join(folder_path, image_name)
            with Image.open(image_path) as img:
                if img.mode != "RGB":
                    # if it's not in RGB mode, convert it and save the new image
                    print(f"The image {image_name} is not RGB.\n")
                    rgb_img = img.convert("RGB")
                    rgb_img.save(image_path)
                    print(f"The image {image_name} was converted to RGB.\n")
                
        except Exception as e:
            # if an error occurs, print an error message and remove any partial output
            print(f"Failed to convert {image_name} to RGB: {str(e)}")
            shutil.rmtree(image_path)


def mean_color_DB_images(folder_path):
    """
    Returns a list of tuples containing the name of each image file in a folder and its mean color value.

    Parameters:
    folder_path (str): The path to the folder containing the images.

    Returns:
    list: A list of tuples, where each tuple contains the name of an image file and its mean color value.
    """

    # initialize a list to store the image names and mean color values
    mean_color_list = []

    # iterate over each file in the folder
    for image_name in os.listdir(folder_path):
        image_path = os.path.join(folder_path, image_name)

        try:
            with Image.open(image_path) as img:
                # convert the image to a NumPy array
                array_image = np.array(img)

                # calculate the mean color value for each channel (red, green, blue) in the image array
                mean_color = np.mean(array_image, axis=(0, 1))

                # add the image name and mean color value to the list
                mean_color_list.append((image_name, mean_color))

        except Exception as e:
            print(f"Failed to read image {image_name}: {str(e)}\n")
            shutil.rmtree(folder_path)

    # print the list of images with their corresponding mean color values
    print("Done calculating the mean color of Database images.\n")
    print()

    return mean_color_list


def mean_color_pixels_image(image_path, kernel_size):
    """
    Downsamples an image and returns the mean color of pixels of each kernel.

    :param image_path: path of the input image
    :param kernel_size: size of the kernel for downsampling
    :return: downsampled image as a numpy array with mean color of each kernel
    """
    try:
        # open image using PIL library
        image = Image.open(image_path)
    except Exception as e:
        # handle exception if image could not be opened
        print(f"Failed to open the image to pixelize {image_path}: {str(e)}\n")
        return None
    
    if image.mode != "RGB":
        # if it's not in RGB mode, convert it and save the new image
        print(f"The image to pixelize is not RGB.\n")
        rgb_img = image.convert("RGB")
        rgb_img.save(image_path)
        print(f"The image to pixelize was converted to RGB.\n")

    # convert image to numpy array
    ArrayImage = np.array(image)
    # get height, width and channels of the image
    height, width, *channels = ArrayImage.shape
    # calculate the downsampled shape using the kernel size
    downscaled_shape = (height//kernel_size, width//kernel_size, *channels)
    # create a numpy array of zeros with the calculated downsampled shape
    color_image = np.zeros(downscaled_shape, dtype=np.uint8)

    # loop through each kernel and calculate the mean color of pixels in that kernel
    for i in range(0, height - kernel_size + 1, kernel_size):
        for j in range(0, width - kernel_size + 1, kernel_size):
            # get the kernel using the current position and kernel size
            kernel = ArrayImage[i:i+kernel_size, j:j+kernel_size, :]
            # calculate the mean color of the kernel along the height, width and channels axis
            mean_color = np.mean(kernel, axis=(0, 1)).astype(np.uint8)
            # set the mean color of the kernel to the corresponding position in the downsampled image
            color_image[i//kernel_size, j//kernel_size, :] = mean_color

    print("Done calculating the mean color of the kernels in the image to pixelize.\n")
    print()

    # return the downsampled image with mean color of each kernel
    return color_image


def color_distance(color1, color2, image_name, temporary_folder):
    """
    Calculates the Euclidean distance between two RGB color values.

    :param color1: tuple representing the first RGB color value.
    :param color2: tuple representing the second RGB color value.
    :param image_name: name of the image being processed to locate the image in case of error.
    :param temporary_folder: path to the temporary folder where image processing is being done in order to delete it in case of error.
    :return: Euclidean distance between the two RGB color values.
    """
    try:
        # Extract RGB channels from color tuples
        r1, g1, b1 = color1
        r2, g2, b2 = color2

        # Calculate Euclidean distance between the two RGB color values
        distance = math.sqrt((r2 - r1) ** 2 + (g2 - g1) ** 2 + (b2 - b1) ** 2)

        return distance
    except (ValueError, TypeError):
        # If input colors are not valid, delete the temporary folder and return None
        print("Input colors must be tuples of 3 values representing RGB channels. The following image must be deleted:")
        print("Image name: ", image_name, "\nImage shape: ", color2.shape, "\n")
        shutil.rmtree(temporary_folder)
        return None



'''
def main () :
    dataBase_Path = "data_base"
    print(dataBase_Path)
    verify_PNG_JPG(dataBase_Path)
    print( "done" )

if __name__ == "__main__" :
    main ()
'''