import os
import shutil

# === CONFIGURATION ===
source_folder = r'C:\Users\bslid.BENJI-PC\OneDrive\Dokumente\MC\capes\cape.mc'
destination_folder = r'C:\Users\bslid.BENJI-PC\OneDrive\Dokumente\MC\capes\cape.png'

# Create output folder if it doesn't exist
os.makedirs(destination_folder, exist_ok=True)

# Go through all files recursively
for root, dirs, files in os.walk(source_folder):
    for file in files:
        source_file_path = os.path.join(root, file)

        # Get name of the immediate parent folder (not full path)
        parent_folder = os.path.basename(root)

        # Build new filename: [foldername]_[originalname].png
        new_file_name = f"{parent_folder}_{file}.png"
        destination_file_path = os.path.join(destination_folder, new_file_name)

        # Copy file
        shutil.copy2(source_file_path, destination_file_path)
        print(f"Copied: {source_file_path} → {destination_file_path}")

print("✅ Done: All files copied with folder name prefix and '.png' added.")
