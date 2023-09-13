# Author: https://github.com/hafiz-muhammad
# Imports
import urllib.request
from PIL import Image
import datetime
import os.path
import urllib.error

# Get the absolute path of the script.
script_dir = os.path.abspath(__file__)

# Get the directory of the script.
script_dir = os.path.dirname(script_dir)

# Specify the subdirectory where images will be saved.
sub_dir = "images"

# Create the save path by joining the script directory with the subdirectory.
save_path = os.path.join(script_dir, sub_dir)

def check_directory(path):
    # Checks if the default directory exists in the parent directory, and creates it if not.
    if os.path.exists(path):
        print(f"Directory {path} already exists.")
    else:
        os.mkdir(path)
        print(f"Directory {path} created.")

# Prompts user for image URL.
url = input("Enter image URL: ")

# Prompts user for directory to save image.
directory = input("Input a directory to save image or press ENTER to save to default directory: ")
if not directory:
    directory = save_path

path = os.path.expanduser(directory)

check_directory(path)

def check_url(url):
    # Checks if URL starts with https:// or http://, adds https:// if not.
    if url.startswith("https://") or url.startswith("http://"):
        pass
    else:
        url = "https://" + url

check_url(url)

# Prompts user for file name, otherwise uses current date and time.
filename = input("Input a name for the image or press ENTER: ")
if not filename:
    filename = datetime.datetime.now().strftime("%m%d%Y-%H%M%S")

try:
    response = urllib.request.urlopen(url)

    def check_download_status(response):
        # Checks the HTTP response code to see if the image was downloaded successfully.
        if response.getcode() == 200: 
            print("\033[32mImage downloaded successfully!\033[0m")

    check_download_status(response)

    loaded_img = Image.open(response)

# Handles errors that may occur while downloading the image.
except urllib.error.HTTPError:
    print("\033[31mImage download failed!\033[0m")

# Gets image dimensions.
img_width = loaded_img.width
img_height = loaded_img.height

file_format = loaded_img.format.lower()

def get_filename_with_extension(filename):
    # Adds .png file extension to the end of the filename if it doesn't have one.
    if file_format:
        filename = filename + "." + file_format
    else:
        filename = filename + ".png"
    return filename

filename = get_filename_with_extension(filename)

# Opens the output file in binary write mode, 
# saves the image to the output file, and closes the output file.
output_file = open(os.path.join(path, filename), "wb")
loaded_img.save(output_file)
output_file.close()

# Prints image information.
print(f"""{chr(10)}\033[1;4mFile Information Summary\033[0m {chr(10)}
\033[1mName:\033[0m {filename.split(".")[0]}\033[0m.{filename.split(".")[1]}
\033[1mLocation:\033[0m {directory}
\033[1mImage dimensions:\033[0m {img_width}x{img_height} pixels
\033[1mFile size:\033[0m {os.stat(os.path.join(path, filename)).st_size} bytes 
{chr(10)}""")
