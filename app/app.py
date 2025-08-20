import cv2
import os
import shutil
from flask import Flask, render_template, request, redirect, url_for
from utils import delete_files, get_shift_name
from database.db_operations import retrieve, insert_measurement_row
from features.measurements import measure_locking_bar

# temp paths for images
IMAGE_PATH = 'static/capture.jpeg'
GREYSCALE_PATH = 'static/greyscale.jpeg'

# Delete existing temp images if they exist in static folder
delete_files([IMAGE_PATH, GREYSCALE_PATH])

# Initialize Flask app
app = Flask(__name__)

# -------------------------------
# ROUTE 1: Landing Page (Autoliv)
# -------------------------------
@app.route("/")
def home():
    return render_template("index.html")  # landing page (your uploaded template)


# ------------------------------------------
# ROUTE 2: Dimensional Measurement Page
# ------------------------------------------
@app.route('/dimensional-inspection', methods=['GET', 'POST'])
def dimensional_inspection():
    image_exists = os.path.exists(IMAGE_PATH)
    greyscale_exists = os.path.exists(GREYSCALE_PATH)

    # Default values for form fields
    model_number = ''
    selected_part = ''
    measurement_type = ''
    shift_name = ''
    measurement_value = 10
    retrieved_data = []
    is_ok = True
    
    # fetch unique part numbers from the database
    fetch_data = retrieve()
    part_numbers = set([item['part_number'] for item in fetch_data]) 

    if request.method == 'POST':
        # Get form values
        model_number = request.form.get('model_number', '')
        selected_part = request.form.get('part_number', '')
        measurement_type = request.form.get('measurement_type', '')

        # automatically fetch shift name
        shift_name = get_shift_name()
        
        # Retrieve info from the database based on selected part and measurement type
        retrieved_data = retrieve(selected_part, measurement_type) 
        
        # when capture button is clicked
        if 'capture' in request.form:
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            cap.release()
            if ret:
                cv2.imwrite(IMAGE_PATH, frame)
                print("Image saved at", IMAGE_PATH)
                image_exists = True

        # when measurement button is clicked
        elif 'measurement' in request.form and image_exists:
            img = cv2.imread(IMAGE_PATH)
            grey, measurement_value = measure_locking_bar(img)
            cv2.imwrite(GREYSCALE_PATH, grey)
            greyscale_exists = True 

        # when submit button is clicked
        elif 'submit' in request.form and image_exists and greyscale_exists:
            # Save images to a new folder
            folder_name = model_number or 'default_folder'
            folder_path = os.path.join('data', folder_name)
            os.makedirs(folder_path, exist_ok=True)
            shutil.copy(IMAGE_PATH, os.path.join(folder_path, f"{folder_name}_original.jpeg"))
            shutil.copy(GREYSCALE_PATH, os.path.join(folder_path, f"{folder_name}_greyscale.jpeg"))
            # Delete images from static path
            delete_files([IMAGE_PATH, GREYSCALE_PATH])
            
            # Save in DB
            insert_measurement_row(
                model_number, retrieved_data[0]["measurement_id"], retrieved_data[0]["part_number"],
                None, "Pass", measurement_value, "2025-07-30", shift_name,
                "Melroy", folder_path, None, None, None, "2025-07-30", "admin"
            )
            
            # Reset values after submission
            model_number = ''
            selected_part = ''
            measurement_type = ''
            measurement_value = ''
            retrieved_data = []
            is_ok = False
            image_exists = False
            greyscale_exists = False

    # Render template with variables
    return render_template(
        'dimensional.html',
        measurement_exists=greyscale_exists,
        image_exists=image_exists,
        part_numbers=part_numbers,
        model_number=model_number,
        selected_part=selected_part,
        measurement_type=measurement_type,
        shift_name=shift_name,
        measurement_value=measurement_value,
        retrieved_data=retrieved_data,
        is_ok=is_ok
    )


if __name__ == '__main__':
    app.run(debug=True)
