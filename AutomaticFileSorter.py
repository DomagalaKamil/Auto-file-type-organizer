from pathlib import Path
import shutil

# Set the path to the folder containing the files
SOURCE_DIR = Path("path/to/source_folder/")
FILE_TYPES_TXT = SOURCE_DIR / "fileTypes.txt"


def get_unique_destination_path(destination_folder: Path, filename: str) -> Path:
    
   # Returns a unique file path by appending (1), (2), etc.
   # Mimics Windows duplicate file naming behavior.
    
    base_name = Path(filename).stem
    extension = Path(filename).suffix

    candidate = destination_folder / filename
    counter = 1

    while candidate.exists():
        candidate = destination_folder / f"{base_name}({counter}){extension}"
        counter += 1

    return candidate

# STEP 1: Detect file types
file_types = set()

for item in SOURCE_DIR.iterdir():
    if item.is_file():
        # Skip the control file
        if item.name == FILE_TYPES_TXT.name:
            continue

        ext = item.suffix.lower()
        if ext:
            file_types.add(ext)

# STEP 2: Save file types
with open(FILE_TYPES_TXT, "w", encoding="utf-8") as f:
    for ext in sorted(file_types):
        f.write(ext + "\n")

# STEP 3: Read file types
with open(FILE_TYPES_TXT, "r", encoding="utf-8") as f:
    types_from_file = [line.strip() for line in f if line.strip()]

# STEP 4: Create folders
for ext in types_from_file:
    folder_name = f"Files Type {ext[1:]}"  # remove dot
    folder_path = SOURCE_DIR / folder_name
    folder_path.mkdir(exist_ok=True)

# STEP 5: Move files safely
for item in SOURCE_DIR.iterdir():
    if item.is_file():
        # Skip the control file
        if item.name == FILE_TYPES_TXT.name:
            continue

        ext = item.suffix.lower()
        if ext in types_from_file:
            destination_folder = SOURCE_DIR / f"Files Type {ext[1:]}"
            destination_path = get_unique_destination_path(
                destination_folder,
                item.name
            )

            shutil.move(str(item), destination_path)

