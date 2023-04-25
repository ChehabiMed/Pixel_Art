# Pixel_Art

## How to use the program:

To begin you need to put your data base images in the same folder, you can put all type of images the program can filter other extentions that PNG, JPG JPEG, and also can convert NON-RGB images to RGB.
Now we put our python file programs (pixelize.py and utils.py) in the same folder, then we open the CMD and navigate to our folder.
This image show the files in my folder, it is not mandatory to put the input image or the data_base with the other files.

![](https://github.com/ChehabiMed/Pixel_Art/blob/main/readme_pictures/Capture1.JPG)

We can write the following command to get help.
```
pixelize.py -h
```
![](https://github.com/ChehabiMed/Pixel_Art/blob/main/readme_pictures/Capture2.JPG)

It is mandatory to type the command as follow to execute the program:
``` 
pixelize.py  data_base_path  image to pixelize_path  ratio  kernel_size
```
After this command the image will appear at the end and won’t be saved.
![](https://github.com/ChehabiMed/Pixel_Art/blob/main/readme_pictures/Capture3.JPG)
If you want to save the image you need to add one optional argument (-s 1) that will save the image at the same folder of the program.
``` 
pixelize.py  data_base_path  image to pixelize_path  ratio  kernel_size   –s 1	
``` 
![](https://github.com/ChehabiMed/Pixel_Art/blob/main/readme_pictures/Capture4.JPG)

The image will be saved.
## Functions used in the code:
**verify_PNG_JPG(folder_path)**
This function takes the path of a folder as input and checks that the images it contains have the extensions .png, .jpg or .jpeg. If an image does not have one of these extensions, it is deleted. If it has one of these extensions, it is renamed with the prefix "img" followed by a sequential number. The images are thus renamed so that there are no duplicates in the names. If the folder does not contain any images with one of the mentioned extensions, no operation is performed.
**resize_images(folder_path, finale_size, output_dir)**
This function takes the path of a folder, the desired final size for the images, and the path of the output folder as input. It resizes all the images in the input folder to the desired final size while maintaining the height/width ratio. If an output folder is specified, the resized images are saved in this folder. Otherwise, they are saved in the input folder by overwriting the original images.
**convert_to_RGB(folder_path)**
This function takes the path of a folder as input and checks that the images it contains are in the RGB format. If an image is not in the RGB format, it is converted to RGB and saved.
**mean_color_DB_images(folder_path)**
This function takes the path of a folder as input and returns a list of tuples containing the name of each image in the folder and the average value of its colors. The average value is calculated for each color channel (red, green, blue) of each image using the numpy library.
**mean_color_pixels_image(image_path, kernel_size)**
This function takes the path of an image and the size of the kernel as input. It divides the image into square regions of size kernel_size and calculates the average color value of each region. It returns an image where each region is replaced by a pixel with the average value color of that region.
**color_distance(color1, color2, image_name, temporary_folder)**
This function calculates the Euclidean distance between two colors. The two colors are represented as a triplet of RGB values. This function is used to calculate the distance between the average color of an image and a given reference color. The path of this temporary folder must be passed as a parameter, in order to delete it if there’s an error.
## The main code explanation:
The main code pixelizes an input image by finding the closest match in a database of pre-existing images saved in a data base folder.  The pixelization is performed by dividing the input image into small regions and replacing each region with the closest matching image from the database, resized depending on the ratio chosen, dataset image size = ratio*kernel_size.
**It means that if size kernel=10 and ratio=4, we will replace every 10 pixel of the image by a 40 pixel image from our database!!**
![files used in my code.](https://github.com/ChehabiMed/Pixel_Art/blob/main/readme_pictures/Capture5.JPG)
The first part of the code sets up the input and output paths, as well as parameters such as the ratio of the output image size to the kernel size used to calculate the mean color of each region in the input image.
![the input image](https://github.com/ChehabiMed/Pixel_Art/blob/main/readme_pictures/Capture6.JPG)
Next, the code calls a function ```verify_PNG_JPG``` to ensure that all images in the database are either PNG or JPG or JPEG and also to renamed images with the prefix "img" followed by a sequential number this.
![data base folder with strange names before the code](https://github.com/ChehabiMed/Pixel_Art/blob/main/readme_pictures/Capture7.JPG)
![data base after filtering and renaming](https://github.com/ChehabiMed/Pixel_Art/blob/main/readme_pictures/Capture8.JPG)
And another function ```resize_images``` to resize all images in the database to a fixed size and store them in a temporary directory.
![the temporary folder created by the program.](https://github.com/ChehabiMed/Pixel_Art/blob/main/readme_pictures/Capture9.JPG)
![resized images stored in the temporary folder.](https://github.com/ChehabiMed/Pixel_Art/blob/main/readme_pictures/Capture10.JPG)
Then, the code calls a function ```convert_to_RGB``` to convert all images in the temporary directory to RGB format.
![](https://github.com/ChehabiMed/Pixel_Art/blob/main/readme_pictures/Capture11.JPG)
And another function mean_color_DB_images to calculate the mean color of each image in the temporary directory and store them in a list.
![](https://github.com/ChehabiMed/Pixel_Art/blob/main/readme_pictures/Capture12.JPG)
Next, the code calculates the mean color of each pixel in the input image using a kernel chosen by the user by using the function ```mean_color_pixels_image``` and replace every kernel by a pixel with the RGB value of the mean color of every pixel of that kernel and return the resulting image that we will call ```mean_color_image```, and now we just need to match every pixel with the corresponding image in the data base.
![](https://github.com/ChehabiMed/Pixel_Art/blob/main/readme_pictures/Capture13.JPG)
We initializes an empty numpy array with a size equal to:
Where we will store the final pixelized image after calculations.
![](https://github.com/ChehabiMed/Pixel_Art/blob/main/readme_pictures/Capture14.JPG)
Finally, the code loops over each pixel in the mean_color_image, finds the closest match in the database, loads the chosen image, and stores it in the final image array. The progress of the pixelization process is printed to the console.
![](https://github.com/ChehabiMed/Pixel_Art/blob/main/readme_pictures/Capture15.JPG)
## The results:
This is the resulting image.
![this is the resulting image.](https://github.com/ChehabiMed/Pixel_Art/blob/main/readme_pictures/Capture16.JPG)
let's zoom in!
![let's zoom in!](https://github.com/ChehabiMed/Pixel_Art/blob/main/readme_pictures/Capture17.JPG)
## TO DO!
graphical interface




