import os
from rembg import remove
from PIL import Image

def get_unique_filename(directory, base_name, extension):
    """
    Generates a unique filename in the specified directory by incrementing the number
    in the filename until a unique name is found.
    """
    i = 100  # Start numbering from 100
    while True:
        filename = f"{base_name}{i}.{extension}"
        if not os.path.exists(os.path.join(directory, filename)):
            return filename
        i += 1

# Paths
inputPath = './cars/car3.png'
output_dir = './outputs/'
result_dir = './results/'

# Generate a unique output filename
output_filename = get_unique_filename(output_dir, 'output', 'png')
outputPath = os.path.join(output_dir, output_filename)

# Open the input image
input_image = Image.open(inputPath)

# Remove the background
output_image = remove(input_image)

# Save the output image
output_image.save(outputPath)

# Load the images for the next step
foreground = Image.open(outputPath)
background = Image.open('./backgrounds/back3.jpeg')

# Resize the foreground image to be half the width of the background image,
# maintaining the aspect ratio for the height.
foreground_width = background.width // 2
aspect_ratio = foreground_width / foreground.width
foreground_height = int(foreground.height * aspect_ratio)
foreground = foreground.resize((foreground_width, foreground_height), Image.Resampling.LANCZOS)
foreground = foreground.convert("RGBA")

# Calculate the position to place the foreground in the right-bottom corner
position = (
    background.width - foreground.width,
    background.height - foreground.height
)

# Ensure the background is in RGBA mode
background = background.convert("RGBA")

# Paste the foreground onto the background at the right-bottom corner
background.paste(foreground, position, foreground)

# Generate a unique result filename
result_filename = get_unique_filename(result_dir, 'result', 'png')
resultPath = os.path.join(result_dir, result_filename)

# Save the resulting image
background.save(resultPath)




# combined_image = Image.alpha_composite(background.convert("RGBA"), foreground)

# combined_image.save('./result2.png') # make it dynamic result number like result100, result101 for every run