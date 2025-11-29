from rembg import remove
from PIL import Image

input_path = "phone-alert.png"
output_path = "phone-alert.png"

with open(input_path, "rb") as input_file:
    input_data = input_file.read()

output_data = remove(input_data)

with open(output_path, "wb") as output_file:
    output_file.write(output_data)

print(f"Background removed! Saved to {output_path}")
