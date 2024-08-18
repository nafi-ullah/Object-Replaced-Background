from flask import Flask, request, jsonify
import os
from PIL import Image
from rembg import remove
from main import get_unique_filename, adjust_foreground_to_match_background, add_shadow_to_object
from aifunctions import analyze_image_and_prompt, generate_dalle_image

app = Flask(__name__)

UPLOAD_FOLDER = './uploaded_images/'
OUTPUT_DIR = './outputs/'
RESULT_DIR = './results/'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)

@app.route('/check', methods=['GET'])
def check():
    return jsonify(message="Hello, it's working")

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    image_file = request.files['image']

    if image_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    image_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
    image_file.save(image_path)

    input_image = Image.open(image_path).convert('RGBA')
    output_image = remove(input_image)

    output_filename = get_unique_filename(OUTPUT_DIR, 'output', 'png')
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    output_image.save(output_path)

    foreground = Image.open(output_path)
    background = Image.open('./backgrounds/backai.png').convert('RGBA')

    # Adjust foreground to match background
    # foreground = adjust_foreground_to_match_background(foreground)

    # Resize and position the foreground image
    scale_factor = 1
    foreground_width = int(background.width * scale_factor)
    aspect_ratio = foreground_width / foreground.width
    foreground_height = int(foreground.height * aspect_ratio)
    foreground = foreground.resize((foreground_width, foreground_height), Image.Resampling.LANCZOS)

    position = (
        background.width - foreground.width ,
        background.height - foreground_height 
    )

    # Paste foreground onto background
    background.paste(foreground, position, foreground)

    # Save the final result
    result_filename = get_unique_filename(RESULT_DIR, 'result', 'png')
    result_path = os.path.join(RESULT_DIR, result_filename)
    background.save(result_path)

    return jsonify({'result_path': result_path}), 200

@app.route('/generate-image', methods=['POST'])
def generate_image():
    # data = request.json
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    # image = data.get('image')
    # prompt = data.get('prompt')
    # prompt = "Set the following car infront of hyundai showroom mention in the image." 
    analysis = """
    Make and Model: The car appears to be a Toyota, specifically a Toyota Corolla hatchback, based on the design cues and emblem on the front grille.
    Body Type: The car is a hatchback, which is characterized by a rear door that swings upward to provide access to a cargo area.
    Color: The car is painted in a shiny metallic red, which is a vibrant and eye-catching color.
    Headlights: The car has sleek, angular headlights with a sharp design that adds to its modern and sporty look. The headlights seem to be equipped with LED technology.
    Grille: The front grille is large and features a honeycomb pattern, which is common in sportier models. The grille is black, contrasting sharply with the red body color.
    Wheels: The car has dark-colored alloy wheels with a multi-spoke design, contributing to the vehicle's sporty appearance. The wheels appear to be relatively large, which often suggests a focus on performance.
    Side Mirrors: The side mirrors are black, which contrasts with the red body. They are likely power-adjustable and could have integrated turn signals, which is common in modern cars.
    Windows: The car has tinted windows, providing privacy and a sleek look. The rear side windows and rear windshield seem to be more tinted than the front.
    Body Lines: The car features sharp and defined body lines along the side, giving it a dynamic and aggressive stance. These lines are typically designed to enhance aerodynamics and aesthetic appeal.
    Roofline: The car has a sloping roofline, which gives it a sporty, fastback appearance, adding to the aerodynamic profile.
    Bumper and Lower Body: The front bumper is designed with integrated air vents, which add to the sporty appearance and likely contribute to cooling. The lower body also has black accents, which are common in sportier trims.
    Overall Stance: The car has a low and wide stance, contributing to its sporty look. This is typical of hatchback models designed with performance in mind.
    """
    prompt = f"You have to change the background of the car. The car should be infront of hyundai car shop. The image description is: {analysis}."
    image = request.files['image']
    # if not image or not prompt:
    #     return jsonify({'error': 'Image and prompt are required.'}), 400
    print(image)
    # gpt_analysis = analyze_image_and_prompt("https://www.shutterstock.com/image-photo/biysk-russia-circa-september-2017-260nw-735050692.jpg", prompt)
    # print(gpt_analysis)
    generated_image = generate_dalle_image(prompt, image)
    
    return jsonify({'generated_image': generated_image})

if __name__ == '__main__':
    app.run(port=5055)
