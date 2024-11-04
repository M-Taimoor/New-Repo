from PIL import Image
import os
from fontTools.ttLib import TTFont

# Define a function to extract the dominant color from an image
def get_dominant_color(image_path):
    with Image.open(image_path) as img:
        img = img.convert('RGB')
        # Resize the image to reduce the number of pixels to process
        img = img.resize((50, 50), Image.LANCZOS)
        # Get colors from the image and aggregate them
        result = img.getcolors(2500)
        # Sort colors based on occurrence
        result.sort(key=lambda x: x[0], reverse=True)
        # Return the most frequent color
        dominant_color = result[0][1]
        return dominant_color

# Define a function to extract font properties from an image
def get_font_properties(image_path):
    # This is a placeholder function. In practice, you would need
    # to use OCR (Optical Character Recognition) to extract text and
    # then analyze the font properties using fontTools or a similar library.
    # For this example, we'll return a dummy font property.
    return {'font_name': 'Arial', 'font_size': 12}

# Define the directory containing theme images
theme_images_dir = './images'

# Define a standard color to compare against
standard_color = (255, 255, 255)  # Example standard color (white)

# Define standard typography properties to compare against
standard_font_name = 'Arial'
standard_font_size = 12

# List all image files in the directory
image_files = [f for f in os.listdir(theme_images_dir) if f.endswith('.jpg') or f.endswith('.png')]

# Analyze color and typography consistency
for image_file in image_files:
    image_path = os.path.join(theme_images_dir, image_file)
    
    # Extract dominant color
    dominant_color = get_dominant_color(image_path)
    
    # Extract font properties (dummy function in this example)
    font_properties = get_font_properties(image_path)
    
    # Compare the dominant color with the standard color
    if dominant_color == standard_color:
        print(f"{image_file} matches the standard color.")
    else:
        print(f"{image_file} does not match the standard color. Dominant color: {dominant_color}")
    
    # Compare typography properties with the standard
    if font_properties['font_name'] == standard_font_name and font_properties['font_size'] == standard_font_size:
        print(f"{image_file} matches the standard typography.")
    else:
        print(f"{image_file} does not match the standard typography. Font properties: {font_properties}")
