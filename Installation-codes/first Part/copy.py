import os
import shutil

# === Setup ===
script_dir = os.path.dirname(os.path.abspath(__file__))

# List all subfolders in the script directory
subfolders = [f for f in os.listdir(script_dir) if os.path.isdir(os.path.join(script_dir, f))]

print("📁 Available folders in the script directory:")
for folder in subfolders:
    print(f" - {folder}")

# Ask user to choose a folder
source_folder_name = input("\nEnter the name of the folder you want to use as the source: ").strip()
source_folder = os.path.join(script_dir, source_folder_name)

# Check if folder exists
if not os.path.exists(source_folder):
    print(f"❌ Error: The folder '{source_folder_name}' does not exist.")
    exit(1)

# Create output folder
output_folder = os.path.join(script_dir, "output")
os.makedirs(output_folder, exist_ok=True)

# === Copy process ===
for root, dirs, files in os.walk(source_folder):
    for file in files:
        source_file_path = os.path.join(root, file)
        parent_folder = os.path.basename(root)
        
        # Create new filename with folder prefix and .png
        new_file_name = f"{parent_folder}_{file}.png"
        destination_file_path = os.path.join(output_folder, new_file_name)
        
        # Copy file
        shutil.copy2(source_file_path, destination_file_path)
        print(f"✅ Copied: {source_file_path} → {destination_file_path}")

print("\n🎉 Done: All files copied and renamed into the 'output' folder.")
