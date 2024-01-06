import os

print("Current working directory:", os.getcwd())
image_path = "images/cross.png"
print("Resolved image path:", os.path.abspath(image_path))