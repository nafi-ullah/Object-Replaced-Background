import os
from rembg import remove
from PIL import Image, ImageEnhance

def get_unique_filename(directory, base_name, extension):
    i = 100  # Start numbering from 100
    while True:
        filename = f"{base_name}{i}.{extension}"
        if not os.path.exists(os.path.join(directory, filename)):
            return filename
        i += 1

from PIL import ImageEnhance

def adjust_foreground_to_match_background(foreground):
    # Convert the image to grayscale to get brightness levels (optional)
    fg_gray = foreground.convert('L')

    # Slightly decrease brightness
    brightness_enhancer = ImageEnhance.Brightness(foreground)
    brightness_factor = 0.95  # Decrease brightness slightly (adjust as needed)
    foreground = brightness_enhancer.enhance(brightness_factor)
    
    # Slightly decrease contrast
    contrast_enhancer = ImageEnhance.Contrast(foreground)
    foreground = contrast_enhancer.enhance(0.98)
    
    # Optionally, adjust color balance if necessary
    # fg_color = ImageEnhance.Color(foreground)
    # foreground = fg_color.enhance(1.09)  # Increase color intensity slightly
    
    return foreground




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
background = Image.open('./backgrounds/backRight.jpeg')
foreground = adjust_foreground_to_match_background(foreground)

# Resize the foreground image to be half the width of the background image,
# maintaining the aspect ratio for the height.
scale_factor = 0.75  # Scale factor adjusted to make the car size more realistic
foreground_width = int(background.width * scale_factor)
aspect_ratio = foreground_width / foreground.width
foreground_height = int(foreground.height * aspect_ratio)
foreground = foreground.resize((foreground_width, foreground_height), Image.Resampling.LANCZOS)
foreground = foreground.convert("RGBA")

# Calculate the position to place the foreground in the right-bottom corner
position = (
    background.width - foreground.width + 50,  # Slightly shift to the left
    background.height - foreground_height - 100  # Align to the ground level
)
background = background.convert("RGBA")

background.paste(foreground, position, foreground)

result_filename = get_unique_filename(result_dir, 'result', 'png')
resultPath = os.path.join(result_dir, result_filename)
# Save the resulting image
background.save(resultPath)




# combined_image = Image.alpha_composite(background.convert("RGBA"), foreground)

# combined_image.save('./result2.png') # make it dynamic result number like result100, result101 for every run