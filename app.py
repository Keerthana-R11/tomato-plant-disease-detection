from flask import Flask, request, jsonify, render_template
from PIL import Image
import google.generativeai as genai
import os
from dotenv import load_dotenv
import markdown

import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import json

# Load model and class labels
model = load_model('fmodel.h5')

with open('class_labels.json') as f:
    class_indices = json.load(f)

# Reverse the dictionary to get index → label
class_labels = list(class_indices.keys())
image_size = (224, 224)

def predict_disease(image_path):
    img = load_img(image_path, target_size=image_size)
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)
    predicted_class = np.argmax(prediction, axis=1)[0]
    predicted_label = class_labels[predicted_class]
    confidence = prediction[0][predicted_class] * 100

    return predicted_label, confidence

app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/explore')
def explore():
    return render_template('explore.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/service')
def service():
    return render_template('service.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/basket')
def basket():
    return render_template('basket.html')

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')

@app.route('/diagnosis')
def diagnosis():
    return render_template('diagnosis.html')

@app.route('/pest-control')
def pest_control():
    return render_template('pest-control.html')
    

# Function to save the uploaded image locally
def save_image_locally(file, filename, save_dir='images'):
    # Create the directory if it doesn't exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Build the full file path
    file_path = os.path.join(save_dir, filename)

    # Open the file in binary mode and write it to the directory
    with open(file_path, 'wb') as f:
        f.write(file.read())

    print(f"File saved at: {file_path}")
    return file_path

# Endpoint to handle image and input text
@app.route('/analyze', methods=['GET', 'POST'])
def analyze_image():
    if request.method == 'GET':
        # Render the HTML form when the route is accessed via GET
        return '''
            <html>
            <style>
                    body {
                    display:flex;
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f9;
                        color: #333;
                        margin: 0;
                        padding: 20px;
                        align-items:center;
                        justify-content:center;
                    }

                    .container {
                        max-width: 600px;
                        margin: 0 auto;
                        padding: 20px;
                        background-color: #fff;
                        border-radius: 8px;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    }

                    h1 {
                        color: #2c3e50;
                    }

                    form {
                        display: flex;
                        flex-direction: column;
                    }

                    label {
                        font-weight: bold;
                        margin-bottom: 5px;
                    }

                    input, button {
                        padding: 10px;
                        margin-bottom: 15px;
                        border: 1px solid #ddd;
                        border-radius: 4px;
                    }

                    button {
                        background-color:  #3c7c46;
                        color: white;
                        cursor: pointer;
                        height:40px;
                        width:140px;
                        margin-left:100px;
                        

                    }
                    .back-button {
                        display: inline-block;
                        padding: 10px 10px;
                        background-color:  #3c7c46; /* Change this to your preferred color */
                        color: white;
                        text-align: center;
                        text-decoration: none;
                        border-radius: 5px;
                        transition: background-color 0.3s;
                    }

                    .back-button:hover {
                        background-color: #0056b3; /* Darker shade for hover effect */
                    }

 
                </style>
                    
                <body>
                    
                    
                    <form method="POST" enctype="multipart/form-data" action="/analyze">
                    <h1>Plant Disease Analysis</h1>
                        
                        <label for="image">Upload Image:</label>
                        <input type="file" id="image" name="image" accept="image/*"><br><br>
                        <button type="submit">Analyze Image</button>
                       
                     <!-- Back to explore Link -->
                     <center>
                       <div class="back-link">
                        <a href="/explore" class="back-button">Back to explore</a>
                    </div>
                    </center>

                        </div>
                    </form>
                </body>
            </html>
        '''
    elif request.method == 'POST':
        try:
            # Get the input text and image from the request
            input_text = request.form.get('input_text')
            image_file = request.files['image']

            # Check if an image file was uploaded
            if image_file.filename == '':
                return jsonify({"error": "No selected file"}), 400

            # Save the uploaded image locally
            path=save_image_locally(image_file, image_file.filename)

            # Print input text and image filename for debugging
            print(f"Input Text: {input_text}")
            print(f"Uploaded Image: {image_file.filename}")

            res=predict_disease(path)

            # Return the AI response as HTML
            return f"""
             <html>
                <style>
                    body {{
                        font-family: 'Poppins', sans-serif;
                        background-color: #e0f7fa;
                        color: #333;
                        margin: 0;
                        padding: 20px;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        min-height: 100vh;
                    }}

                    .container {{
                        background-color: #ffffff;
                        border-radius: 15px;
                        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
                        padding: 30px;
                        max-width: 700px;
                        text-align: center;
                        transition: transform 0.3s ease-in-out;
                    }}

                    .container:hover {{
                        transform: scale(1.02);
                    }}

                    h1 {{
                        color: #00796b;
                        font-size: 2em;
                        margin-bottom: 20px;
                    }}

                    p {{
                        font-size: 1.1em;
                        line-height: 1.6;
                        color: #546e7a;
                    }}

                    .result-box {{
                        background-color: #f1f8e9;
                        border: 2px solid #aed581;
                        border-radius: 10px;
                        padding: 20px;
                        margin-top: 20px;
                        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05);
                    }}

                    label {{
                        font-weight: bold;
                        margin-bottom: 10px;
                        display: block;
                        color: #00796b;
                    }}

                    input, button {{
                        padding: 12px;
                        border: 1px solid #ddd;
                        border-radius: 8px;
                        margin-bottom: 15px;
                        width: 100%;
                        font-size: 1em;
                    }}

                    button {{
                        background-color: #00796b;
                        color: white;
                        cursor: pointer;
                        border: none;
                        transition: background-color 0.3s;
                    }}

                    button:hover {{
                        background-color: #004d40;
                    }}

                    .ai-response {{
                        margin-top: 20px;
                        font-style: italic;
                        color: #2e7d32;
                    }}
                    .back-button {{
                            display: inline-block;
                            padding: 10px 10px;
                            background-color:  #3c7c46; /* Change this to your preferred color */
                            color: white;
                            text-align: center;
                            text-decoration: none;
                            border-radius: 5px;
                            transition: background-color 0.3s;
                        }}

                        .back-button:hover {{
                            background-color: #0056b3; /* Darker shade for hover effect */
                        }}

                </style>
                <body>
                    <div class="container">
                        <h1>Plant Disease Analysis</h1>
                        <p>Species: {input_text}</p>
                        <p>Uploaded Image: {image_file.filename}</p>
                        <div class="result-box">
                        <label>AI Response:</label>
                        <p class="ai-response">{res[0]} with confidence {res[1]}</p>
                  <!-- Back to explore Link -->*
                        <div class="back-link">
                            <a href="/explore" class="back-button">Back to explore</a>
                        </div>
                    </div>

                        </div>
                    </div>
                </body>
            </html> 
            """

        except Exception as e:
            print(f"Error: {str(e)}")  # Print the error for debugging
            return jsonify({"error": str(e)}), 500


# Function to load OpenAI model and get responses
def get_gemini_response(input_text, image):
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt_template = """
        Analyze the image to determine if it is related to plants or leaves:

        1. Identify the botanical and common names.
        2. Detect diseases and suggest treatments.
    """

    # Create the prompt based on input_text
    final_prompt = f"{input_text}\n\n{prompt_template}" if input_text else prompt_template
    
    # Generate a response using the model
    response = model.generate_content([final_prompt, image])
    
    return response.text

if __name__ == '__main__':
    app.run(debug=True)
