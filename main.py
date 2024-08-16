from rembg import remove
from PIL import Image

# Specify the input and output paths
inputPath = './car2.png'
outputPath = './output.png'

# Open the input image
input_image = Image.open(inputPath)

# Remove the background
output_image = remove(input_image)

# Save the output image
output_image.save(outputPath)


foreground = Image.open('./output.png')
background = Image.open('./background.jpg')

background = background.resize(foreground.size)

# Ensure the foreground is in RGBA mode to handle transparency
foreground = foreground.convert("RGBA")

# Composite the foreground onto the background
combined_image = Image.alpha_composite(background.convert("RGBA"), foreground)

# Save the resulting image
combined_image.save('./output_with_new_background.png')