import os
from rembg import remove
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

def get_unique_filename(directory, base_name, extension):
    i = 100  # Start numbering from 100
    while True:
        filename = f"{base_name}{i}.{extension}"
        if not os.path.exists(os.path.join(directory, filename)):
            return filename
        i += 1

def adjust_foreground_to_match_background(foreground):
    # Ensure the image is in RGB or RGBA mode
    if foreground.mode not in ("RGB", "RGBA"):
        foreground = foreground.convert("RGB")

    # Slightly decrease brightness
    brightness_enhancer = ImageEnhance.Brightness(foreground)
    brightness_factor = 0.8  # Decrease brightness (adjust as needed)
    foreground = brightness_enhancer.enhance(brightness_factor)
    
    # Slightly decrease contrast
    contrast_enhancer = ImageEnhance.Contrast(foreground)
    contrast_factor = 0.85  # Decrease contrast (adjust as needed)
    foreground = contrast_enhancer.enhance(contrast_factor)
    
    return foreground

def add_shadow_to_object(image, offset=(50, 50), background_color=(255, 255, 255, 0), shadow_color=(0, 0, 0), blur_radius=5):
    # Create an image for the shadow
    shadow = Image.new('RGBA', image.size, background_color)
    
    # Create the shadow mask by converting the image to grayscale
    shadow_mask = image.convert('L')
    
    # Apply the shadow color to the mask
    shadow = ImageOps.colorize(shadow_mask, black=shadow_color, white=shadow_color)
    
    # Convert the shadow to 'RGBA' mode (to add an alpha channel)
    shadow = shadow.convert('RGBA')
    
    # Apply blur to the shadow to make it soft
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur_radius))
    
    # Create a new image to hold both the shadow and the original image
    combined = Image.new('RGBA', image.size, background_color)
    
    # Create the alpha mask for the shadow
    shadow_alpha = shadow_mask.filter(ImageFilter.GaussianBlur(blur_radius))
    
    # Paste the shadow onto the new image, offset by the desired amount
    combined.paste(shadow, offset, shadow_alpha)
    
    # Paste the original image on top of the shadow
    combined.paste(image, (0, 0), image)
    
    return combined



# Paths
inputPath = './cars/carai.png'
output_dir = './outputs/'
result_dir = './results/'

# Ensure output and result directories exist
os.makedirs(output_dir, exist_ok=True)
os.makedirs(result_dir, exist_ok=True)

# Generate a unique output filename
output_filename = get_unique_filename(output_dir, 'output', 'png')
outputPath = os.path.join(output_dir, output_filename)

# Open the input image
input_image = Image.open(inputPath).convert('RGBA')

# Remove the background
output_image = remove(input_image)

# Save the output image
output_image.save(outputPath)

# Load the images for the next step
foreground = Image.open(outputPath)
background = Image.open('./backgrounds/backRight.jpeg').convert('RGBA')

# Adjust the foreground image to match the background
foreground = adjust_foreground_to_match_background(foreground)

# Add shadow to the foreground object
# foreground = add_shadow_to_object(foreground)

# Resize the foreground image to be a proportion of the background's width, maintaining aspect ratio
scale_factor = 0.75  # Adjust to make the car size more realistic
foreground_width = int(background.width * scale_factor)
aspect_ratio = foreground_width / foreground.width
foreground_height = int(foreground.height * aspect_ratio)
foreground = foreground.resize((foreground_width, foreground_height), Image.Resampling.LANCZOS)

# Calculate the position to place the foreground in the bottom-right corner
position = (
    background.width - foreground.width - 50,  # Slightly shift to the left
    background.height - foreground_height - 100  # Align to the ground level
)

# Composite the foreground with the background
background.paste(foreground, position, foreground)

# Generate a unique result filename and save the final image
result_filename = get_unique_filename(result_dir, 'result', 'png')
resultPath = os.path.join(result_dir, result_filename)
background.save(resultPath)





# combined_image = Image.alpha_composite(background.convert("RGBA"), foreground)

# combined_image.save('./result2.png') # make it dynamic result number like result100, result101 for every run