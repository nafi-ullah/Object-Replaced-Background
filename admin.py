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
    prompt = "Set the following car mentioned in image infront of hyundai showroom. Dont change the car's design." 
    image = request.files['image']
    # if not image or not prompt:
    #     return jsonify({'error': 'Image and prompt are required.'}), 400
    print(image)
    gpt_analysis = analyze_image_and_prompt("https://www.shutterstock.com/image-photo/biysk-russia-circa-september-2017-260nw-735050692.jpg", prompt)
    print(gpt_analysis)
    generated_image = generate_dalle_image(gpt_analysis)
    
    return jsonify({'generated_image': generated_image})

if __name__ == '__main__':
    app.run(debug=True)
