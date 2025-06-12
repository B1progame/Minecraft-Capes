import cv2
import os
import shutil

# === CONFIGURATION ===
template_path = r'C:\Users\bslid.BENJI-PC\OneDrive\Dokumente\MC\capes\cape_orgi_ch.png'         # Your reference image
search_folder = r'C:\Users\bslid.BENJI-PC\OneDrive\Dokumente\MC\capes\cape.png'            # Folder to search in
output_folder = r'C:\Users\bslid.BENJI-PC\OneDrive\Dokumente\MC\capes\output'                        # Folder to copy matches to
threshold = 0.95                                            # Matching threshold

# === Setup ===
os.makedirs(output_folder, exist_ok=True)

# Load the template image
template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
template_h, template_w = template.shape[:2]

# Go through each .png in the search folder
for filename in os.listdir(search_folder):
    if filename.lower().endswith('.png'):
        filepath = os.path.join(search_folder, filename)
        image = cv2.imread(filepath, cv2.IMREAD_UNCHANGED)

        if image is None or image.shape[0] < template_h or image.shape[1] < template_w:
            continue  # Skip invalid or too-small images

        # Template matching
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)

        if max_val >= threshold:
            print(f"✅ MATCH: {filename} (score: {max_val:.3f})")

            # Copy matching image to output folder
            shutil.copy2(filepath, os.path.join(output_folder, filename))
        else:
            print(f"❌ No match: {filename} (score: {max_val:.3f})")

print("🔍 Done. Matching files have been copied.")
