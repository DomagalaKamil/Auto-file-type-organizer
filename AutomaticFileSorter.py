from pathlib import Path
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox


def get_unique_destination_path(destination_folder: Path, filename: str) -> Path:
    """
    Generate a unique destination path for a file.

    If a file with the same name already exists in the destination folder,
    this function appends (1), (2), (3), etc. to the filename, mimicking
    Windows duplicate file naming behavior.

    Example:
        Document.docx
        Document(1).docx
        Document(2).docx
    """
    base_name = Path(filename).stem
    extension = Path(filename).suffix

    candidate = destination_folder / filename
    counter = 1

    # Loop until a filename that does not exist is found
    while candidate.exists():
        candidate = destination_folder / f"{base_name}({counter}){extension}"
        counter += 1

    return candidate


def organize_files(source_dir: Path):
    """
    Organize files in the given directory by their file extension.

    - Detects all file types dynamically
    - Stores detected types in fileTypes.txt
    - Creates folders based on file types
    - Moves files into their respective folders
    - Prevents overwriting by handling duplicate filenames
    - Excludes folders and the control file (fileTypes.txt)
    """
    FILE_TYPES_TXT = source_dir / "fileTypes.txt"

    # STEP 1: Detect unique file types
    file_types = set()

    for item in source_dir.iterdir():
        if item.is_file():
            # Skip the control file
            if item.name == FILE_TYPES_TXT.name:
                continue

            ext = item.suffix.lower()
            if ext:
                file_types.add(ext)

    # STEP 2: Save file types to text file
    with open(FILE_TYPES_TXT, "w", encoding="utf-8") as f:
        for ext in sorted(file_types):
            f.write(ext + "\n")

    # STEP 3: Read file types from text file
    with open(FILE_TYPES_TXT, "r", encoding="utf-8") as f:
        types_from_file = [line.strip() for line in f if line.strip()]

    # STEP 4: Create folders for each file type
    for ext in types_from_file:
        folder_name = f"Files Type {ext[1:]}"  # remove the dot from extension
        (source_dir / folder_name).mkdir(exist_ok=True)

    # STEP 5: Move files into folders safely
    for item in source_dir.iterdir():
        if item.is_file():
            # Skip the control file
            if item.name == FILE_TYPES_TXT.name:
                continue

            ext = item.suffix.lower()
            if ext in types_from_file:
                destination_folder = source_dir / f"Files Type {ext[1:]}"
                destination_path = get_unique_destination_path(
                    destination_folder,
                    item.name
                )

                shutil.move(str(item), destination_path)


def select_folder_and_run():
    """
    Open a folder selection dialog and run the file organizer.

    - Allows the user to select a folder via a GUI
    - Runs the file organization logic on the selected folder
    - Displays success or error messages
    """
    folder_path = filedialog.askdirectory(
        title="Select Folder to Organize"
    )

    # User canceled folder selection
    if not folder_path:
        messagebox.showwarning(
            "No Folder Selected",
            "Operation cancelled."
        )
        return

    try:
        organize_files(Path(folder_path))
        messagebox.showinfo(
            "Success",
            "Files have been successfully organized."
        )
    except Exception as e:
        messagebox.showerror(
            "Error",
            str(e)
        )


# Basic UI Setup
root = tk.Tk()
root.title("Auto File Type Organizer")
root.geometry("300x150")
root.resizable(False, False)

label = tk.Label(
    root,
    text="Select a folder to organize files",
    pady=20
)
label.pack()

run_button = tk.Button(
    root,
    text="Choose Folder",
    command=select_folder_and_run,
    width=20
)
run_button.pack()

# Start the GUI event loop
root.mainloop()
