import os
import shutil
from datetime import datetime

# Get Downloads path (Windows)
downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")

# File categories
folders = {
    "Images": [".jpg", ".png", ".jpeg", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx"],
    "Videos": [".mp4", ".mkv", ".avi"],
    "Music": [".mp3", ".wav"],
    "Others": []
}

# Loop through files
for file in os.listdir(downloads_path):
    file_path = os.path.join(downloads_path, file)

    # Skip folders
    if os.path.isdir(file_path):
        continue

    ext = os.path.splitext(file)[1].lower()
    moved = False

    # Get file date
    created_time = os.path.getctime(file_path)
    date = datetime.fromtimestamp(created_time)
    year = str(date.year)
    month = date.strftime("%B")

    # Find category
    for folder, extensions in folders.items():
        if ext in extensions:
            target_folder = os.path.join(downloads_path, folder, year, month)
            os.makedirs(target_folder, exist_ok=True)

            shutil.move(file_path, os.path.join(target_folder, file))
            moved = True
            break

    # If not matched → Others
    if not moved:
        target_folder = os.path.join(downloads_path, "Others", year, month)
        os.makedirs(target_folder, exist_ok=True)
        shutil.move(file_path, os.path.join(target_folder, file))

print("✅ Downloads organized by type and date!")
