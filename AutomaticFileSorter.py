from pathlib import Path
import shutil

# CHANGE THIS PATH
SOURCE_DIR = Path("C:/Users/Domag/Desktop/Automatic Sort Test/")
FILE_TYPES_TXT = SOURCE_DIR / "fileTypes.txt"

# STEP 1: Detect file types
file_types = set()

for item in SOURCE_DIR.iterdir():
    if item.is_file():
        ext = item.suffix.lower()
        if ext:
            file_types.add(ext)


# STEP 2: Save to fileTypes.txt
with open(FILE_TYPES_TXT, "w") as f:
    for ext in sorted(file_types):
        f.write(ext + "\n")

# STEP 3: Read fileTypes.txt
with open(FILE_TYPES_TXT, "r") as f:
    types_from_file = [line.strip() for line in f if line.strip()]

# STEP 4: Create folders
for ext in types_from_file:
    folder_name = f"Files Type {ext[1:]}"  # remove dot
    folder_path = SOURCE_DIR / folder_name
    folder_path.mkdir(exist_ok=True)

# STEP 5: Move files
for item in SOURCE_DIR.iterdir():
    if item.is_file() and item.name != FILE_TYPES_TXT.name:
        ext = item.suffix.lower()
        if ext in types_from_file:
            destination = SOURCE_DIR / f"Files Type {ext[1:]}" / item.name
            shutil.move(str(item), destination)
