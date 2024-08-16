from rembg import remove
from PIL import Image

inputPath = './cars/car3.png'
outputPath = './outputs/output101.png' # make it dynamic output number like output100, output101 for every run if the same name exist increast the value

# Open the input image
input_image = Image.open(inputPath)

# Remove the background
output_image = remove(input_image)

# Save the output image
output_image.save(outputPath)


foreground = Image.open(outputPath) 
background = Image.open('./backgrounds/back3.jpeg') 

# background = background.resize(foreground.size)
foreground = foreground.resize((background.width // 2, background.height // 2))
foreground = foreground.convert("RGBA")
position = (
    (background.width - foreground.width) // 2,
    (background.height - foreground.height) // 2
)
background = background.convert("RGBA")
background.paste(foreground, position, foreground)
background.save('./results/result2.png') # make it dynamic result number like result100, result101 for every run for every run if the same name exist increast the value

# combined_image = Image.alpha_composite(background.convert("RGBA"), foreground)

# combined_image.save('./result2.png') # make it dynamic result number like result100, result101 for every run