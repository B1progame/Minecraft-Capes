import cv2
import os
import shutil

# === SETUP ===
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define paths
template_path = os.path.join(script_dir, 'Cape.png')          # Template image
search_folder = os.path.join(script_dir, 'output')                    # Folder to search in
output_folder = os.path.join(script_dir, 'last-output')               # Matches go here

# Matching threshold
threshold = 0.95

# Check if search folder exists
if not os.path.exists(search_folder):
    print(f"❌ Error: Search folder '{search_folder}' does not exist.")
    exit(1)

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Load template image
template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
if template is None:
    print(f"❌ Error: Could not load template image from '{template_path}'")
    exit(1)

template_h, template_w = template.shape[:2]

# Go through images in the output folder
for filename in os.listdir(search_folder):
    if filename.lower().endswith('.png'):
        filepath = os.path.join(search_folder, filename)
        image = cv2.imread(filepath, cv2.IMREAD_UNCHANGED)

        if image is None or image.shape[0] < template_h or image.shape[1] < template_w:
            print(f"⚠️ Skipped (invalid or too small): {filename}")
            continue

        # Template matching
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)

        if max_val >= threshold:
            print(f"✅ MATCH: {filename} (score: {max_val:.3f})")
            shutil.copy2(filepath, os.path.join(output_folder, filename))
        else:
            print(f"❌ No match: {filename} (score: {max_val:.3f})")

print("\n🔍 Done. Matching images were copied to 'last-output'.")
